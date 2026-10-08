---
tags: [system, schema]
---

# Vault 架构

> 这是「一人公司 OS」的参考示例：一个四层架构 + AI 工作流的个人知识库。照搬后按你的主业替换即可。示例中的业务词（电商/运营/平台）均为占位，可整体替换。

本库分四层，LLM（Codex/Claude 等）按此规则读写：

```
_raw/        ← ① 原始输入层（只读，原样保存，一字不改）
_wiki/       ← ② 知识百科层（结构化、长期维护的知识）
_workspace/  ← ③ 工作区（中间产物 → 最终输出：草稿、已发布、查询输出）
_assets/     ← ④ 附件（图片、PDF、截图等二进制文件）
_templates/  ← 笔记软件模板
```

## ① _raw/ — 原始输入

> 核心原则：正文原封不动（一字不改、不分类、不优化措辞）。**允许在文件顶部追加 YAML frontmatter 写入 `raw/{子目录}` 结构性 tag**（既有零散主题 tag 统一加 `raw/` 前缀），但绝不改动正文任何字符。

- LLM 对 raw 文件**只读正文、可加 frontmatter tag**：可补 `raw/{子目录}` 结构性 tag（既有的零散主题 tag 统一加 `raw/` 前缀），但**正文任何字符都不得修改**；新增原始输入按工作流原样落盘后，仅可补 frontmatter tag
- 子目录（示例，按需替换）：`chatlogs/` `副业/` `写作/` `工具使用/` `软件开发/` `招聘面试/` `业务/` `自媒体参考/`（碎片与日记可单独管理，见下方注）
- `招聘面试/历史批次/`：已关闭招聘批次的 JD + 全部原始简历，原样保存，移入后仅可补 frontmatter tag
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
├── 行为记录/             ← 用户确认的高价值行为事实，待提炼/验证
├── 团队经营/             ← 协作者档案、周期性回顾、访谈追问、行动清单（示例结构，不含真实成员信息）
└── interviews/         ← 招聘批次工作区（JD 副本、问题清单、候选人记录、结论、对比）
```

## ④ _assets/ — 附件

> 图片、截图、PDF 等二进制文件。粘贴图片自动存入此目录。

---

## _wiki/ — LLM 维护的结构化知识

所有 wiki 文件用 **YAML frontmatter 标签**归类，不依赖文件夹层级。

### 标签体系（四层树）

笔记软件按标签渲染侧边栏文件夹树。所有标签以四层架构的**层名**为一级前缀，保证树根为 `wiki` / `raw` / `workspace`（`_assets/` 为二进制文件不挂 tag）：

| 一级（层） | 二级 | 三级示例 | 含义 |
|---|---|---|---|
| `wiki` | `concept` | 四层骨架（通用模板，`domain` 可替换为主业）：`#wiki/concept/domain/{主业}`（示例：`ecommerce` 电商）、`/ops/management`（支撑·组织管理）、`/ops/ai`（支撑·AI 与工程）、`/output/business`（输出·商业变现）、`/output/content`（输出·内容与流量）、`/self/personal`（自我·个人哲学）；跨领域页可挂多个 | 概念/方法论 |
| `wiki` | `people` | `#wiki/people/team`、`/tech`、`/self`、`/friend` | 人物 |
| `wiki` | `project` | `#wiki/project/active`、`/done` | 项目 |
| `wiki` | `idea` | `#wiki/idea/seed`、`/growing`、`/evergreen`、`/archived` | 想法（状态流转） |
| `wiki` | `entity` | `#wiki/entity/company`、`/product`、`/position` | 实体/公司/产品/岗位 |
| `wiki` | `decision` | — | 决策（ADR，status: decided/validated） |
| `wiki` | `source` | `#wiki/source/book`、`/article` | 来源摘要 |
| `wiki` | `output` | `#wiki/output/query` | LLM 查询输出 |
| `wiki` | `index` / `log` / `private` | — | 仅 index.md / log.md / 私密内容 |
| `raw` | `{子目录}` | `#raw/业务`、`#raw/软件开发`、`#raw/招聘面试`、`#raw/工具使用`… | 原始文件所在子目录（结构性 tag，每个 raw 文件必带） |
| `raw` | `{主题}` | `#raw/电商`、`#raw/运营`、`#raw/面试`、`#raw/工具`、`#raw/技术`… | raw 文件既有零散主题 tag，统一加 `raw/` 前缀，避免污染顶层 |
| `workspace` | `project` / `fragment` / `output` / `concept` / `platform` … | `#workspace/project/active`、`#workspace/output/query` | 工作区文件，按内容性质加 `workspace/` 前缀 |
| `workspace` | `behavior-record` | `#workspace/behavior-record` | 用户确认的高价值行为记录，按状态提炼、应用和验证 |

