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

- **Git 历史**：扫描当前工作树，不检查 Git 对象库中的旧提交；发布前需单独检查待发布 diff/历史，避免旧版本残留。
- **本地词表**：默认查找扫描根目录下的 `scrub-patterns.local.txt`，不存在时按无本地规则运行；若显式传入 `--local`，路径必须存在且为文件。词表作为匹配规则，不会作为扫描输入。
- 默认也扫描支持类型的隐藏目录与隐藏文件；仅跳过版本控制元数据目录以及依赖/虚拟环境目录。
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
    ("主机", "high", r"(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?!\d)(?!\.\d)"),          # 任意 IPv4（内网/公网一律报）
    ("主机", "medium", r"(?i)\b(ssh|scp|rsync)\s+[a-z0-9_.-]+@[a-z0-9.-]+"),
    ("主机", "medium", r"(?i)\b(tailscale|wireguard|vpn)\b.*\b\d{1,3}(\.\d{1,3}){3}\b"),
    ("路径", "medium", r"(/Users/|/home/|C:\\\\Users\\\\)[A-Za-z0-9_.-]+"),
    ("路径", "low", r"(?i)\b(\.hermes|\.codex|\.claude)/[a-z0-9_/-]+"),
    ("身份", "medium", r"(?i)\b(github\.com/)[A-Za-z0-9-]+/[A-Za-z0-9._-]+"),
    ("身份", "low", r"[\w.+-]+@[\w-]+\.[\w.]{2,}"),                       # 邮箱
    ("金额", "low", r"(?i)(月薪|底薪|年薪|工资|薪资|总资产|净资产)\s*[:：]?\s*[\d,，.]+\s*(万|k|K|元)?"),
]

SCAN_EXT = {".md", ".py", ".json", ".yaml", ".yml", ".sh", ".txt", ".js", ".ts"}
SKIP_DIRS = {".git", ".hg", ".svn", "node_modules", ".venv", "venv"}


def iter_scan_files(root: Path):
    for p in sorted(root.rglob("*")):
        if not p.is_file() or any(part in SKIP_DIRS for part in p.relative_to(root).parts[:-1]):
            continue
        if p.suffix.lower() in SCAN_EXT or any(p.name.lower().endswith(ext) for ext in SCAN_EXT):
            yield p


def load_local_patterns(path: Path | None) -> list[tuple[str, str, str]]:
    """Load additional local wordlist entries as scan rules."""
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
            pattern = line[1:-1]
        else:
            pattern = re.escape(line)
        rules.append((cat, "high", pattern))
    return rules


def main() -> int:
    ap = argparse.ArgumentParser(description="发布脱敏 L1 机械扫描")
    ap.add_argument("--root", default=".", help="扫描根目录")
    ap.add_argument("--local", default=None, help="本地私密词表（显式提供时必须存在；默认位置缺失时按无本地规则处理）")
    ap.add_argument("--ignore", nargs="*", default=[], help="排除的文件名（有意公开的，如 README.md）")
    ap.add_argument("--json", action="store_true")
    ap.add_argument(
        "--show-sensitive-context", action="store_true",
        help="include matched text in local human-readable output for debugging; disabled with --json",
    )
    args = ap.parse_args()
    if args.show_sensitive_context and args.json:
        ap.error("--show-sensitive-context cannot be used with --json")

    root = Path(args.root).expanduser().resolve()
    if not root.is_dir():
        print("[scrub_scan] 扫描目录无效")
        return 2
    local_path = Path(args.local).expanduser() if args.local else root / "scrub-patterns.local.txt"
    if args.local and not local_path.is_absolute():
        local_path = root / local_path
    local_path = local_path.resolve()
    if args.local and not local_path.is_file():
        print("[scrub_scan] 显式指定的本地词表不可用")
        return 2
    rules = GENERIC_RULES + load_local_patterns(local_path)
    compiled = [(c, s, re.compile(p)) for c, s, p in rules]
    ignore = {n.lower() for n in args.ignore}

    def safe_rel_path(rel: str) -> str:
        safe = rel
        for _, _, rx in compiled:
            safe = rx.sub("[REDACTED]", safe)
        return safe

    def matches_path(rel: str) -> list[tuple[str, str]]:
        return [(cat, sev) for cat, sev, rx in compiled if rx.search(rel)]

    def findings_for_path(rel: str) -> list[tuple[str, str]]:
        """One hit per category per path: a filename matches a category at most once."""
        seen: set[str] = set()
        out = []
        for cat, sev in matches_path(rel):
            if cat not in seen:
                out.append((cat, sev))
                seen.add(cat)
        return out

    def add_finding(rel: str, line: int, cat: str, sev: str, quoted: str | None = None, context: str | None = None) -> None:
        safe_path = safe_rel_path(rel)
        key = (safe_path, line)
        finding = findings_by_key.get(key)
        if finding is None:
            finding = {"file": safe_path, "line": line, "_cats": [cat], "severity": sev}
            findings_by_key[key] = finding
            findings_order.append(key)
        else:
            if cat in finding["_cats"]:
                finding["occurrences"] = finding.get("occurrences", 1) + 1
            else:
                finding["_cats"].append(cat)
            if sev == "high":
                finding["severity"] = "high"
        if args.show_sensitive_context and quoted is not None:
            finding["quoted"] = quoted[:60]
            if context is not None:
                finding["context"] = context[:90]

    findings_order: list[tuple[str, int]] = []
    findings_by_key: dict[tuple[str, int], dict] = {}
    scanned = 0
    for p in iter_scan_files(root):
        if p == local_path.resolve():
            continue
        if p.name.lower() in ignore:
            continue
        rel = str(p.relative_to(root))
        for cat, sev in findings_for_path(rel):
            add_finding(rel, 0, cat, sev)
        if p.is_symlink():
            continue
        try:
            lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        scanned += 1
        for i, line in enumerate(lines, 1):
            for cat, sev, rx in compiled:
                match = rx.search(line)
                if match:
                    add_finding(rel, i, cat, sev, match.group(0), line.strip())

    findings = []
    for key in findings_order:
        f = findings_by_key[key]
        f["category"] = ", ".join(f.pop("_cats"))
        findings.append(f)
    if args.json:
        print(json.dumps({"scanned_files": scanned, "findings": findings}, ensure_ascii=False, indent=2))
    else:
        print(f"=== L1 机械扫描：{root.name or '扫描目录'} ===")
        print(f"扫描 {scanned} 个文件，规则 {len(compiled)} 条（通用 {len(GENERIC_RULES)} + 本地 {len(rules)-len(GENERIC_RULES)}）")
        if not findings:
            print("\n✅ 0 命中——L1 通过（注意：L1 通过 ≠ 可以发布，还要过 L2 语义审核）")
        else:
            print(f"\n❌ {len(findings)} 处命中：")
            for f in findings[:40]:
                detail = f" {f.get('quoted', '')}" if args.show_sensitive_context else ""
                print(f"  [{f['severity']:6}] {f['file']}:{f['line']}  ({f['category']}){detail}")
                if args.show_sensitive_context:
                    print(f"           {f.get('context', '')}")
            if len(findings) > 40:
                print(f"  … 另有 {len(findings)-40} 处")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
