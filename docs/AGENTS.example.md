---
tags: [system, schema]
---

# Vault 架构

本库分四层，LLM（Codex）按此规则读写：

```
_raw/        ← ① 原始输入层（只读，原样保存，一字不改）
_wiki/       ← ② 知识百科层（结构化、长期维护的知识）
_workspace/  ← ③ 工作区（中间产物 → 最终输出：草稿、已发布、查询输出）
_assets/     ← ④ 附件（图片、PDF、截图等二进制文件）
_templates/  ← Obsidian 模板
```

## ① _raw/ — 原始输入

> 核心原则：原封不动地存，一字不改。不加 frontmatter，不分类，不优化措辞。

- LLM 只读，**绝不修改任何文件**
- 子目录：`chat/` `一人公司/` `写书/` `工具使用/` `软件开发/` `招聘面试/` `电商运营/` `自媒体参考/` `fragments/` `journal/` `chatlogs/` + 平铺 .md
- `招聘面试/历史批次/`：已关闭招聘批次的 JD + 全部原始简历，原样保存，移入后不再修改
- `fragments/`：每日碎碎念原始记录，纯文本 dump
- `journal/`：日记录入，原汁原味转写
- `chatlogs/`：AI 对话导出摘要
- 引用格式：`[[_raw/子目录/文件名|显示名]]`

## ② _wiki/ — 知识百科

> 提炼过的、结构化的、长期维护的知识。像维基百科，只存「成品知识」。

## ③ _workspace/ — 工作区

> 内容的「生产线」。中间产物 → 最终输出。

```
_workspace/
├── content-library.md  ← 素材库（选题 → 状态 → 输出追踪）
├── fragments/          ← 待加工的每日碎片副本
├── drafts/             ← 待发草稿（各平台适配稿）
├── published/          ← 已发布内容
├── outputs/            ← 查询输出
└── interviews/         ← 招聘批次工作区（JD 副本、问题清单、候选人记录、结论、对比）
```

## ④ _assets/ — 附件

> 图片、截图、PDF 等二进制文件。Obsidian 粘贴图片自动存入此目录。

---

## _wiki/ — LLM 维护的结构化知识

所有 wiki 文件用 **YAML frontmatter 标签**归类，不依赖文件夹层级。

### 标签体系

| 主标签 | 含义 | 子标签示例 |
|---|---|---|
| `#index` | 全局索引（仅 index.md） | — |
| `#log` | 操作日志（仅 log.md） | — |
| `#journal` | 日记 | `#journal/2026` |
| `#idea` | 想法 | `#idea/seed`, `#idea/growing`, `#idea/evergreen`, `#idea/archived` |
| `#decision` | 决策记录（ADR 风格） | `#decision`（状态用 frontmatter status: decided/validated） |
| `#people` | 人物 | `#people/tech`, `#people/friend` |
| `#concept` | 概念/方法论 | `#concept/ai`, `#concept/business` |
| `#project` | 项目 | `#project/active`, `#project/done` |
| `#source` | 来源摘要 | `#source/book`, `#source/article` |
| `#output` | LLM 查询输出 | `#output/query` |
| `#entity` | 实体/产品/公司/岗位 | `#entity/company`, `#entity/product`, `#entity/position` |
| `#private` | 私密（仅在明确查询时引用） | — |

### 目录结构（文件级，仅用于物理管理）

```
_wiki/
├── index.md          ← 全局索引（LLM 每次先读这个）
├── log.md            ← 操作日志
├── ideas/            ← slug.md，tag: #idea + 状态子标签
├── decisions/        ← 决策记录（ADR 风格：背景/选项/选择/理由/验证/认知修正），tag: #decision
├── people/           ← 人物档案，tag: #people
├── concepts/         ← 概念页，tag: #concept
├── projects/         ← 项目，tag: #project
├── sources/          ← 来源摘要，tag: #source
├── entities/         ← 实体目录（公司/产品/岗位档案），tag: #entity
└── private/          ← 私密内容，tag: #private

> 注：`journal/` `outputs/` `chatlogs/` 已分别迁至 `_raw/journal/` `_workspace/outputs/` `_raw/chatlogs/`
```

