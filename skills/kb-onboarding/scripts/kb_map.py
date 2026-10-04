#!/usr/bin/env python3
"""kb_map.py — 知识库冷启动地图扫描器（只读，零依赖）

用途：kb-onboarding 技能在开口提问之前先跑这个，拿到「用户库里真实有什么」，
据此生成一句话能答完的具体选项——而不是通用人生问卷。

用法：
    python3 kb_map.py                        # 扫当前目录
    python3 kb_map.py --vault ~/my-vault
    python3 kb_map.py --json                 # 机器可读输出
    python3 kb_map.py --recent 5             # 只看最近 5 条更新

退出码恒为 0（这是只读扫描器，不该阻断流程）。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

LAYERS = ["_raw", "_wiki", "_workspace", "_assets"]
# 模板名 → 该模板应当落进的目录（用于判断「空白区」）
TEMPLATE_TARGETS = {
    "想法": "_wiki/ideas",
    "idea": "_wiki/ideas",
    "概念": "_wiki/concepts",
    "concept": "_wiki/concepts",
    "人物": "_wiki/people",
    "people": "_wiki/people",
    "决策": "_wiki/decisions",
    "decision": "_wiki/decisions",
    "日记": "_raw/journal",
    "journal": "_raw/journal",
    "碎片": "_raw/fragments",
    "fragments": "_raw/fragments",
}
STALE_SEED_DAYS = 30
# 空白区/线索的人话叫法——小白看不懂 `_raw/fragments` 这种路径
HUMAN_NAMES = {
    "_raw/fragments/": "随手记的碎片",
    "_raw/journal/": "每天的日记",
    "_raw/chat/": "聊天记录",
    "_wiki/ideas/": "想法",
    "_wiki/concepts/": "概念/方法论",
    "_wiki/people/": "人物",
    "_wiki/decisions/": "做过的决定",
    "_workspace/": "正在做的工作",
}


def md_files(root: Path):
    for p in root.rglob("*.md"):
        if any(part.startswith(".") for part in p.parts):
            continue
        if "_templates" in p.parts:
            continue
        yield p


def read_head(path: Path, max_bytes: int = 4000) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")[:max_bytes]
    except OSError:
        return ""


def extract_title(path: Path, text: str) -> str:
    m = re.search(r"^#\s+(.+)$", text, re.M)
    if m:
        return m.group(1).strip()[:60]
    return path.stem


def extract_frontmatter(text: str) -> dict:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    block = text[3:end]
    out: dict = {}
    for line in block.splitlines():
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line.strip())
        if m:
            out[m.group(1).lower()] = m.group(2).strip()
    tags_raw = out.get("tags", "")
    tags = re.findall(r"[\w/\-]+", tags_raw.strip("[]").replace('"', "").replace("'", ""))
    out["_tags"] = tags
    return out


def collect(root: Path) -> dict:
    files = list(md_files(root))
    layers = {layer: 0 for layer in LAYERS}
    recent = []
    tags: dict[str, int] = {}
    ideas_seed = []

    for p in files:
        rel = p.relative_to(root)
        top = rel.parts[0] if rel.parts else ""
        if top in layers:
            layers[top] += 1
        try:
            mtime = datetime.fromtimestamp(p.stat().st_mtime, tz=timezone.utc)
        except OSError:
            mtime = datetime.now(tz=timezone.utc)
        text = read_head(p)
        fm = extract_frontmatter(text)
        recent.append({
            "path": str(rel),
            "title": extract_title(p, text),
            "mtime": mtime,
            "tags": fm.get("_tags", []),
        })
        for t in fm.get("_tags", []):
            tags[t] = tags.get(t, 0) + 1
        if "ideas" in rel.parts and fm.get("status", "").lower() == "seed":
            created = fm.get("created", "")
            ideas_seed.append({"path": str(rel), "created": created, "title": extract_title(p, text)})

    recent.sort(key=lambda r: r["mtime"], reverse=True)
    return {
        "layers": layers,
        "total_md": len(files),
        "recent": recent,
        "tags": tags,
        "ideas_seed": ideas_seed,
        "templates": sorted({p.stem for p in (root / "_templates").glob("*.md")})
        if (root / "_templates").is_dir() else [],
    }


def blank_zones(root: Path, data: dict) -> list[str]:
    """有模板但落点目录为空 = 冷启动空白区。子目录里有内容也算有内容。"""
    blanks = []
    for tpl, target in TEMPLATE_TARGETS.items():
        if not any(tpl in name for name in data["templates"]):
            continue
        target_dir = root / target
        count = sum(1 for _ in target_dir.rglob("*.md")) if target_dir.is_dir() else 0
        if count == 0:
            blanks.append(f"{target}/（模板已备：{tpl}）")
    return sorted(set(blanks))


def human_zone(zone: str) -> str:
    """把 `_raw/fragments/（模板已备：碎片）` 转成小白能懂的「随手记的碎片」。"""
    path = zone.split("（")[0]
    return HUMAN_NAMES.get(path, path.rstrip("/"))


def is_infra(rel: str) -> bool:
    """工具/结构文件不算「用户的真实内容」，不要拿来生成提问。"""
    p = rel.replace("\\", "/")
    name = p.rsplit("/", 1)[-1]
    if name in ("index.md", "log.md", "README.md", "AGENTS.md", "CLAUDE.md", "manifest.json"):
        return True
    if "/skills/" in p or p.startswith("_templates/"):
        return True
    return False


def open_threads(data: dict) -> list[dict]:
    threads = []
    for it in data["ideas_seed"]:
        created = it.get("created", "")
        try:
            d = datetime.strptime(created[:10], "%Y-%m-%d").replace(tzinfo=timezone.utc)
            stale = datetime.now(tz=timezone.utc) - d > timedelta(days=STALE_SEED_DAYS)
            when = f"{created[:10]} 起 seed，未推进"
        except ValueError:
            stale = True
            when = "seed，创建日期不明"
        if stale:
            threads.append({"title": it.get("title") or it["path"], "path": it["path"], "note": when})
    return threads


def print_human(root: Path, data: dict, blanks: list[str], threads: list[dict], recent_n: int) -> None:
    print(f"=== 知识库地图：{root} ===")
    total = data["total_md"]
    if total == 0:
        print("\n【全新库】一条内容都没有。")
        print("冷启动建议（从最容易的开始，一次只问一个）：")
        print("  1. 「今天有什么事，是你回头还想得起来的？」→ 落 _raw/journal/")
        print("  2. 「最近有没有谁让你印象挺深？」→ 落 _wiki/people/")
        print("  3. 「有没有什么事，你现在就想把它搞定？」→ 落 _wiki/ideas/")
        print("\n提示：先别问目标/规划这类大问题。空库阶段要的是「真实发生过的小事」。")
        return

    print(f"\n【规模】共 {total} 条笔记")
    for layer in LAYERS:
        bar = "█" * min(data["layers"][layer], 20)
        print(f"  {layer:<12} {data['layers'][layer]:>4} 条  {bar}")

    if data["tags"]:
        top = sorted(data["tags"].items(), key=lambda kv: -kv[1])[:8]
        print(f"\n【主题分布】{', '.join(f'{k}({v})' for k, v in top)}")

    content_recent = [r for r in data["recent"] if not is_infra(r["path"])]
    print(f"\n【最近更新】（{min(recent_n, len(data['recent']))} 条）")
    for r in data["recent"][:recent_n]:
        age = (datetime.now(tz=timezone.utc) - r["mtime"]).days
        print(f"  · {r['title']}")
        print(f"      {r['path']}  —— {age} 天前")

    if threads:
        print(f"\n【未闭环线索】（优先问这些）")
        for t in threads[:6]:
            print(f"  ? {t['title']}  —— {t['note']}  ({t['path']})")

    if blanks:
        print(f"\n【空白区】（模板已备但还没内容）")
        for b in blanks:
            print(f"  ○ {human_zone(b)}   ← {b.split('（')[0].rstrip('/')}")

    print("\n【据此可问的三类问题】")
    if threads:
        print(f"  ① 追下文：「{threads[0]['title']}」这条，后来怎么样了？")
    if content_recent:
        t = content_recent[0]["title"]
        print(f"  ② 挖深一层：「你上次提到『{t}』，当时是怎么想的？」")
    if blanks:
        print(f"  ③ 填空白：「{human_zone(blanks[0])} 这块，你最近有想过什么吗？」")
    if not (threads or content_recent or blanks):
        print("  （库内容已较完整）问「最近有什么事，是你想记但还没记的？」")


def main() -> int:
    ap = argparse.ArgumentParser(description="知识库冷启动地图（只读）")
    ap.add_argument("--vault", default=".", help="知识库根目录（默认当前目录）")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    ap.add_argument("--recent", type=int, default=5, help="展示最近 N 条更新")
    args = ap.parse_args()

    root = Path(args.vault).expanduser().resolve()
    if not root.is_dir():
        print(f"[kb_map] ❌ 目录不存在: {root}")
        return 0

    data = collect(root)
    blanks = blank_zones(root, data)
    threads = open_threads(data)

    if args.json:
        payload = {
            "vault": str(root),
            "total_md": data["total_md"],
            "layers": data["layers"],
            "tags": data["tags"],
            "blank_zones": blanks,
            "open_threads": threads,
            "recent": [
                {"path": r["path"], "title": r["title"], "days_ago": (datetime.now(tz=timezone.utc) - r["mtime"]).days}
                for r in data["recent"][: args.recent]
            ],
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print_human(root, data, blanks, threads, args.recent)
    return 0


if __name__ == "__main__":
    sys.exit(main())