### 目录结构（文件级，仅用于物理管理）

```
_wiki/
├── index.md          ← 全局索引（LLM 每次先读这个）
├── log.md            ← 操作日志
├── ideas/            ← slug.md，tag: #wiki/idea + 状态子标签
├── decisions/        ← 决策记录（ADR 风格：背景/选项/选择/理由/验证/认知修正），tag: #wiki/decision
├── people/           ← 人物档案，tag: #wiki/people
├── concepts/         ← 概念页，tag: #wiki/concept；四层骨架子目录（domain/{主业}/ ops/management/ ops/ai/ output/business/ output/content/ self/personal/），domain 层可替换为主业
├── projects/         ← 项目，tag: #wiki/project；项目页可加 `path`（磁盘路径）字段，配一个「机器目录地图」页把库外项目目录登记成索引，让知识库兼任电脑文件导航头
├── sources/          ← 来源摘要，tag: #wiki/source
├── entities/         ← 实体目录（公司/产品/岗位档案），tag: #wiki/entity
└── private/          ← 私密内容，tag: #wiki/private

> 注：迁移到独立子目录的内容（如日记、输出、对话摘要）可按需调整物理位置，标签不变。
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

概念页与人物页的 frontmatter 可加关系字段，给内链赋予语义（本体论轻量版）。**正文「## 关联」区保留**（人读），关系字段为机器可读语义层（Dataview 可查询）。**关系字段直接写在顶层（扁平），每个关系一个字段**——不要用 `relations:` 嵌套对象，否则属性面板会折叠截断、不便检查。

```yaml
source: "[[_raw/...]]"             # 内容来源（原始素材/对话/事件）
derives_from: "[[xxx]]"            # 认知派生自（飞轮演化）
relates_to:                        # 一般关联（默认，可多值）
  - "[[yyy]]"
contradicts: "[[zzz]]"             # 反面/对立（辩证）
feeds_into: "[[www]]"              # 被应用在（输出/落地）
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
| 项目 project | active → done | 子标签 `#wiki/project/active`、`#wiki/project/done` |
| 素材 material | 🧪 实验 → 📝 已写稿 → 🟢 已发布 → ♻️ 复盘 | content-library 条目 emoji 状态 |
| 草稿 draft | draft → published | 移动文件夹（drafts/ → published/）+ frontmatter `status` |
| 岗位 position | open → filled → inactive | frontmatter `status` + tag `#wiki/entity/position` |

派生看板统一在 `_wiki/index.md`，用 Dataview 自动生成，不手写维护。

### 单一事实源（引用不复制）

**同一事实只存在归属页，其他页只链接、不复制描述。**

- 事实归属页：人物 → `people/`，概念 → `concepts/{domain|ops|output|self}/`，决策 → `decisions/`，项目 → `projects/`
- 其他页引用时：只写 `[[链接]]` + 一行角色/关系标签（如「团队成员」「关联概念」），不展开日期、背景、经历等细节
- 例外：`log.md` 操作日志允许带上下文（是流水账不是事实源）；content-library 素材条目允许引用事实（为内容输出服务）
- 修改事实时：只改归属页，其他页不需要动（它们的链接自动指向新内容）

### 命名规范

- 想法：`slug.md`（如 `ai-agent-design.md`）
- 人物：`姓-名.md`（如 `zhang-san.md`）
- 项目：`项目名.md`
- 概念：`概念名.md`
- 岗位：`岗位名.md`
- 日记：`YYYY-MM-DD.md`

---

# 工作流

LLM 必须按以下工作流执行操作：

## 0. kb-onboarding — 冷启动访谈（新用户第一次就跑这个）

