# Seekway Codex 开发规范

本仓库保存公司统一的 Codex 开发规范，用于约束 Codex 在项目中的需求分析、代码修改、测试验证和结果汇报行为。

## 仓库内容

```text
seekway-codex-standards/
├── README.md
├── AGENTS.md
└── templates/
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
3. 使用 `templates/task-template.md` 编写开发任务。
4. 根据项目实际情况补充业务边界、检查命令和禁止修改项。
5. 只有子目录存在不同于根目录的特殊规则时，才在该子目录创建 `AGENTS.md`。

### 现有项目

1. 保留项目已经验证有效的业务规则和检查命令。
2. 将公司核心规则合并到项目根目录 `AGENTS.md`。
3. 不要求为了目录统一而进行无业务收益的全量重构。
4. 历史项目与公司规范存在差异时，应在项目 `AGENTS.md` 中明确说明。

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

- 版本：V1.0.0
- 发布日期：2026-08-06
