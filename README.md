# SEEKWAY Codex 开发规范

本仓库保存 SEEKWAY Codex 开发规范，约束需求分析、代码修改、验证和结果汇报。

## 仓库内容

- [AGENTS.md](AGENTS.md)：始终生效的规则和专项规范索引。
- [docs/codex](docs/codex)：按任务加载的开发与验证规范。
- [templates](templates)：项目文档、主题、界面规范和登录页模板。
- [CHANGELOG.md](CHANGELOG.md)：版本变更记录。

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

## 登录页模板

入口：[templates/seekway-login](templates/seekway-login)。这是可运行的前端模板，不是认证服务。默认使用已确认的 C 版错位字场，完整品牌文案为 `SEEK THE WAY YOU WANT. LIVE THE LIFE YOU FOUND.`。

本地预览（Windows PowerShell 与 Linux 命令相同；Node.js 22.12 及以上）：

```sh
cd templates/seekway-login
npm ci
npm run dev
```

打开终端显示的本地地址。任意非空模拟输入默认展示“尚未连接登录服务”；地址加 `?demo=success` 可验证成功状态。不要输入真实凭据；预览不会发送或存储输入值。

接入业务项目：

1. 复制 `src/SeekwayLogin.tsx`、`src/BrandArtwork.tsx`、`src/login-theme.ts`、`src/seekway-login.css`、`src/brand-artwork.css` 和完整 `src/assets/` 到项目登录模块。不要复制 `main.tsx` 的模拟回调到生产业务。
2. 沿用项目根级 `ConfigProvider`、Ant Design `App` 和 SEEKWAY 主题。组件内部的局部 Provider 仅调整登录页尺寸、中文和必要对比度，不改变其他业务页面；已有主题文件不得重复复制。
3. 将 `onLogin` 对接项目已有认证 Service。认证、Token 管理和成功跳转由接入项目负责；模板只处理输入校验、提交状态和脱敏后的结果反馈。

```tsx
<SeekwayLogin
  systemName="登录工作台"
  helpText="账号问题请联系系统管理员"
  onLogin={handleLogin}
/>
```

`handleLogin` 接收 `{ account, password }`，返回 `{ success: true }` 或 `{ success: false, message: "脱敏后的提示" }`。模板不提供注册、找回密码、验证码或单点登录。现有项目是否替换登录页由负责人决定。

接入边界：

- 业务项目通过 `systemName` 和 `helpText` 配置文案。
- Logo、完整 slogan、品牌色和默认字场作为品牌基线保留；需要调整时先由项目负责人确认。具体视觉参数以模板代码为准，不在规范中重复维护。
- 桌面展示艺术字场；窄屏布局改为简洁双句文案，同时保留 Logo 和完整表单，不添加循环动效。

复制模板时，在业务项目已有 README 中记录本仓库地址、来源提交号和接入日期。复制后的代码不会自动升级；后续按 [CHANGELOG](CHANGELOG.md) 对照来源提交进行差异合并，保留业务接入逻辑。模板变更记录区分视觉调整与功能、可访问性修复：前者由接入方选择是否同步，后者说明受影响行为和需同步的文件。

检查环境初始化（与检查命令分开执行）：

```sh
npm ci
npx playwright install chromium
```

Windows / Linux 通用检查：

```sh
npm run check
npm ls antd @ant-design/icons react react-dom
```

`check` 依次执行格式、ESLint、类型、浏览器测试、构建、jscpd、knip 和循环依赖检查。没有后端，`vulture` 不适用。也可使用本机已安装的 Chrome：PowerShell 执行 `$env:PLAYWRIGHT_CHANNEL='chrome'; npm run check`；Linux 执行 `PLAYWRIGHT_CHANNEL=chrome npm run check`。检查命令不安装依赖。

品牌标记来自 [Figma 反白 Logo 节点](https://www.figma.com/design/eed9GukOv7zM7n04Lu1xUl?node-id=38-17)，使用原始 SVG 与节点规定的字标间距；它不属于开源字体许可证的授权范围。Anton 字场字体和 Inter 字标字体以原始 WOFF2 本地加载，许可证随 `src/assets` 分发，运行时不访问字体 CDN。模板构建自动输出 `Fonts-LICENSE.txt`；接入项目也必须让该许可随字体构建产物一起分发。

## 开发辅助资源（可选）

按当前问题选择，不要求每个任务都使用，也不作为项目启动或验收的前提。

| 遇到的问题 | 推荐资源 | 使用目标 |
| --- | --- | --- |
| 不知道如何准确描述需求或交互 | [VibeHub Skill](https://github.com/oil-oil/vibe-hub-skill) | 将口语描述整理成准确需求，保持原意并解释相关术语 |
| 不理解需求讨论中的产品概念 | [VibeHub 产品术语](https://vibe-hub.org/topics/product) | 查阅用户故事、用户流程、PRD、MVP 等概念；直接访问，无需安装 |
| 架构或流程复杂，文字难以说明 | [Archify](https://github.com/tt-a1i/archify) | 用交互图示说明关键关系，辅助方案讨论和项目交接 |
| 不知道已有实现在哪里、修改会影响什么 | [CodeGraph](https://github.com/colbymchenry/codegraph) | 通过代码索引查找符号、调用链和依赖，定位可复用实现 |

- 推荐不等于安装授权。按需参考各资源官方说明安装，任务需要时再使用；CodeGraph 是否建立项目索引由项目负责人确认。不自动修改个人配置，不加入业务生产依赖。
- 术语解释不能替代业务需求确认；架构图和代码索引需与源码核对，索引过期时直接检查当前代码。这些工具不替代测试及代码质量检查。
- 工具不可用时继续使用现有开发方式，不因此阻塞任务。权限、敏感信息和安装边界沿用 [开发流程与项目边界](docs/codex/workflow.md)。

## 规则加载方式

规则优先级、目录作用域及 `AGENTS.override.md` 的处理方式见 [开发流程与项目边界](docs/codex/workflow.md)。具体加载机制以 [Codex 官方说明](https://learn.chatgpt.com/docs/agent-configuration/agents-md) 为准。

## 规范版本

版本号使用 `MAJOR.MINOR.PATCH`：

- **PATCH**：修正错别字、措词或不改变执行行为的说明。
- **MINOR**：新增规则、模板、检查能力或向后兼容的默认能力。
- **MAJOR**：删除或反转现有规则、改变默认技术栈，或要求现有项目迁移。

版本发布后不得修改同一版本的内容。后续变化必须增加版本号，并在 CHANGELOG 中记录新增、变更和删除的规则。

规范维护和发布检查见 [验证与完成报告规范](docs/codex/verification.md)。

## 当前版本

- 版本：V1.8.1
- 发布日期：2026-09-09
- 变更记录：[CHANGELOG.md](CHANGELOG.md)