触发：用户说「不知道问啥」「不知道问什么」「陪我聊聊」「采访我」「帮我填充知识库」「刚开始用」「grill me」，或刚装完库不知道从何下手
动作：
1. **先跑地图**：`python3 skills/kb-onboarding/scripts/kb_map.py --vault <库根目录>`，拿到三类线索：未闭环线索 / 已有内容延伸 / 空白区
2. **给 3 个选项**，每个必须**一句话能答完**且指向用户自己的真实痕迹；不给开放题、不给通用人生问卷
3. **一次只问一问，每问带推荐答案**（「我猜是 XX，你改一下就行」）——连环炮是本工作流的头号失败模式
4. **能从库里查到的不问**；挖的是「已经在用户脑子里、但从没写下来」的：决策理由、踩过的坑、别人不知道的约束、当时的真实感受
5. **落盘由 agent 决定落点**（原话→`_raw/`、提炼→`_wiki/`、想法→`_wiki/ideas/`、决定→`_wiki/decisions/`），**不让用户学四层结构**
6. **收尾必须回看**：「今天记了什么 + 我下次会记得什么」——缺这一句，用户第三次就弃用
7. 稳态是**被动采集**：日常对话里顺手问「这段要存吗？」（一天最多 2–3 次）

详见 `skills/kb-onboarding/SKILL.md`。

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
3. 提取可复用 prompt/方法 → 写入 `_wiki/concepts/` 四层对应子目录
4. 更新 `_wiki/index.md`
5. 追加 `_wiki/log.md`

## 3. idea-capture — 新想法

触发：用户口述/丢入新想法
动作：
1. 以 seed 状态录入 `_wiki/ideas/slug.md`
2. 加 tag `#wiki/idea/seed`
3. `seed` 状态不进入 index.md（等 growing 才索引入库）

## 4. idea-review — 定期复盘

触发：用户要求复盘或定期触发
动作：
1. 扫描所有 `#wiki/idea/seed` 和 `#wiki/idea/growing`
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
3. 重要答案存入 `_workspace/outputs/`（tag: `#wiki/output/query`）
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
3. 查超 30 天未更新的 `#wiki/idea/seed`
4. 查 `log.md` 表格完整性（多会话并发追加易破损，破损会让 Dataview/预览渲染错乱）：
   - **列粘连**：`grep -Fn '||' _wiki/log.md` —— 4 列表里出现 `||` = 两条记录被挤进同一行，必须拆回两行
   - **列数校验**：`sed 's/\\\\//g; s/\\|//g' _wiki/log.md | awk -F'|' '/^\|/ && NF!=6 {printf "第 %d 行：%d 列（应 4 列）\n", NR, NF-2}'` —— 有输出即破损行（链接里的 `\|` 已先剔除不计；4 列行应得 6 个字段）
   - 修复纪律：只补换行 / 纠正列序（操作=人话任务名、工作流=workflow 名），**不改他人记录的内容**（见核心约束「log 并发写纪律」）
5. 列出问题，等用户确认后处理
6. 追加 `log.md`

## 9. fragment-processor — 每日碎片加工

触发：用户说「处理今天的碎片」或「补草稿」
动作：
1. 读取 `_raw/fragments/YYYY-MM-DD.md`（原始碎片，不改原文件）
2. 识别有价值条目 → 追加到 `_workspace/content-library.md`
3. 按平台适配规则生成草稿 → 输出到 `_workspace/drafts/`
   （以下平台名为占位示例，请替换为你实际运营的平台）
   - 微博：保留原始语气，几乎不加工
   - 小红书：结构化叙事（hook + 正文 + 引导评论）
   - 知乎：扩写技术深度（问题引入 → 背景 → 做法 → 总结）
   - 公众号：完整故事线才触发长文写作
4. 更新 `_wiki/index.md` 草稿区
5. 追加 `_wiki/log.md`

## 10. reference-ingest — 参考资料摄入