### Frontmatter 规范

每个 wiki 文件头部必须包含：

```yaml
---
tags: [tag1, tag2]
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: seed|growing|evergreen  # 仅 ideas/ 需要
---
```

### 链接类型化规范（relations 字段）

概念页与人物页的 frontmatter 可加 `relations` 字段，给内链赋予语义（Palantir 本体论轻量版）。**正文「## 关联」区保留**（人读），relations 为机器可读语义层（Dataview 可查询）。

```yaml
relations:
  source: "[[_raw/...]]"           # 内容来源（原始素材/对话/事件）
  derives_from: "[[xxx]]"          # 认知派生自（飞轮演化）
  relates_to:                      # 一般关联（默认）
    - "[[yyy]]"
  contradicts: "[[zzz]]"           # 反面/对立（辩证）
  feeds_into: "[[www]]"            # 被应用在（输出/落地）
```

关系词表（5 个，不再增加）：

| 关系 | 含义 | 示例 |
|---|---|---|
| `source` | 内容来源 | 概念页 ← 某次对话/raw 素材 |
| `derives_from` | 认知派生自 | 复盘清单 ← 方法论 |
| `relates_to` | 一般关联 | 任何平级关联 |
| `contradicts` | 反面/对立 | 辩证记录 |
| `feeds_into` | 被应用在 | 哲学 → 变现策略 |

只给**概念页和人物页**加；素材条目（content-library）暂不适用。新文件按需加，旧文件试点页已迁移（见 log）。

### 状态流转图（对象生命周期）

每个对象类型有固定生命周期，状态变更时按此流转：

| 对象 | 状态流 | 状态存放位置 |
|---|---|---|
| 想法 idea | seed → growing → evergreen → archived | frontmatter `status` |
| 决策 decision | decided → validated | frontmatter `status` |
| 项目 project | active → done | 子标签 `#project/active`、`#project/done` |
| 素材 material | 🧪 实验 → 📝 已写稿 → 🟢 已发布 → ♻️ 复盘 | content-library 条目 emoji 状态 |
| 草稿 draft | draft → published | 移动文件夹（drafts/ → published/）+ frontmatter `status` |
| 岗位 position | open → filled → inactive | frontmatter `status` + tag `#entity/position` |

派生看板统一在 `_wiki/index.md`，用 Dataview 自动生成，不手写维护。

### 单一事实源（引用不复制）

**同一事实只存在归属页，其他页只链接、不复制描述。**

- 事实归属页：人物 → `people/`，概念 → `concepts/`，决策 → `decisions/`，项目 → `projects/`
- 其他页引用时：只写 `[[链接]]` + 一行角色/关系标签（如「团队成员」「关联概念」），不展开日期、背景、经历等细节
- 例外：`log.md` 操作日志允许带上下文（是流水账不是事实源）；content-library 素材条目允许引用事实（为内容输出服务）
- 修改事实时：只改归属页，其他页不需要动（它们的链接自动指向新内容）

### 命名规范

- 想法：`slug.md`（如 `ai-agent-design.md`）
- 人物：`姓-名.md`（如 `zhang-san.md`）
- 项目：`项目名.md`
- 概念：`概念名.md`
- 岗位：`岗位名.md`（如 `TT运营.md`）
- 日记：`YYYY-MM-DD.md`

---

# 工作流

LLM 必须按以下工作流执行操作：

## 1. chat-ingest — 处理微信原始记录

触发：用户丢入微信聊天记录（`_raw/chat/`）
动作：
1. 原样保存到 `_raw/chat/`
2. 提取决定、待办、重要信息
3. 更新相关人物页（`_wiki/people/`）
4. 有价值素材 → `_workspace/content-library.md`
5. 更新 `_wiki/index.md` 相关索引
6. 追加 `_wiki/log.md` 操作记录

