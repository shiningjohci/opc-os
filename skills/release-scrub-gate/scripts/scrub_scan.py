#!/usr/bin/env python3
"""scrub_scan.py — 发布脱敏 L1 机械扫描器（确定性，只读，零依赖）

用途：发布前第一道门。抓确定性模式（凭据 / 主机 / 私有路径 / 个人数字）。
语义泄露（示例措辞、反推线索）抓不到——那是 L2 双 agent 的活。

用法：
    python3 scrub_scan.py --root .                      # 扫当前目录
    python3 scrub_scan.py --root . --local scrub-patterns.local.txt
    python3 scrub_scan.py --root . --json               # 机器可读
    python3 scrub_scan.py --root . --ignore README.md   # 排除有意公开的文件

退出码：0 = 干净；1 = 有命中（可用于 CI / 发布闸门）。

⚠️ 本文件的通用规则里【绝不放】你自己的真实姓名/公司/店铺名——
   那些放进本地 scrub-patterns.local.txt（并加进 .gitignore）。
   否则扫描器本身就成了泄露源。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# 通用规则：任何项目都适用，不含任何特定个人信息
GENERIC_RULES: list[tuple[str, str, str]] = [
    # (类别, 严重度, 正则)
    ("凭据", "high", r"(?i)\b(sk-[A-Za-z0-9]{16,}|ghp_[A-Za-z0-9]{20,}|gho_[A-Za-z0-9]{20,}|xox[baprs]-[A-Za-z0-9-]{10,}|AKIA[0-9A-Z]{16})\b"),
    ("凭据", "high", r"(?i)\b(api[_-]?key|secret|passwd|password|access[_-]?token|private[_-]?key)\s*[:=]\s*[\"']?[A-Za-z0-9_\-./+]{12,}"),
    ("凭据", "medium", r"(?i)\bBearer\s+[A-Za-z0-9_\-.]{20,}"),
    ("主机", "high", r"\b(?:\d{1,3}\.){3}\d{1,3}\b(?![\d.])"),          # 任意 IPv4（内网/公网一律报）
    ("主机", "medium", r"(?i)\b(ssh|scp|rsync)\s+[a-z0-9_.-]+@[a-z0-9.-]+"),
    ("主机", "medium", r"(?i)\b(tailscale|wireguard|vpn)\b.*\b\d{1,3}(\.\d{1,3}){3}\b"),
    ("路径", "medium", r"(/Users/|/home/|C:\\\\Users\\\\)[A-Za-z0-9_.-]+"),
    ("路径", "low", r"(?i)\b(\.hermes|\.codex|\.claude)/[a-z0-9_/-]+"),
    ("身份", "medium", r"(?i)\b(github\.com/)[A-Za-z0-9-]+/[A-Za-z0-9._-]+"),
    ("身份", "low", r"[\w.+-]+@[\w-]+\.[\w.]{2,}"),                       # 邮箱
    ("金额", "low", r"(?i)(月薪|底薪|年薪|工资|薪资|总资产|净资产)\s*[:：]?\s*[\d,，.]+\s*(万|k|K|元)?"),
]

SCAN_EXT = {".md", ".py", ".json", ".yaml", ".yml", ".sh", ".txt", ".js", ".ts"}


def load_local_patterns(path: Path | None) -> list[tuple[str, str, str]]:
    """本地词表：每行一个词或 /正则/，格式 [类别:]词语。"""
    rules = []
    if not path or not path.is_file():
        return rules
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        cat = "本地词表"
        if ":" in line and not line.startswith("/"):
            head, _, tail = line.partition(":")
            if head in ("身份", "业务", "私事", "凭据", "主机", "路径", "金额"):
                cat, line = head, tail.strip()
        if line.startswith("/") and line.endswith("/") and len(line) > 2:
            rules.append((cat, "high", line[1:-1]))
        else:
            rules.append((cat, "high", re.escape(line)))
    return rules


def _resolve_deny_path(explicit: str | None, filename: str) -> Path:
    """词表查找顺序：显式参数 → 脚本同级 private/（知识库主副本）→ ~/.config/opc-os/（兜底副本）。
    主副本放在技能的 private/ 目录里以便备份与编辑，但**绝不随产品发布**——
    发布管道会硬拒 private/ 与 deny-*（见 publish_os.py）。"""
    if explicit:
        p = Path(explicit).expanduser()
        if p.is_file():
            return p
    here = Path(__file__).resolve().parent.parent / "private" / filename   # 技能根/private/
    if here.is_file():
        return here
    alt = Path(__file__).resolve().parent / "private" / filename           # scripts/private/
    if alt.is_file():
        return alt
    return Path.home() / ".config" / "opc-os" / filename


def load_deny_list(path: Path | None) -> dict[str, str]:
    """跨语料 deny-list：{值: 类别}。从私有语料抽取，本地维护，**不随产品发布**——
    它本身就是一份「哪些值不能见人」的清单，发布它等于把答案发出去。"""
    if not path or not path.is_file():
        return {}
    try:
        return {str(k): str(v) for k, v in json.loads(path.read_text(encoding="utf-8")).items()}
    except Exception:
        return {}


def load_deny_phrases(path: Path | None) -> list[str]:
    """禁发原句。人工维护，同样不随产品发布。"""
    if not path or not path.is_file():
        return []
    out = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line and not line.startswith("#"):
            out.append(line)
    return out


def _self_slugs(root):
    """仓库自身的公开地址（owner/repo）不是泄露——它是产物的下载地址。
    只豁免含完整 slug 的命中；单独出现的账号名仍照常报警。"""
    try:
        import subprocess
        r = subprocess.run(["git", "-C", str(root), "remote", "get-url", "origin"],
                           capture_output=True, text=True, timeout=5)
        if r.returncode == 0:
            m = re.search(r"github\.com[:/]([^/]+/[^/.]+)", r.stdout.strip())
            if m:
                return {m.group(1)}
    except Exception:
        pass
    return set()


def main() -> int:
    ap = argparse.ArgumentParser(description="发布脱敏 L1 机械扫描")
    ap.add_argument("--root", default=".", help="扫描根目录")
    ap.add_argument("--local", default="scrub-patterns.local.txt", help="本地私密词表（不入库）")
    ap.add_argument("--ignore", nargs="*", default=[], help="排除的文件名（有意公开的，如 README.md）")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--deny-list", default=None,
                    help="跨语料 deny-list 路径（默认：脚本同级 private/，其次 ~/.config/opc-os/）")
    ap.add_argument("--deny-phrases", default=None,
                    help="禁发原句路径（默认同上；两份清单均不随产品发布）")
    args = ap.parse_args()

    root = Path(args.root).expanduser().resolve()
    rules = GENERIC_RULES + load_local_patterns(root / args.local)
    compiled = [(c, s, re.compile(p)) for c, s, p in rules]
    deny_list = load_deny_list(_resolve_deny_path(args.deny_list, "deny-list.json"))
    deny_phrases = load_deny_phrases(_resolve_deny_path(args.deny_phrases, "deny-phrases.txt"))
    ignore = {n.lower() for n in args.ignore}
    self_slugs = _self_slugs(root)   # 仓库自身地址豁免（owner/repo）

    findings = []
    scanned = 0
    for p in sorted(root.rglob("*")):
        if not p.is_file() or p.suffix.lower() not in SCAN_EXT:
            continue
        if any(part.startswith(".") and part != "." for part in p.relative_to(root).parts[:-1]):
            continue
        if p.name.lower() in ignore:
            continue
        rel = str(p.relative_to(root))
        try:
            lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        scanned += 1
        for i, line in enumerate(lines, 1):
            for cat, sev, rx in compiled:
                m = rx.search(line)
                if not m:
                    continue
                if any(s in m.group(0) for s in self_slugs):
                    continue      # 仓库自身地址（owner/repo）不是泄露
                findings.append({
                        "file": rel, "line": i, "category": cat, "severity": sev,
                        "quoted": m.group(0)[:60], "context": line.strip()[:90],
                    })
            # 跨语料闸：私有语料里的值 / 禁发原句，出现在发布物里 = 泄露
            for term, cat in deny_list.items():
                if term in line:
                    findings.append({
                        "file": rel, "line": i, "category": f"跨语料·{cat}", "severity": "high",
                        "quoted": term[:60], "context": line.strip()[:90],
                    })
            for ph in deny_phrases:
                if ph in line:
                    findings.append({
                        "file": rel, "line": i, "category": "禁发原句", "severity": "high",
                        "quoted": ph[:60], "context": line.strip()[:90],
                    })

    if args.json:
        print(json.dumps({"scanned_files": scanned, "findings": findings}, ensure_ascii=False, indent=2))
    else:
        print(f"=== L1 机械扫描：{root} ===")
        print(f"扫描 {scanned} 个文件，规则 {len(compiled)} 条（通用 {len(GENERIC_RULES)} + 本地 {len(rules)-len(GENERIC_RULES)}）"
              f" + 跨语料 {len(deny_list)} 项 + 禁发原句 {len(deny_phrases)} 句")
        if not findings:
            print("\n✅ 0 命中——L1 通过（注意：L1 通过 ≠ 可以发布，还要过 L2 语义审核）")
        else:
            print(f"\n❌ {len(findings)} 处命中：")
            for f in findings[:40]:
                print(f"  [{f['severity']:6}] {f['file']}:{f['line']}  ({f['category']}) {f['quoted']}")
                print(f"           {f['context']}")
            if len(findings) > 40:
                print(f"  … 另有 {len(findings)-40} 处")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
