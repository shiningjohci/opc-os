<div align="center">

# 🏢 OPC-OS

### 一人公司操作系统（One-Person Company Operating System）

**把一个人的知识库、AI 工作流和模板，变成一台能自己跑的机器。**

*给一人公司用的个人操作系统：知识库架构 + AI 工作流 + 经过真实使用检验的模板。这里没有「最佳实践」空话——能进这个仓库的，都是在真实业务里跑过的。*

[![EN](https://img.shields.io/badge/Lang-English-blue)](README.md)
[![中文](https://img.shields.io/badge/Lang-%E4%B8%AD%E6%96%87-orange)](README.zh-CN.md)

[![Code: MIT](https://img.shields.io/badge/Code-MIT-blue.svg)](LICENSE)
[![Docs: CC BY 4.0](https://img.shields.io/badge/Docs-CC%20BY%204.0-lightgrey)](https://creativecommons.org/licenses/by/4.0/)
![Status: Living](https://img.shields.io/badge/Status-Living%20Repo-brightgreen)

</div>

---

## 为什么有这个仓库

我经营跨境电商，并且用 AI Agent 自动化自己团队的日常工作。这个仓库里的每一个文件，都来自我**每天都在用的真实系统**——不是周末拍脑袋造出来的模板。

- ✅ 运行了几个月的 Obsidian 知识库架构
- ✅ 团队真正在执行的工作流
- ✅ 经历过真实面试、真实发布、真实决策的模板

> ⭐ 如果对你有帮助，点个 Star——这能告诉我接下来该做什么。

## 你能得到什么

| | |
|---|---|
| 🧠 **知识库架构** | 四层知识库：原始输入 → 百科 → 工作区 → 附件，带语义链接和统一状态机 |
| 🤖 **AI 工作流** | 11 个可执行工作流：碎片加工 → 多平台草稿、招聘全流程、资料摄入、内容复盘 |
| 📋 **模板** | 16 个即用 Obsidian 模板：决策记录（ADR 风格）、想法、人物、概念、招聘全流程（JD → 问题清单 → 面试记录 → 结论 → 对比） |
| 🛡️ **发布纪律** | 任何内容公开前先过脱敏检查：机械扫描 + 子 Agent 审核 + 人工终审 |
| 🔄 **同步管道** | 一条命令把私人库的白名单文件同步到本仓库——只发布白名单，隐私永不泄露 |

## 快速开始

```bash
git clone https://github.com/shiningjohci/opc-os.git
cd opc-os
```

1. 读 `docs/AGENTS.example.md`——知识库架构的完整操作手册
2. 把任意 `templates/` 文件复制进你自己的 Obsidian vault 的 `_templates/`
3. 从 `templates/idea.md` 和 `templates/decision-record.md` 开始——它们是骨架

## 仓库结构

```
opc-os/
├── docs/
│   ├── AGENTS.example.md   # 完整知识库操作手册（已脱敏）
│   └── architecture.md     # 四层架构设计详解
├── templates/              # 16 个 Obsidian 模板
├── workflows/              # （规划中）分步 AI 工作流
├── skills/
│   ├── kb-onboarding/      # 冷启动访谈：让 agent 会问，而不是让用户会问
│   └── release-scrub-gate/ # 发布脱敏三重门：机械扫描 → 双 agent 审核 → 人工签收
└── tools/
    ├── publish_os.py       # 私人库 → 公开仓库（白名单 + 脱敏）
    └── manifest.json       # 文件映射 + 秘密替换规则
```

## 我怎么保持这个仓库更新

我的私人知识库通过 Obsidian Git 插件同步到私人仓库。要发布时，一条命令搞定：

```bash
python3 tools/publish_os.py --dry-run   # 预览将要发布的文件
python3 tools/publish_os.py             # 复制 + 提交
python3 tools/publish_os.py --push      # 复制 + 提交 + 推送
```

只有 `tools/manifest.json` 里列出的文件会被发布。每次发布前自动跑敏感词扫描，命中即中止。原始知识库（笔记、人物、私密决策）永远不会进入这个仓库。

## 许可

- 代码与脚本：**MIT**
- 文档与模板：**CC BY 4.0**

## 作者

**Simon（刘琦峰）**——跨境电商运营者，AI 工作流实践者。写关于「用 AI 带小团队」和「搭建一人公司 OS」的内容。

- GitHub: [@shiningjohci](https://github.com/shiningjohci)
- 小红书: [Simon](https://www.xiaohongshu.com/user/profile/680b0ee2000000001802502d)
- 知乎: [刘琦峰](https://www.zhihu.com/people/liu-qi-feng-66)
- 合作：通过以上平台联系

---

*活仓库。每月发布一个工作流或模板。*