## 2. ai-chat-ingest — 处理 AI 对话导出

触发：用户丢入 Claude/ChatGPT 导出（`_raw/claude/`、`_raw/chatgpt/`）
动作：
1. 原样保存到 `_raw/chatlogs/`
2. 识别主题，写入 `_raw/chatlogs/` 摘要
3. 提取可复用 prompt/方法 → 写入 `_wiki/concepts/`
4. 更新 `_wiki/index.md`
5. 追加 `_wiki/log.md`

## 3. idea-capture — 新想法

触发：用户口述/丢入新想法
动作：
1. 以 seed 状态录入 `_wiki/ideas/slug.md`
2. 加 tag `#idea/seed`
3. `seed` 状态不进入 index.md（等 growing 才索引入库）

## 4. idea-review — 定期复盘

触发：用户要求复盘或定期触发
动作：
1. 扫描所有 `#idea/seed` 和 `#idea/growing`
2. 建议：合并、升级到 evergreen、或归档
3. 只对用户确认的执行状态变更
4. 更新 `index.md` 和 `log.md`

## 5. journal-ingest — 日记录入

触发：用户口述/丢入当日记录
动作：
1. 原样写入 `_raw/journal/YYYY-MM-DD.md`（纯文本，不加 frontmatter）
2. 原汁原味转写，不做 AI 分析
3. 如果用户要求提取，再走 idea-capture 流程
4. 追加 `_wiki/log.md`

## 6. query — 查询知识库

触发：用户提问
动作：
1. **先读** `_wiki/index.md` 了解知识结构
2. 根据问题定位相关 wiki 页和 _raw/ 素材
3. 重要答案存入 `_workspace/outputs/`（tag: `#output/query`）
4. 追加 `log.md`

## 7. people-update — 发现人物信息

触发：在任何对话/素材中发现人物信息
动作：
1. 创建或更新 `_wiki/people/` 中的人物档案
2. 更新 `index.md` 的人物索引区
3. 追加 `log.md`

## 8. lint — 维护

触发：用户要求或定期检查
动作：
1. 查孤立页（没有内链指向的页面）
2. 查断链（指向不存在文件的链接）
3. 查超 30 天未更新的 `#idea/seed`
4. 列出问题，等用户确认后处理
5. 追加 `log.md`


## 9. fragment-processor — 每日碎片加工

触发：用户说「处理今天的碎片」或「补草稿」
动作：
1. 读取 `_raw/fragments/YYYY-MM-DD.md`（原始碎片，不改原文件）
2. 识别有价值条目 → 追加到 `_workspace/content-library.md`
3. 按平台适配规则生成草稿 → 输出到 `_workspace/drafts/`
   - 微博：保留原始语气，几乎不加工
   - 小红书：结构化叙事（hook + 正文 + 引导评论）
   - 知乎：扩写技术深度（问题引入 → 背景 → 做法 → 总结）
   - 公众号：完整故事线才触发 khazix-writer
4. 更新 `_wiki/index.md` 草稿区
5. 追加 `_wiki/log.md`


## 10. reference-ingest — 参考资料摄入

触发：用户丢入任何外部参考资料（文章、知乎回答、公众号、视频文稿等）
动作：
1. **价值分级**：🟢高（方法论/观点/经历）→ 全流程；🟡中（工具/平台/数据）→ 仅补 wiki 和存 raw；🔴低 → 跳过
2. **更新现有 wiki**：扫描 _wiki/concepts/ 和 _wiki/ideas/，用新内容补充或佐证已有页面
3. **提取概念**：提炼可跨领域应用的概念 → _wiki/concepts/{slug}.md
4. **提取素材**：按认知升级/方法论/行业观察/踩坑复盘/技能干货分类 → _workspace/content-library.md
5. **原样保存** → _raw/自媒体参考/（不加 frontmatter）
6. 更新 index.md 和 log.md

