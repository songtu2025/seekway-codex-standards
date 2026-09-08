# SEEKWAY Codex 开发规范

本仓库保存 SEEKWAY Codex 开发规范，约束需求分析、代码修改、验证和结果汇报。

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
    ├── seekway-antd-theme.ts
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
3. 使用 `templates/project-README-template.md` 建立 README，并填写业务边界、实际检查命令和项目差异。
4. 将 `templates/gitignore-template` 复制为根目录 `.gitignore`，再补充项目产物。
5. 新 Web 项目按 `docs/codex/frontend.md` 安装 Ant Design 6 和 `@ant-design/icons` 6，并复制两个 SEEKWAY 主题模板。
6. 将 `templates/web-ui-standard-template.md` 复制为 `docs/web-ui-standard.md`，填写设计来源和项目差异。
7. 使用 `templates/task-template.md` 编写任务；仅在子目录确有独立规则时创建嵌套 `AGENTS.md`。

### 现有项目

不得用公司模板覆盖已有规则，也不得为了符合默认技术栈进行全量迁移。先审计项目规则和实际配置，再按 `docs/codex/workflow.md` 的“既有项目规范接入”执行差异合并。项目 README 必须记录规范基线版本、接入日期、项目差异和真实检查命令。

## Web 界面规范

新 Web 项目默认使用 Ant Design 6、`@ant-design/icons` 6 和 SEEKWAY 主题。依赖来源、安装方式和工程约束见 `docs/codex/frontend.md`；视觉与交互规则见由 `templates/web-ui-standard-template.md` 初始化的 `docs/web-ui-standard.md`。设计参考为 [SEEKWAY Web UI Kit V1.2.0](https://www.figma.com/design/eed9GukOv7zM7n04Lu1xUl)。

## 规则加载方式

Codex 按以下顺序加载规则：

1. Codex 用户目录中的全局规则。
2. 项目根目录中的项目规则。
3. 从项目根目录到当前工作目录之间的子目录规则。

越接近当前目录的规则越具体。全局规则只保存跨项目偏好和底线；项目规则、嵌套规则、专项文档及 `AGENTS.override.md` 的职责和冲突处理见 `docs/codex/workflow.md`。

具体加载机制以 [Codex 官方说明](https://learn.chatgpt.com/docs/agent-configuration/agents-md) 为准。

## 规范维护

本仓库不提供检查脚本或 CI。发布前必须人工核对：

1. 新项目 `AGENTS.md` 不超过 100 行；历史项目超过目标时已说明保留原因和渐进治理方式。
2. AGENTS、README 和 CHANGELOG 版本一致。
3. 专项规范索引和本地 Markdown 链接有效。
4. 同一规则只有一个事实来源，不存在逻辑冲突和非必要重复。
5. 模板中的路径、命令占位和项目配置说明完整。
6. 既有项目接入规则没有覆盖原规则，并正确处理 `AGENTS.override.md`。

## 当前版本

- 版本：V1.6.0
- 发布日期：2026-09-08
- 变更记录：[CHANGELOG.md](CHANGELOG.md)
