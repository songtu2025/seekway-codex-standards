# Codex React 与 TypeScript 工程规范

涉及 React、TypeScript 或前端业务逻辑时，必须读取本文件。界面规则由项目的 `docs/web-ui-standard.md` 索引；文件不存在时读取对应模板并报告缺失。

## 1. React 与 TypeScript

生成或修改的前端代码必须：

1. 使用 React 函数组件和 Hooks，并遵循项目已有约定。
2. 使用清晰的英文变量名、函数名、组件名和文件名；普通注释、JSDoc 和 TSDoc 使用中文。
3. API 请求放在 Service 层，复杂业务逻辑放入内聚的 Hook、Service 或业务模块。
4. 复用已有状态管理和业务模式，不得在多处维护同一状态。
5. 前端只负责展示和交互，不得代替后端权限校验；金额、库存和权限等关键结果以后端为准。
6. 页面、组件和 Hook 的职责及规模遵循 `docs/codex/code-quality.md`。

## 2. 组件与主题基线

1. 新 Web 项目默认使用 Ant Design 6 和 `@ant-design/icons` 6，React 版本不得低于 18。
2. 现有项目保留已验证的组件库、图标和主题；没有成熟组件库时，改用公司基线前必须确认。

组件按以下顺序选择：

```text
Ant Design 能满足需求
└── 直接使用 Ant Design 组件和 Token

多个页面重复使用，并包含稳定业务规则
└── 组合 Ant Design 组件形成业务组件

Ant Design 无法满足必要的业务、交互或可访问性要求
└── 说明缺口、复用范围和验证方式后，自定义基础组件
```

只改变名称、默认属性或样式时，不得创建转发组件；应使用业务代码、ThemeConfig、组件 Token、语义化 `classNames` 或 `styles`。自定义基础组件不得复制 Ant Design 已有能力，也不得通过依赖内部 DOM、内部类名或高优先级全局覆盖实现。

Ant Design 组件令牌由 `seekway-antd-theme.ts` 维护并通过根级 `ConfigProvider` 应用；布局扩展放在 `seekway-theme.css`，两处不得定义同一令牌。全局反馈必须位于 Ant Design `App` 上下文，并通过 Hook 或上下文实例调用 message、notification 和 Modal，不得使用无法继承主题的静态调用。

采用公司基线时，`@ant-design/icons` 是唯一主要业务图标体系；图标按钮必须有可访问名称和提示。

使用项目已有包管理器从 npm Registry 安装基线依赖并提交锁文件，不得从非官方站点下载或用公共 CDN 引入生产代码。官方来源：[Ant Design React 文档](https://ant.design/docs/react/introduce/)、[`antd` npm 包](https://www.npmjs.com/package/antd)、[Ant Design 图标文档](https://ant.design/components/icon/)、[`@ant-design/icons` npm 包](https://www.npmjs.com/package/@ant-design/icons)。

## 3. 禁止事项

1. 不得滥用 `any`、使用 `@ts-ignore` 掩盖错误或无理由使用非空断言。
2. 不得将大量请求、状态和业务逻辑堆积在单个组件中。
3. 除新 Web 项目的 Ant Design 6 和 `@ant-design/icons` 6 基线外，未经批准不得引入新的 UI 组件库、图标库、CSS 框架、字体或可视化依赖。
4. 不得为了视觉效果擅自改变业务流程、字段、权限、默认值或操作结果。