详见 `skills/reference-ingest/SKILL.md`。

## 11. interview-run — 招聘批次工作流

触发：用户提供 JD 或说「开始一轮招聘」
动作：
1. **建档**：从 JD 提取岗位名和批次，创建 `_workspace/interviews/{岗位}-{批次}/`，原始 JD 原样存为 `00-JD.md`；批次命名如 `TT运营-2026Q3-越南`
2. **生成问题清单**：读取 `_raw/招聘面试/{岗位}面试考察.md`、`_raw/工具使用/面试方法.md` 和 wiki 业务上下文，生成 `01-问题清单.md`，包含问题 ID、考察维度、优先级、建议追问、判断证据
3. **录入简历**：每份简历原样存入 `候选人/{姓名}/`，生成 `简历摘要.md`，区分简历事实与待验证信息
4. **面试记录**：每次输入回答后更新 `候选人/{姓名}/面试记录.md`，标记已覆盖问题、关键证据、需要追问的问题
5. **候选人结论**：面试结束后生成 `候选人/{姓名}/结论.md`，包含证据、评分、风险、录用建议、入职注意点
6. **批次对比**：同一 JD 多候选人完成后生成 `02-对比.md`，按同一套维度对比并给出推荐
7. **归档**：有人入职或批次关闭后，将 `00-JD.md` 和全部原始简历移入 `_raw/招聘面试/历史批次/{岗位}-{批次}/`，移入后不再修改
8. **知识沉淀**：更新 `_wiki/entities/{岗位}.md`（tag: `#entity/position`）任职记录、人物页链接、`index.md`、`log.md`

模板：`_templates/岗位档案模板.md`、`_templates/面试问题清单模板.md`、`_templates/简历摘要模板.md`、`_templates/候选人面试记录模板.md`、`_templates/候选人结论模板.md`、`_templates/候选人对比模板.md`

---

# 核心约束

- **隐私边界**：`_wiki/private/` 和 tag `#private` 的内容仅在用户明确查询时提及，不主动引用
- **不删页**：过期内容归档（改 tag 为 `#idea/archived`），不删除文件
- **raw 只读**：已有 `_raw/` 文件绝不修改；新原始输入（含招聘归档）按工作流原样落盘后不再修改
- **引用格式**：统一用 `[[路径|显示名]]` 内链
- **双维护**：每次操作后同步更新 `index.md` 和 `log.md`
- **不跨库**：不与其他 Obsidian vault 交叉引用
- **AGENTS 同步**：任何架构变更（目录增删、层级调整、工作流新增/修改/删除）后，必须同步更新 AGENTS.md 里的架构描述、工作流定义和路径引用，保持一致。

---

# 工作流示例

## chat-ingest 示例

**输入**：
```
[微信聊天记录]
张三：那个 Shopee 店铺的 API key 过期了，要更新
我：好的，明天处理
张三：另外发货模板要加个新站点
```

**输出**：
- 更新 `_wiki/people/zhang-san.md`：追加互动记录
- 在 `_wiki/ideas/` 新建 `shopee-api-key-renewal.md`（状态 seed）
- 在 `_wiki/concepts/` 更新或新建 `发货模板.md`
- 更新 `index.md` 相关索引
- `log.md` 追加：`2026-07-10 | chat-ingest | 处理张三微信记录，提取2条待办`

## ai-chat-ingest 示例

**输入**：用户丢入 Claude 对话导出（包含一段关于"如何优化 Obsidian 工作流"的讨论）

**输出**：
- `_raw/chatlogs/obsidian-workflow-discussion.md`：摘要
- `_wiki/concepts/ai-vault-workflow.md`：提取的可复用 prompt/方法
- 更新 `index.md` 概念区
- `log.md` 追加记录

## idea-capture 示例

**输入**："我感觉可以用 AI 自动给我的笔记打标签"

