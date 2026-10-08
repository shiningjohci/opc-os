<div align="center">

# 🏢 OPC-OS

### One-Person Company Operating System

*A personal OS for running a one-person company with AI — a vault architecture, Codex workflows, and templates that survived real daily use. No best-practices filler: if it's here, it ships.*

[![Code: MIT](https://img.shields.io/badge/Code-MIT-blue.svg)](LICENSE)
[![Docs: CC BY 4.0](https://img.shields.io/badge/Docs-CC%20BY%204.0-lightgrey)](https://creativecommons.org/licenses/by/4.0/)
![Status: Living](https://img.shields.io/badge/Status-Living%20Repo-brightgreen)
[![EN](https://img.shields.io/badge/Lang-English-blue)](README.md)
[![中文](https://img.shields.io/badge/Lang-%E4%B8%AD%E6%96%87-orange)](README.zh-CN.md)

</div>

---

## Why this exists

I run cross-border e-commerce operations and build AI agents to automate my own team. Every file in this repo is extracted from my **actual daily system** — not a template someone made up over a weekend.

- ✅ Obsidian vault architecture I've run for months
- ✅ Workflows my team actually executes
- ✅ Templates that survived real interviews, real launches, real decisions

> ⭐ If this helps you, give it a star — it tells me what to ship next.

## What you get

| | |
|---|---|
| 🧠 **Vault architecture** | Four-layer knowledge base: raw input → wiki → workspace → assets, with typed links and a unified state machine |
| 🤖 **AI workflows** | 11 executable workflows: fragment processing → multi-platform drafts, interview pipeline, reference ingestion, content review cycle |
| 📋 **Templates** | 16 ready-to-use Obsidian templates: decisions (ADR-style), ideas, people, concepts, full interview pipeline (JD → questions → notes → conclusion → compare) |
| 🛡️ **Publish discipline** | A desensitization check before anything goes public: mechanical scan + sub-agent review + human sign-off |
| 🔄 **Sync pipeline** | One command publishes selected files from private vault to this repo — whitelist only, secrets never leak |

## Quick start

```bash
git clone https://github.com/shiningjohci/opc-os.git
cd opc-os
```

1. Install [Obsidian](https://obsidian.md/download) if needed. Alternatively download this repository with Code → Download ZIP; Git is optional.
2. Open the folder containing `Home.md` as an Obsidian vault and read [Start here](Home.md).
3. Explore the [fictional e-commerce hiring demo](demos/ecommerce-hiring/00-从这里开始.md); no plugin or AI is required for reading it.
4. Enable Dataview for dynamic lists. Homepage is optional for opening the home note on startup.
5. Follow the [installation guide](docs/install.md) to prepare empty vault folders, selected templates and rules before using a local AI agent.

Downloading files does not install software, plugins or AI skills. AI-assisted plugin installation needs explicit permission, user trust/enablement and actual UI verification. Never overwrite an existing vault's settings. Fixed home entries change with capabilities; dynamic lists query source notes rather than duplicate facts.

Workflows and templates come from real practice; all people, companies, figures and answers in the demo are fictional teaching material, not verified business outcomes.

## Repo layout

```
opc-os/
├── Home.md                 # Four-module home; readable without plugins
├── demos/ecommerce-hiring/  # Self-contained fictional hiring example
├── docs/
│   ├── AGENTS.example.md   # Full vault operating manual (desensitized)
│   ├── architecture.md     # Why the four-layer design works
│   └── install.md          # Manual/AI setup, permissions and verification
├── templates/              # 16 Obsidian templates
├── workflows/              # (coming) step-by-step AI workflows
├── skills/
│   ├── kb-onboarding/      # Cold-start interview: make the agent ask, not the user
│   └── release-scrub-gate/ # 3-gate publish scrub: machine scan → 2 agents → human sign-off
└── tools/
    ├── publish_os.py       # Private vault → public repo (whitelist + scrub)
    └── manifest.json       # File mapping + secret replacement rules
```

## How I keep this repo fresh

My private vault syncs to a private repo via the Obsidian Git plugin. When I want to publish, one command does the rest:

```bash
python3 tools/publish_os.py --dry-run   # preview what will be published
python3 tools/publish_os.py             # copy + commit
python3 tools/publish_os.py --push      # copy + commit + push
```

Only files listed in `tools/manifest.json` are ever published. A sensitive-word scan runs before every publish and aborts on hits. The raw vault — notes, people, private decisions — never touches this repo.

## License

- Code & scripts: **MIT**
- Docs & templates: **CC BY 4.0**

## Author

**Simon** — cross-border e-commerce operator, AI-workflow practitioner. I write about running lean teams with AI and building a one-person-company OS.

- GitHub: [@shiningjohci](https://github.com/shiningjohci)
- Xiaohongshu: [Simon](https://www.xiaohongshu.com/user/profile/680b0ee2000000001802502d)
- Zhihu: [Liu Qifeng](https://www.zhihu.com/people/liu-qi-feng-66)
- Collaboration: reach me via the platforms above

---

*Living repo. I ship one workflow or template per month.*
