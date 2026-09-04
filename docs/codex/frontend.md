# Codex React 与 TypeScript 工程规范

当任务涉及 React、TypeScript 或前端业务逻辑时，必须读取本文件。视觉、交互、页面状态、响应式和可访问性规则只在项目的 `docs/web-ui-standard.md` 中维护；该文件不存在时读取 `templates/web-ui-standard-template.md` 并报告缺失。

## 1. React 与 TypeScript

生成或修改的前端代码必须：

1. 使用 React 函数组件和 Hooks，遵循项目已有的 React 与 TypeScript 约定。
2. 使用清晰的英文变量名、函数名、组件名和文件名；普通注释、JSDoc 和 TSDoc 使用中文。
3. 将 API 请求集中放在 Service 层，将复杂业务逻辑放入内聚的 Hook、Service 或业务模块。
4. 复用项目已有状态管理和业务模式，不得在多个位置重复维护同一份状态。
5. 前端只负责展示和交互，不得代替后端权限校验；金额、库存和权限等关键结果以后端为准。
6. 页面、组件和 Hook 的职责及规模遵循 `docs/codex/code-quality.md`。

## 2. 禁止事项

1. 不得滥用 `any`、使用 `@ts-ignore` 掩盖错误或无理由使用非空断言。
2. 不得将大量请求、状态和业务逻辑堆积在单个组件中。
3. 未经批准不得引入新的 UI 组件库、图标库、CSS 框架、字体或可视化依赖。
4. 不得为了视觉效果擅自改变业务流程、字段、权限、默认值或操作结果。