**输出**（`_wiki/ideas/auto-tagging-with-ai.md`）：
```yaml
---
tags: [idea/seed]
created: 2026-07-10
updated: 2026-07-10
status: seed
---
# AI 自动打标签
## 核心想法
用 LLM 读取笔记内容，自动生成合适的 YAML 标签。
## 关联
[[_raw/LLM Wiki 工作流.md]]
```

## idea-review 示例

**输入**："帮我复盘一下最近的想法"

**动作**：
1. 扫描 `#idea/seed` → 列出：`auto-tagging-with-ai.md`（30 天未更新）
2. 扫描 `#idea/growing` → 列出：`obsidian-ai-vault.md`（活跃）
3. 建议：
   - `auto-tagging-with-ai.md`：归档（太久未更新）
   - `obsidian-ai-vault.md`：升级到 evergreen
4. 用户确认后执行

## query 示例

**输入**："我们之前讨论过 Shopee 发货模板的问题吗？"

**动作**：
1. 先读 `_wiki/index.md`
2. 查标签 `#concept` 和 `_wiki/concepts/`
3. 查 `_raw/` 下含"发货"、"Shopee"的笔记
4. 汇总结果存入 `_workspace/outputs/shopee-shipping-query-2026-07-10.md`
5. `log.md` 追加记录

## lint 示例

**输入**："检查一下 vault 有没有问题"

**输出**（列表，等用户确认）：
- 孤立页：`_wiki/ideas/old-idea.md`（无任何内链指向）
- 断链：`[[不存在的页面]]` 在 `_wiki/concepts/some-concept.md`
- 超 30 天 seed：`_wiki/ideas/auto-tagging-with-ai.md`

---

# 已安装插件

以下插件已配置，LLM 必须了解其用法：

## Templater
- 模板引擎，替代 Obsidian 核心模板
- 语法：`<% tp.date.now("YYYY-MM-DD") %>`、`<% tp.file.title %>`
- 所有 `_templates/` 下的模板均使用 Templater 语法
- 新建 wiki 文件时，从对应模板创建

## Tasks
- 任务管理，用 `- [ ]`、`- [x]` 标记
- 可用于 `_wiki/log.md` 追踪待办
- 可用 Dataview 查询：`TASK FROM #project`

## Advanced Tables
- 增强表格编辑（Tab 对齐、自动格式化）
- LLM 写 Markdown 表格时无需特殊处理，插件自动美化

## Tag Wrangler
- 批量重命名、合并标签
- 用法：需要将所有 `#idea/seed` 升级为 `#idea/growing` 时使用
- LLM 执行 idea-review 时，确认升级后操作标签

## TagFolder
- 将 YAML 标签显示为侧边栏文件夹树
- 配置根目录：`_wiki/`
- LLM 无需操作，标签打对了自动分类

## Git
- 自动备份 vault 到 Git
- LLM 不操作 git，由插件自动处理
- 建议配置：每 30 分钟自动 commit + push

---

# Codex 技能（Skills）

以下技能安装在本机 `~/.codex/skills/`，Codex 通过 SKILL.md 自动加载：

| 技能 | 位置 | 用途 |
|---|---|---|
| `fragment-processor` | `~/.codex/skills/fragment-processor/` | 每日碎片加工（读取 _raw/fragments/ → 生成各平台草稿到 _workspace/drafts/） |
| `xiaohongshu-cli` | `~/.codex/skills/xiaohongshu-cli/` | 小红书 CLI，支持发笔记（`xhs post`） |
| `zhihu-cli` | `~/.codex/skills/zhihu-cli/` | 知乎 CLI，支持发文章/想法/提问 |
| `khazix-writer` | `~/.codex/skills/khazix-writer/` | 公众号长文写作（完整故事线才触发） |

> 注：`weibo-cli` 已装但仅支持只读（热搜/搜索/用户），不发帖。

---

# 运行环境

- 所有 shell 命令前缀 `rtk`（Rust Token Killer），减少 token 消耗
- 例：`rtk git status`、`rtk pytest -q`
