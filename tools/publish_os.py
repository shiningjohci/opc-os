#!/usr/bin/env python3
"""OPCOS 发布脚本：私人 vault → 开源仓库（白名单 + 脱敏 + 敏感词扫描）

用法：
  python3 tools/publish_os.py --dry-run   # 预览将发布的文件
  python3 tools/publish_os.py             # 复制 + commit
  python3 tools/publish_os.py --push      # 复制 + commit + push
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="发布一人公司 OS 开源仓库")
    parser.add_argument("--dry-run", action="store_true", help="只预览不写入")
    parser.add_argument("--push", action="store_true", help="commit 后 push")
    parser.add_argument("--vault-root", default=None, help="覆盖 vault 根目录（默认读 manifest）")
    args = parser.parse_args()

    tools_dir = Path(__file__).resolve().parent
    repo = tools_dir.parent
    manifest = json.loads((tools_dir / "manifest.json").read_text(encoding="utf-8"))
    private_cfg = json.loads((Path.home() / ".config/opc-os/config.json").read_text(encoding="utf-8"))
    vault = Path(args.vault_root or private_cfg.get("vault_root") or "")

    email_re = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
    phone_re = re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)")
    secrets = list(private_cfg.get("secret_scan", [])) + list(private_cfg.get("secret_replace", {}).keys())

    plan = []
    for src_rel, dst_rel in manifest["public"].items():
        src = vault / src_rel
        if not src.exists():
            print(f"[中止] 源文件不存在: {src_rel}")
            sys.exit(1)
        text = src.read_text(encoding="utf-8")
        if src_rel not in manifest.get("exempt_scan", []):
            hits = [s for s in secrets if s in text]
            hits += [m.group(0) for m in email_re.finditer(text)]
            hits += [m.group(0) for m in phone_re.finditer(text)]
            if hits:
                print(f"[中止] 敏感词命中: {src_rel} -> {hits}")
                sys.exit(1)
        plan.append((src_rel, dst_rel))

    print(f"将发布 {len(plan)} 个文件到 {repo}")
    if args.dry_run:
        for _, dst in sorted(plan, key=lambda x: x[1]):
            print(f"  {dst}")
        print("dry-run 完成，未写入任何文件")
        return

    for src_rel, dst_rel in sorted(plan, key=lambda x: x[1]):
        src = vault / src_rel
        dst = repo / dst_rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        text = src.read_text(encoding="utf-8")
        for key, value in private_cfg.get("secret_replace", {}).items():
            text = text.replace(key, value)
        dst.write_text(text, encoding="utf-8")
        print(f"  ✓ {src_rel} -> {dst_rel}")

    subprocess.run(["git", "add", "-A"], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-m", f"publish: 同步 {len(plan)} 个文件"], cwd=repo, check=True)
    if args.push:
        subprocess.run(["git", "push"], cwd=repo, check=True)
    print("发布完成")


if __name__ == "__main__":
    main()
