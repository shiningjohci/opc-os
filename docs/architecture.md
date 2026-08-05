# 知识库架构（四层设计）

> 这套架构来自我的个人知识库（Obsidian vault），`AGENTS.example.md` 是它的完整操作手册。这里解释「为什么这么设计」。

## 核心理念

**分层 + 对象化 + 状态机 + 单一事实源**。个人知识库不是一个文件夹堆，而是一个可运行的系统：
原始输入、成品知识、工作产物、附件各自分层；知识以「对象」为单位组织（概念/人物/项目/决策/素材）；
每个对象有生命周期；每个事实只有一个归属页。

## 四层结构

```
_raw/        ← 原始输入层（只读）：微信记录、碎片、日记、参考文章，一字不改
_wiki/       ← 知识百科层：结构化成品知识（concepts/people/projects/decisions/ideas）
_workspace/  ← 工作区：内容生产线（素材库 → 草稿 → 已发布）
_assets/     ← 附件：图片、PDF 等二进制
_templates/  ← Obsidian 模板（Templater 语法）
```

- `_raw/` 是唯一事实来源的输入侧：原始素材只进不出，永不修改
- `_wiki/` 是知识侧：提炼过的、可长期维护的「成品知识」
- `_workspace/` 是输出侧：内容生产管道

## 对象类型与生命周期

| 对象 | 标签 | 生命周期 |
|---|---|---|
| 想法 | #idea | seed → growing → evergreen → archived |
| 决策 | #decision | decided → validated |
| 概念 | #concept | — |
| 人物 | #people | — |
| 项目 | #project | active → done |
| 素材 | （content-library 条目） | 🧪 实验 → 📝 已写稿 → 🟢 已发布 → ♻️ 复盘 |
| 草稿 | （drafts/ 文件） | draft → published |

## 关键机制

### 链接类型化（relations）
frontmatter 里用 `relations` 字段给内链赋予语义（5 类：source / derives_from / relates_to / contradicts / feeds_into），
让知识之间的因果、派生、对立关系可被查询（Dataview），而不只是一团无类型链接。

### 决策记录（ADR 风格）
每个重要决策一个文件：背景 → 选项（≥2）→ 选择 → 理由 → 验证结果 → 认知修正。
决策不散落在日志里，而是可回顾、可迭代的认知飞轮。

### 状态机统一
所有对象类型有统一生命周期，index 页用 Dataview 自动生成看板，不手写维护。

### 单一事实源
同一事实只存在归属页（people/concepts/decisions/projects），其他页只链接不复制。
改事实只改一处，链接自动指向新内容。

## 工作流

11 个可执行工作流（完整定义见 `AGENTS.example.md`）：
chat-ingest（聊天记录）、ai-chat-ingest（AI 对话）、idea-capture（想法录入）、
idea-review（定期复盘）、journal-ingest（日记）、query（查询）、people-update（人物更新）、
lint（维护）、fragment-processor（碎片加工→多平台草稿）、reference-ingest（资料摄入）、
interview-run（招聘批次管理）。

## 发布纪律

- 发布前脱敏检查（三不写：不写真实薪资/金额、不写真名同事事件、不写未公开内部策略）
- 机械扫描（敏感词正则）+ 子 Agent 语义审核 + 人工终审
- 开源仓库只发布白名单文件，绝不镜像整个 vault
