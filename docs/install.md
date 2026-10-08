# 安装与上手指南 / Installation guide

## 先分清三样东西

- 知识库文件：Markdown、模板和 Demo；下载仓库不会自动安装 Obsidian 或插件。
- Dataview：动态查询增强；没装时仍能阅读首页指令与 Demo，但查询代码不会变成列表。
- Homepage：可选的启动入口；不安装也能手动打开 `Home.md`。

当前没有一键安装器。本指南的 AI 辅助步骤需要用户授权、本机文件权限与网络；文件准备完成不等于插件启用或界面验收通过。

## A. 先体验，不安装插件

1. 从 https://obsidian.md/download 安装 Obsidian；已安装则跳过。
2. 从 https://github.com/shiningjohci/opc-os 选择 Code → Download ZIP，解压；或执行：

```sh
git clone https://github.com/shiningjohci/opc-os.git
```

3. Obsidian → 打开文件夹作为仓库，选择解压后包含 `Home.md` 的目录，而不是外面的压缩包目录。
4. 在文件列表打开 `Home.md`，使用阅读视图；按首页链接进入 `demos/ecommerce-hiring/00-从这里开始.md`。
5. 按顺序看岗位→简历→证据缺口→追问回填→结论。全部为虚构，不作为真实招聘材料。

GitHub 网页可能不解析 Demo 内的 Obsidian 双链；请在 Obsidian 阅读。仅阅读 Demo 不需要 AI、Git、Python 或社区插件。

## B. 准备自己的工作区

体验库没有私人笔记。准备实际使用时，可在这个新库里新建 `_raw`、`_wiki`、`_workspace`、`_assets`、`_templates` 文件夹；将需要的 `templates/` 模板复制到 `_templates/`。目录为空时动态列表没有内容是正常的。

先读 `docs/AGENTS.example.md`。若希望本机 AI 自动读取仓库规则，可在这个新库中把它复制为根目录 `AGENTS.md`；不得覆盖已有规则。模板中的 Templater 表达式需要另装并启用 Templater，或由 AI/用户填成实际值，不能把表达式当已生成内容。

把具体材料交给具备文件权限的 AI，明确指定此库根目录，并要求先读规则、只在获授权的范围内写入。技能文件随仓库提供，但不同 AI 宿主的技能加载方式不同；克隆文件不等于技能已安装或会自动触发。普通聊天网页不能默认访问本机文件，可手动提供规则和相关材料。

## C. 按需启用动态首页

Obsidian → 设置 → 第三方插件（Community plugins）→ 确认启用社区插件 → 浏览 → 搜索 **Dataview** → 安装 → 启用。

打开 `Home.md` 的阅读视图。“继续上次”“回头看”应显示列表或空结果，而不是原始查询代码。首页只使用普通 Dataview 查询，不要求开启 JavaScript 查询。

可用下面的临时测试笔记验证：在 `_workspace/首页测试.md` 写入：

```markdown
---
status: active
---
# 首页测试
- [ ] 核对首页动态列表
```

该笔记应进入“继续上次”，待办应进入“回头看”。勾选待办后应从未完成列表消失；测试结束后自行删除这份临时测试笔记。近期工作列表按修改时间排序，不是上次聊天恢复，也不是未完成证明。

## D. 可选：启动时自动打开首页

按同样方式安装并启用 **Homepage**，在其设置中选择首页文件 `Home`，打开启动时显示首页的选项。重启或重新打开仓库，检查是否自动进入首页。

已有库不要覆盖 `.obsidian` 配置；沿用已有首页文件名即可。例如原首页叫 `Home🏠`，配置应指向该文件，不必改名。

## E. 让 AI 辅助准备（不是默认自动安装）

可把下面指令交给有本机工具的 AI，先填入目标路径：

> 请把 OPC-OS 准备在我指定的目标目录。先检查目录是否存在、是否已有知识库；不覆盖同名文件，不复制其他人的笔记或插件配置。下载后检查首页、指南与六份 Demo 链接。按需创建四层空目录，准备模板和规则。先只完成文件准备；安装第三方插件前，告诉我来源、版本、许可和修改范围并等待授权。确认后可从官方社区插件登记对应的仓库下载所需运行文件到目标库插件目录，保留现有配置；不要静默启用插件或替我确认信任。最后分别报告文件准备、插件启用和 Obsidian 实际显示验证是否完成。

AI 可以辅助放置插件的 `manifest.json`、`main.js` 和必要的 `styles.css`，但需要核对插件 ID、版本与兼容性，并从可信来源获取；不要执行未知安装脚本。用户在 Obsidian 确认信任与启用。没有权限或网络时改用手动步骤，不凭空宣布成功。

## 验收与排障

- 首页找不到：检查打开的根目录、文件是否确实叫 `Home.md`。
- Demo 链接不通：保留整个 `demos/ecommerce-hiring/` 目录，不只复制导读。
- 查询显示代码：检查 Dataview 是否安装并启用、笔记是否处于阅读视图；必要时重新打开笔记。
- 列表为空：先确认 `_workspace` 是否有符合条件的文件；空库和被排除的演示材料不会显示。
- 启动未进首页：检查 Homepage 的目标文件和启动开关。
- 切换到已有库：先备份，仅复制选定文件；不整包覆盖配置，不重复建立同一事实的副本。

首页固定“记录/做事”入口只在能力变化时更新；“继续/回顾”读取原文件，不另抄一份台账。默认首页只保留四模块，想法总览等放索引，随机漫游不是默认功能。

安全说明：https://help.obsidian.md/community-plugins

## English quick path

Install Obsidian if needed → download and extract OPC-OS → open the folder containing `Home.md` as a vault → read the fictional hiring demo. No plugin is needed for static reading. Enable Dataview for dynamic lists; Homepage is optional for opening the home note on startup. Create the four-layer empty folders and copy selected templates before real use. Templater expressions require Templater or manual/AI substitution. AI assistance requires explicit scope and permissions; downloading a repository does not install plugins, load AI skills, or approve third-party code. Never overwrite an existing vault or its plugin settings. Verify file preparation, plugin enablement and actual UI behavior separately.
