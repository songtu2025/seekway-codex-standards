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
2. 现有项目保留已验证的组件库、图标和主题；改用公司基线前必须确认。

新建或明显重塑界面时，可选使用 [Frontend Design Skill](https://github.com/anthropics/skills/tree/main/skills/frontend-design) 先形成与业务、受众和页面目标相关的配色、字体、布局、动效和文案方案，再实现代码。用户明确要求、项目现有设计系统和 Web UI 规范始终优先；不得因使用该 Skill 擅自增加字体、组件库或其他生产依赖。

组件按以下顺序选择：

```text
Ant Design 能满足需求
└── 直接使用 Ant Design 组件和 Token

多个页面重复使用，并包含稳定业务规则
└── 组合 Ant Design 组件形成业务组件

Ant Design 无法满足必要的业务、交互或可访问性要求
└── 说明缺口、复用范围和验证方式后，自定义基础组件
```

只改变名称、默认属性或样式时，使用业务代码、ThemeConfig、组件 Token、`classNames` 或 `styles`，不得创建转发组件。自定义基础组件不得复制 Ant Design 已有能力，也不得依赖内部 DOM、内部类名或高优先级全局覆盖。

Ant Design 组件令牌由 `seekway-antd-theme.ts` 维护并通过根级 `ConfigProvider` 应用；布局扩展放在 `seekway-theme.css`，两处不得定义同一令牌。全局反馈须位于 Ant Design `App` 上下文，通过 Hook 或上下文实例调用 message、notification 和 Modal，不得使用静态调用。

采用公司基线时，`@ant-design/icons` 是唯一主要业务图标体系，图标按钮须有可访问名称和提示。使用项目现有包管理器从 npm Registry 安装依赖并提交锁文件，不得从非官方站点或公共 CDN 引入生产代码。官方来源：[Ant Design React 文档](https://ant.design/docs/react/introduce/)、[`antd` npm 包](https://www.npmjs.com/package/antd)、[Ant Design 图标文档](https://ant.design/components/icon/)、[`@ant-design/icons` npm 包](https://www.npmjs.com/package/@ant-design/icons)。

## 3. 前端 Demo 与合成数据

1. 新系统、新操作流程、多角色交互或界面方案不明确时，可先用前端 Demo 验证页面关系、操作路径和信息层级。页面已有成熟模式或主要风险在后端、集成、数据或性能时，不得为了展示而先做完整 Demo。
2. Demo 使用的合成数据不得来自真实用户或生产环境，必须明确标记为演示数据，并尽量与预期数据契约一致。
3. 合成数据至少覆盖任务需要的正常、加载、空数据、失败、无权限、长文本和极值状态；不需要的状态不得为了凑清单而强行增加。
4. 合成数据放在集中的 fixture、mock Service 或适配层，不得散落在页面组件内；不得为 Demo 擅自新增生产依赖。
5. Demo 经用户确认后，先定义接口和数据契约，再打通一个真实页面、接口、业务逻辑和数据读写的最小端到端流程。Demo 代码只有通过生产代码要求后才可继续使用，否则应删除或重写。

## 4. 禁止事项

1. 不得滥用 `any`、使用 `@ts-ignore` 掩盖错误或无理由使用非空断言。
2. 不得将大量请求、状态和业务逻辑堆积在单个组件中。
3. 除新 Web 项目的 Ant Design 6 和 `@ant-design/icons` 6 基线外，未经批准不得引入新的 UI 组件库、图标库、CSS 框架、字体或可视化依赖。
4. 不得为了视觉效果擅自改变业务流程、字段、权限、默认值或操作结果。
