# 从这里开始 / Start here

> 固定入口随文件提供；动态列表由 Dataview 读取原文件，不需要 AI 每次重写首页。手动打开本页不需要 Homepage 插件。安装与初始化见 [安装指南](docs/install.md)，规则见 [知识库操作手册](docs/AGENTS.example.md)。

## ① 记录一下

复制一句话给 AI，并附上材料、明确目标库：
- 碎片：「先原样记录这些碎片，不加工。」
- 资料：「判断这份资料的可用价值，先给建议，不直接入库。」
- 想法：「把这个想法记为 seed，区分原话与推测。」
- 冷启动：「读本库规则和 kb-onboarding 技能，一次问我一个问题。」

## ② 做一件事

先看 [虚构跨境电商招聘闭环](demos/ecommerce-hiring/00-从这里开始.md)。

- 招聘：「读岗位需求与简历，生成完整个性化问句，再按面试证据给结论。」
- 复盘：「读本周记录与上次行动，区分事实、判断、未闭环项，提出下一步。」
- 写作：「读指定素材，先列可加工条目，按我选的平台写草稿。」

这些是指令示例，不是执行按钮；具体技能须按 AI 宿主加载并经授权使用。

## ③ 继续上次

未安装 Dataview 时，可直接在 `_workspace` 文件夹找最近工作。空库无结果正常。修改时间不证明未完成，也不能恢复聊天；选一份问 AI：“读这份文件，列已完成、未完成与待确认，先建议不执行。”

```dataview
TABLE status AS "状态", file.mtime AS "最近更新"
FROM "_workspace"
WHERE !contains(file.path, "/archive/") AND !contains(file.path, "/demos/")
WHERE !contains(file.path, "/private/")
WHERE !contains(file.etags, "#wiki/private") AND !contains(file.etags, "#workspace/private")
WHERE !contains(list("done", "published", "archived", "validated", "cancelled"), status)
SORT file.mtime DESC
LIMIT 6
```

## ④ 回头看

不装插件也可直接查看工作文件内的未完成勾选项；安装 Dataview 后汇总如下。演示材料不进入实际工作统计。

```dataview
TASK
FROM "_workspace"
WHERE !completed AND !contains(file.path, "/archive/") AND !contains(file.path, "/demos/")
WHERE !contains(file.path, "/private/")
WHERE !contains(file.etags, "#wiki/private") AND !contains(file.etags, "#workspace/private")
SORT file.mtime DESC
LIMIT 8
```

行为记录需要先经用户确认；如已启用该流程：

```dataview
TABLE status AS "阶段", next_action AS "下一步"
FROM "_workspace/行为记录"
WHERE contains(list("captured", "reviewed", "extracted", "applied"), status)
WHERE !contains(file.etags, "#wiki/private") AND !contains(file.etags, "#workspace/private")
SORT file.mtime DESC
LIMIT 6
```

首页是本机导航，不是隐私隔离系统；公开截图前仍要检查实际显示内容。不要把默认排除条件当成全库脱敏保证。
