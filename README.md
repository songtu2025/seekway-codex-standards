# SEEKWAY Codex 开发规范

本仓库保存公司统一的 Codex 开发规范，用于约束 Codex 在项目中的需求分析、代码修改、测试验证和结果汇报行为。

## 仓库内容

```text
seekway-codex-standards/
├── README.md
├── CHANGELOG.md
├── AGENTS.md
└── templates/
    ├── check.ps1
    ├── check.sh
    ├── gitignore-template
    ├── seekway-theme.css
    ├── web-ui-standard-template.md
    ├── task-template.md
    └── project-README-template.md
```

首次使用时，可以先输入：

```text
请读取当前项目的 AGENTS.md 和 README，只概括项目规则，不要修改文件。
```

## 项目负责人配置

### 新项目

1. 将根目录 `AGENTS.md` 复制到项目根目录。
2. 使用 `templates/project-README-template.md` 建立项目 README。
3. 将 `templates/gitignore-template` 复制为项目根目录 `.gitignore`，并按项目实际产物补充。
4. 将 `templates/check.ps1` 和 `templates/check.sh` 复制到项目 `scripts/` 目录，保持两端检查入口一致。
5. 将 `templates/seekway-theme.css` 复制为项目的 `frontend/src/styles/seekway-theme.css`，并在全局样式入口导入一次。
6. 将 `templates/web-ui-standard-template.md` 复制为项目的 `docs/web-ui-standard.md`，填写组件库、设计来源和项目差异。
7. 使用 `templates/task-template.md` 编写开发任务。
8. 根据项目实际情况补充业务边界、检查命令和禁止修改项。
9. 只有子目录存在不同于根目录的特殊规则时，才在该子目录创建 `AGENTS.md`。

### 现有项目

1. 保留项目已经验证有效的业务规则和检查命令。
2. 将公司核心规则合并到项目根目录 `AGENTS.md`。
3. 对照 `templates/gitignore-template`、`templates/check.ps1` 和 `templates/check.sh` 补齐缺失的忽略规则和检查入口。
4. 不要求为了目录统一而进行无业务收益的全量重构。
5. 历史项目与公司规范存在差异时，应在项目 `AGENTS.md` 中明确说明。

## Web 界面规范

`templates/seekway-theme.css` 是 Web 设计令牌的唯一取值来源；`templates/web-ui-standard-template.md` 说明这些令牌的使用规则。两者面向公司内部和后台业务系统，默认采用深森林绿、米白背景、桌面端优先、数据密集和操作效率优先的 SEEKWAY“运行驾驶舱”设计方向，不适用于官网、活动页和营销页面。

对应的设计资产位于 [SEEKWAY Web UI Kit V1.2.0](https://www.figma.com/design/eed9GukOv7zM7n04Lu1xUl)。其中 `04 Page Templates` 仅供参考和按需组合，不要求项目整页套用，也不会成为运行时依赖。

项目负责人必须先填写模板顶部的项目配置。Codex 修改界面时，按以下顺序确定规则：

1. 用户明确提供的设计稿或验收标准。
2. 项目的 `docs/web-ui-standard.md`。
3. 项目已有设计系统和相似页面。
4. 公司默认界面规范。

项目已有经过验证的设计系统时，不要求为了套用默认数值而整体重构；新增和修改的界面应继续复用现有规则，并把差异记录到项目界面规范中。

## 规则加载方式

Codex 按以下顺序读取 `AGENTS.md`：

1. Codex 用户目录中的全局规则。
2. 项目根目录中的项目规则。
3. 从项目根目录到当前工作目录之间的子目录规则。

越接近当前工作目录的文件越具体，并在合并后靠后生效。根目录与子目录规则不得保留互相冲突的要求；发现冲突时，应先修正规则再继续开发。

具体加载机制以 [Codex 官方说明](https://learn.chatgpt.com/docs/agent-configuration/agents-md) 为准。

## 开发与部署边界

- 开发人员默认在 Windows 环境使用 Codex 完成开发和本地验证。

## 当前版本

- 版本：V1.3.0
- 发布日期：2026-09-04
- 变更记录：[CHANGELOG.md](CHANGELOG.md)