触发：用户丢入任何外部参考资料（文章、知乎回答、公众号、视频文稿、GitHub 仓库等）
动作：
1. **价值分级**：🟢高（方法论/观点/经历）→ 全流程；🟡中（工具/平台/数据）→ 仅补 wiki 和存 raw；🔴低 → 跳过
2. **业务问题匹配**：提炼资料解决的具体岗位/流程问题，映射到目标业务场景，区分资料声称能力与本库验证结果
3. **更新现有 wiki**：扫描 _wiki/concepts/ 四层子目录和 _wiki/ideas/，用新内容补充或佐证已有页面；工具/平台类条目默认进「待观望」表，实际安装后才转正
4. **提取概念与验证记录**：概念页补充输入、输出、边界、验证状态和来源
5. **提取素材**：按认知升级/方法论/行业观察/踩坑复盘/技能干货/知识库案例分类 → _workspace/content-library.md；具备验证证据的条目补充交付物、适用对象、转化承接物和 CTA
6. **原样保存** → 按内容语义选 _raw/ 子目录，文件名跟随库内同类文件既有格式，不固定日期前缀；GitHub 仓库用 gh api 抓 README 原文
7. 更新 index.md 和 log.md；报告中列出业务问题、验证状态、知识库落点和内容/产品机会

## 10.5. content-benchmark-analysis — 内容对标拆解

触发：用户要求拆解高赞文章、研究账号转化、寻找平台对标内容。

动作：先定目标产品和用户 → 记录公开互动与转化信号 → 评分研究优先级 → 拆内容结构、信任证据和转化路径 → 用本库素材重做原创内容。

边界：公开信号只能说明转化潜力，不证明真实成交；不复制原文、图片、独特案例、数据或专有框架。完整拆解存 `_workspace/content-benchmarks/`，Fragment Processor 只读取结构功能、证据类型和 CTA 逻辑。

技能：`skills/content-benchmark-analysis/SKILL.md`；模板：`_templates/内容对标拆解模板.md`。



触发：用户提供 JD 或说「开始一轮招聘」
动作：
1. **建档**：从 JD 提取岗位名和批次，创建 `_workspace/interviews/{岗位}-{批次}/`，原始 JD 原样存为 `00-JD.md`；批次命名如 `运营-2026Q1-国内`
2. **生成问题清单**：读取 `_raw/招聘面试/{岗位}面试考察.md`、面试方法参考和 wiki 业务上下文，生成 `01-问题清单.md`，包含问题 ID、考察维度、优先级、建议追问、判断证据
3. **录入简历**：每份简历原样存入 `候选人/{姓名}/`，生成 `简历摘要.md`，区分简历事实与待验证信息
4. **面试记录**：每次输入回答后更新 `候选人/{姓名}/面试记录.md`，标记已覆盖问题、关键证据、需要追问的问题
5. **候选人结论**：面试结束后生成 `候选人/{姓名}/结论.md`，包含证据、评分、风险、录用建议、入职注意点
6. **批次对比**：同一 JD 多候选人完成后生成 `02-对比.md`，按同一套维度对比并给出推荐
7. **归档**：有人入职或批次关闭后，将 `00-JD.md` 和全部原始简历移入 `_raw/招聘面试/历史批次/{岗位}-{批次}/`，移入后不再修改
8. **知识沉淀**：更新 `_wiki/entities/{岗位}.md`（tag: `#wiki/entity/position`）任职记录、人物页链接、`index.md`、`log.md`

---

## 13. weekly-operating-review — 每周经营访谈

触发：成员提交每周经营复盘周报，或管理者要求生成某成员的经营访谈问题。

动作：
1. 先读成员 Profile、本周周报、上周访谈/行动、近期行为记录和对应业务目标。
2. 基于证据缺口、异常、未闭环动作和历史待验证能力生成专属追问；已充分证明的内容不重复问。
3. 访谈前明确告知录音/转写用途并取得同意；不同意则使用现场笔记。
4. 访谈后导入转写，按追问清单逐题记录回答、事实、证据强度、存疑，并区分成员没说清楚与管理者没问好。
5. 生成下周行动清单，必须包含动作、负责人、截止时间和验收标准；成员与管理者共同确认。
6. 单次异常不直接更新人物定位；连续 4—6 周证据或足以改变管理决策的重大结果，才更新成员 Profile/人物页的管理判断。
7. 高价值、可复用行为经用户确认后才进入 behavior-record；不把员工隐私、薪资和真实业务细节带入公开内容。

