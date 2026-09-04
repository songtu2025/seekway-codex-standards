# SEEKWAY Codex 开发规范

本仓库保存公司统一的 Codex 开发规范，用于约束 Codex 在项目中的需求分析、代码修改、测试验证和结果汇报行为。

## 仓库内容

```text
seekway-codex-standards/
├── README.md
├── CHANGELOG.md
├── AGENTS.md
├── docs/
│   └── codex/
│       ├── workflow.md
│       ├── code-quality.md
│       ├── backend.md
│       ├── frontend.md
│       └── verification.md
└── templates/
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
2. 将 `docs/codex` 复制到项目的 `docs/codex`，保留 `AGENTS.md` 中的专项规范索引。
3. 使用 `templates/project-README-template.md` 建立项目 README。
4. 将 `templates/gitignore-template` 复制为项目根目录 `.gitignore`，并按项目实际产物补充。
5. 将 `templates/seekway-theme.css` 复制为项目的 `frontend/src/styles/seekway-theme.css`；复制后项目文件成为运行时唯一令牌来源，并在全局样式入口导入一次。
6. 将 `templates/web-ui-standard-template.md` 复制为项目的 `docs/web-ui-standard.md`，填写组件库、设计来源和项目差异。
7. 使用 `templates/task-template.md` 编写开发任务。
8. 根据项目实际情况补充业务边界、Windows 与 Linux/CI 检查命令和禁止修改项；后端必须选择并配置 Mypy 或 Pyright。
9. 只有子目录存在不同于根目录的特殊规则时，才在该子目录创建 `AGENTS.md`。

### 现有项目

1. 不得使用公司模板覆盖项目已有的 `AGENTS.md`；先审计根目录、相关子目录中的 `AGENTS.md`、`AGENTS.override.md`、README、现有规范和实际检查配置。
2. 保留已经验证有效的业务规则、架构约束、禁止事项和检查命令；区分重复、过时、冲突、目录特有和低频专项内容。
3. 将缺失的公司核心规则差异合并到项目根目录 `AGENTS.md`，只同步与项目技术栈和实际开发活动有关的 `docs/codex` 专项规范，并同步调整根文件中的索引。
4. 项目已有等价规范时应建立索引，不得维护第二份相同规则；目录特有规则只在确有独立作用域时放入嵌套 `AGENTS.md`。
5. `AGENTS.override.md` 会替代同目录的普通 `AGENTS.md`，不得将其作为追加公司规范的合并方式。
6. 在项目 README 中记录公司规范基线版本、接入日期、项目差异和实际检查命令。
7. 根目录 `AGENTS.md` 以 100 行以内为优化目标；历史文件超过目标时应渐进治理，不得为控制行数删除有效规则。
8. 项目实际技术栈、结构和工具优先于公司默认模板，不要求进行无业务收益的全量重构；安全、权限和生产边界不得放宽。
9. 无法确定真伪或不能同时满足的规则必须列出证据、影响和建议并获得确认。完整流程见 `docs/codex/workflow.md` 的“既有项目规范接入”。

## Web 界面规范

`templates/seekway-theme.css` 是公司默认令牌的维护来源；复制到项目后，项目主题文件或已有主题配置成为该项目的运行时唯一来源。视觉、交互、页面状态、响应式和可访问性规则只在项目的 `docs/web-ui-standard.md` 中维护，该文件由 `templates/web-ui-standard-template.md` 初始化。

对应的设计资产位于 [SEEKWAY Web UI Kit V1.2.0](https://www.figma.com/design/eed9GukOv7zM7n04Lu1xUl)。其中 `04 Page Templates` 仅供参考和按需组合，不要求项目整页套用，也不会成为运行时依赖。

项目负责人必须填写界面规范顶部的项目配置。具体优先级、默认视觉和项目差异以该文件为唯一依据，README 不重复维护。

## 规则加载方式

Codex 按以下顺序读取 `AGENTS.md`：

1. Codex 用户目录中的全局规则。
2. 项目根目录中的项目规则。
3. 从项目根目录到当前工作目录之间的子目录规则。

全局规则只适合保存稳定的跨项目偏好和底线；项目交付所需的业务、架构、检查和安全规则必须随仓库维护，不得只存在于某位开发者的全局文件中。

越接近当前工作目录的文件越具体，并在合并后靠后生效。根目录与子目录规则不得保留互相冲突的要求；发现冲突时，应先修正规则再继续开发。

新项目根目录 `AGENTS.md` 应控制在 100 行以内，只保留每次任务都必须生效的规则和按触发条件加载的索引。历史项目以不丢失有效规则为前提渐进精简。完整开发细则保存在 `docs/codex`，项目界面差异保存在 `docs/web-ui-standard.md`，任务验收和检查命令分别维护在任务说明和项目 README 中；Codex 只读取当前任务命中的内容。

同一目录最多加载一个规则文件；存在 `AGENTS.override.md` 时，同目录的 `AGENTS.md` 不参与加载。公司规范不得利用该机制静默遮蔽项目原有规则。

具体加载机制以 [Codex 官方说明](https://learn.chatgpt.com/docs/agent-configuration/agents-md) 为准。

## 规范维护

本仓库只保存规范文档和静态模板，不提供检查脚本或 CI。发布新版本前必须人工核对：

1. 新项目 `AGENTS.md` 不超过 100 行；历史项目超过目标时已说明保留原因和渐进治理方式。
2. AGENTS、README 和 CHANGELOG 版本一致。
3. 专项规范索引和本地 Markdown 链接有效。
4. 同一规则只有一个事实来源，不存在逻辑冲突和非必要重复。
5. 模板中的路径、命令占位和项目配置说明完整。
6. 既有项目接入规则明确禁止覆盖，并说明基线版本、项目差异和 `AGENTS.override.md` 的替换语义。

## 开发与部署边界

- 开发人员默认在 Windows 环境使用 Codex 完成开发和本地验证。

## 当前版本

- 版本：V1.5.0
- 发布日期：2026-09-04
- 变更记录：[CHANGELOG.md](CHANGELOG.md)
