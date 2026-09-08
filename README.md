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
    ├── web-ui-layout-standard-template.md
    ├── web-ui-form-standard-template.md
    ├── web-ui-data-standard-template.md
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
6. 将四份 `web-ui-*-template.md` 分别复制为 `docs/web-ui-standard.md`、`docs/web-ui-layout-standard.md`、`docs/web-ui-form-standard.md` 和 `docs/web-ui-data-standard.md`，填写设计来源和项目差异。
7. 使用 `templates/task-template.md` 编写任务；仅在子目录确有独立规则时创建嵌套 `AGENTS.md`。

### 现有项目

不得用公司模板覆盖已有规则，也不得为了符合默认技术栈进行全量迁移。先审计项目规则和实际配置，再按 `docs/codex/workflow.md` 的“既有项目规范接入”执行差异合并。项目 README 必须记录规范基线版本、接入日期、项目差异和真实检查命令。

## Web 界面规范

新 Web 项目默认使用 Ant Design 6、`@ant-design/icons` 6 和 SEEKWAY 主题。依赖来源、安装方式和工程约束见 `docs/codex/frontend.md`；界面核心规则及任务专项索引见 `docs/web-ui-standard.md`。设计参考为 [SEEKWAY Web UI Kit V1.2.0](https://www.figma.com/design/eed9GukOv7zM7n04Lu1xUl)。

现有项目可以继续维护单文件界面规范，不因 V1.7.0 自动拆分；决定迁移时必须保留原规则并同步更新专项索引。

## 规则加载方式

Codex 按以下顺序加载规则：

1. Codex 用户目录中的全局规则。
2. 项目根目录中的项目规则。
3. 从项目根目录到当前工作目录之间的子目录规则。

越接近当前目录的规则越具体。全局规则只保存跨项目偏好和底线；项目规则、嵌套规则、专项文档及 `AGENTS.override.md` 的职责和冲突处理见 `docs/codex/workflow.md`。

具体加载机制以 [Codex 官方说明](https://learn.chatgpt.com/docs/agent-configuration/agents-md) 为准。

## 规范版本

版本号使用 `MAJOR.MINOR.PATCH`：

- **PATCH**：修正错别字、措词或不改变执行行为的说明。
- **MINOR**：新增规则、模板、检查能力或向后兼容的默认能力。
- **MAJOR**：删除或反转现有规则、改变默认技术栈，或要求现有项目迁移。

版本发布后不得修改同一版本的内容。后续变化必须增加版本号，并在 CHANGELOG 中记录新增、变更和删除的规则。

## 规范维护

新增规则必须来自已经发生的问题、安全或平台限制、已确认的技术决策，或现有规则无法覆盖的验收需要。不得将个人偏好、一次性场景或已有工具能够稳定执行的细节写成通用规则。

发布前必须检查并删除重复、失效、已由工具稳定强制或不再适用的规则。规则删除可能改变现有项目行为时，按 MAJOR 版本发布；否则按实际影响选择 PATCH 或 MINOR。

本仓库不提供检查脚本或 CI。发布前必须人工核对：

1. 新项目 `AGENTS.md` 不超过 100 行；历史项目超过目标时已说明保留原因和渐进治理方式。
2. AGENTS、README 和 CHANGELOG 版本一致。
3. 专项规范索引和本地 Markdown 链接有效。
4. 同一规则只有一个事实来源，不存在逻辑冲突和非必要重复。
5. 模板中的路径、命令占位和项目配置说明完整。
6. 既有项目接入规则没有覆盖原规则，并正确处理 `AGENTS.override.md`。
7. 新增和删除规则有依据，版本级别与实际影响一致。

## 当前版本

- 版本：V1.7.0
- 发布日期：2026-09-08
- 变更记录：[CHANGELOG.md](CHANGELOG.md)