模板：`_templates/成员经营档案模板.md`、`_templates/每周经营复盘周报模板.md`、`_templates/每周经营访谈追问清单模板.md`、`_templates/每周经营访谈记录模板.md`。详见相关经营复盘方法页。

---

## 14. behavior-record — 高价值行为记录与提炼

触发：用户明确说「记录这个」「记录刚才的行为」「这次失败值得沉淀」「把验证结果入库」；会话结束只对明确决策、事实修正、验证结果、失败教训或可复用流程提示候选，用户确认后才创建。

动作：
1. 只记录高价值行为，不全量记录普通搜索、排版、重复测试、草稿生成或自动备份。
2. 将行为、结果和证据记录在工作区，区分事实与判断。
3. 提炼为知识、决策、行动或验证候选，用户确认后回写唯一归属页。
4. 经过真实验证后更新状态；保留原记录，不把临时注入状态当长期事实。


- **隐私边界**：`_wiki/private/` 和 tag `#wiki/private` 的内容仅在用户明确查询时提及，不主动引用
- **不删页**：过期内容归档（改 tag 为 `#wiki/idea/archived`），不删除文件
- **raw 正文只读**：`_raw/` 文件**正文绝不修改、不编辑**；但**允许追加 frontmatter tag**（每个文件补 `raw/{子目录}`，既有的零散主题 tag 统一加 `raw/` 前缀）。新增原始输入按工作流原样落盘后，仅可补 frontmatter tag
- **引用格式**：统一用 `[[路径|显示名]]` 内链
- **双维护**：每次操作后同步更新 `index.md` 和 `log.md`
- **行为记录边界**：不全量自动记录普通操作；会话结束候选需用户确认；行为记录经过提炼和验证后才升级为长期知识；不写入临时注入轨
- **不跨库**：不与其他笔记库交叉引用
- **多会话并发是常态，不是异常**：本库由多个会话同时读写，`log.md` 和工作区里出现**别的会话写入的记录属正常现象**，不是冲突信号。**不要为此向用户汇报**（「发现另一个会话在写…」这类顺带通知一律不发）。只在真会造成损害时才提：① 要改的**同一行/同一段**正被另一个会话同时改写（有覆盖风险）；② 数据完整性问题（重复建档、表格列数破损、凭据外泄）；③ 自己的写入被别人覆盖或回滚
- **log 并发写纪律**：`_wiki/log.md` 只**追加**自己本次操作的行；**不删除任何既有 log 记录**（包括别的会话写的）；**只创建、只修改自己写入的那条**（更正自己先前的记录可原位改写，也可追加「修正」行；绝不动别人的行）。保持 4 列表格（日期 / 操作 / 工作流 / 详情），表格内链接的竖线写 `[[路径\|显示名]]`
- **架构同步**：任何架构变更（目录增删、层级调整、工作流新增/修改/删除）后，必须同步更新本文件里的架构描述、工作流定义和路径引用，保持一致。

---

# 工作流示例

## chat-ingest 示例

**输入**：
```
[微信聊天记录]
张三：那个店铺的 API key 过期了，要更新
我：好的，明天处理
张三：另外发货模板要加个新站点
```

**输出**：
- 更新 `_wiki/people/zhang-san.md`：追加互动记录
- 在 `_wiki/ideas/` 新建 `api-key-renewal.md`（状态 seed）
- 在 `_wiki/concepts/domain/{主业}/` 更新或新建 `发货模板.md`
- 更新 `index.md` 相关索引
- `log.md` 追加：`2026-07-10 | chat-ingest | 处理张三微信记录，提取2条待办`

## ai-chat-ingest 示例

**输入**：用户丢入 Claude 对话导出（包含一段关于"如何优化笔记工作流"的讨论）

**输出**：
- `_raw/chatlogs/note-workflow-discussion.md`：摘要
- `_wiki/concepts/ops/ai/ai-vault-workflow.md`：提取的可复用 prompt/方法
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
[[_raw/笔记工作流.md]]
```

## idea-review 示例

**输入**："帮我复盘一下最近的想法"

**动作**：
1. 扫描 `#wiki/idea/seed` → 列出：`auto-tagging-with-ai.md`（30 天未更新）
2. 扫描 `#wiki/idea/growing` → 列出：`ai-vault-workflow.md`（活跃）
3. 建议：
   - `auto-tagging-with-ai.md`：归档（太久未更新）
   - `ai-vault-workflow.md`：升级到 evergreen
4. 用户确认后执行

## query 示例

**输入**："我们之前讨论过发货模板的问题吗？"

**动作**：
1. 先读 `_wiki/index.md`
2. 查标签 `#wiki/concept` 和 `_wiki/concepts/` 四层子目录
3. 查 `_raw/` 下含"发货"、"模板"的笔记
4. 汇总结果存入 `_workspace/outputs/shipping-template-query-2026-07-10.md`
5. `log.md` 追加记录

## lint 示例

**输入**："检查一下笔记库有没有问题"

**输出**（列表，等用户确认）：
- 孤立页：`_wiki/ideas/old-idea.md`（无任何内链指向）
- 断链：`[[不存在的页面]]` 在 `_wiki/concepts/ops/ai/some-concept.md`
- 超 30 天 seed：`_wiki/ideas/auto-tagging-with-ai.md`

---

# 已安装插件

## 首页与新用户上手
- 默认首页 `Home.md` 仅保留记录一下、做一件事、继续上次、回头看四模块；分类总览留在知识索引，随机漫游不属于默认首页。
- 固定入口仅在能力变化时维护；动态列表通过 Dataview 查询原文件状态与待办，不逐次复制事实台账。Homepage 仅负责启动打开首页，可不安装；无插件仍可阅读固定入口与 Demo。
- 新用户先安装 Obsidian（已有则跳过）、下载并打开知识库、阅读首页与虚构 Demo，再按需启用 Dataview 和 Homepage。详细步骤见 `docs/install.md`；模板需 Templater 或手动/AI 填值。
- 下载仓库不自动安装插件或加载 AI 技能。AI 辅助安装需明确授权，用户确认信任与启用；文件准备、插件启用、实际界面验收分别报告。不得覆盖已有库或插件配置。
- `demos/ecommerce-hiring/` 是自包含虚构教学材料，不进入真实候选人档案、待办或经营统计。发布首页须用泛化副本，不复制私人首页或 `.obsidian` 配置。

以下插件已配置，LLM 必须了解其用法（示例为 Obsidian 生态）：

## Templater
- 模板引擎，替代核心模板
- 语法：`<% tp.date.now("YYYY-MM-DD") %>`、`<% tp.file.title %>`
- 所有 `_templates/` 下的模板均使用 Templater 语法
- 新建 wiki 文件时，从对应模板创建

## Tasks
- 任务管理，用 `- [ ]`、`- [x]` 标记
- 可用于 `_wiki/log.md` 追踪待办
- 可用 Dataview 查询：`TASK FROM #wiki/project`

## Advanced Tables
- 增强表格编辑（Tab 对齐、自动格式化）
- LLM 写 Markdown 表格时无需特殊处理，插件自动美化

## Tag Wrangler
- 批量重命名、合并标签
- 用法：需要将所有 `#wiki/idea/seed` 升级为 `#wiki/idea/growing` 时使用
- LLM 执行 idea-review 时，确认升级后操作标签

## TagFolder
- 将 YAML 标签显示为侧边栏文件夹树
- LLM 无需操作，标签打对了自动分类

## Git
- 自动备份笔记库到 Git
- LLM 不操作 git，由插件自动处理
- 建议配置：每 30 分钟自动 commit + push

---

# 团队技能（Skills）登记

团队自定义技能安装在本机技能目录（如 `~/.codex/skills/`），LLM 通过 SKILL.md 自动加载。此表按需登记：

| 技能 | 位置 | 用途 |
|---|---|---|
| （在此登记） | `~/.codex/skills/{技能名}/` | 一句话说明触发时机与作用 |

> 原则：每个技能一个目录 + 一份 SKILL.md；「一次触发、一次产出」的技能才值得沉淀为 skill，用完即弃的一次性操作不建 skill。

---

# 运行环境

- 命令前缀约定（可选）：如本地工具压缩命令输出以减少 LLM token 消耗，可在本文档登记并统一使用
- 例：`<前缀> git status`、`<前缀> pytest -q`

---

> 本文件是公开参考示例，作为个人/团队知识库的架构模板；实际部署时替换为你的主业、技能与工具约定。
