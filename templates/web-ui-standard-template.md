# SEEKWAY Web 界面开发标准

- 规范版本：V1.4.0
- 适用范围：公司内部和后台业务系统
- 视觉基线：SEEKWAY 退货语义分析智能体
- 默认技术栈：React 18 及以上、TypeScript、Vite、Ant Design 6
- 维护负责人：待填写
- 最后更新：2026-09-08

本文件保存所有界面任务都要遵守的规则，并索引按任务加载的专项规范。现有项目保留已验证的设计系统，在“项目配置”中记录差异，不为套用默认值进行全量重构。

## 1. 项目配置

项目负责人填写本节；未填写的项目采用默认值。

- 公司品牌名称：`SEEKWAY`。
- 品牌主色：默认 `#12765B`。
- UI 组件库：新项目默认 Ant Design 6；现有项目填写已验证的组件库，不得自动迁移。
- 图标体系：新项目默认 `@ant-design/icons` 6；同一项目只能使用一个主要业务图标体系。
- 默认语言：简体中文。
- 默认时区：待填写。
- 主要设计视口：默认 `1440 × 900`。
- 最小支持视口：默认 `1024 × 640`。
- 是否支持移动端：默认否。
- 公司设计系统：[SEEKWAY Web UI Kit V1.2.0](https://www.figma.com/design/eed9GukOv7zM7n04Lu1xUl)。
- 项目设计稿或设计系统地址：待填写；没有时使用公司设计系统。
- 允许的项目差异：待填写。

## 2. 规则优先级

发生冲突时按以下顺序执行：

1. 用户明确提供的设计稿和验收标准。
2. 本项目填写后的界面规范。
3. 项目已有设计令牌、基础组件和相似页面。
4. 本标准的默认规则。

设计稿不得覆盖业务、权限、安全和可访问性要求。规则冲突时，必须说明并等待确认。

## 3. 专项规范路由

所有 Web 界面任务先读取本文件，再按任务内容读取下表中的专项规范。任务同时命中多项时全部读取；未命中时不得加载。项目文件缺失时读取对应模板并报告缺失。

| 任务内容 | 项目规范 | 缺失时读取 |
| --- | --- | --- |
| 页面骨架、响应式、应用壳层、登录页、导航或页面标题 | `docs/web-ui-layout-standard.md` | `templates/web-ui-layout-standard-template.md` |
| 按钮、表单、弹窗、抽屉、操作反馈或提交状态 | `docs/web-ui-form-standard.md` | `templates/web-ui-form-standard-template.md` |
| 表格、列表、数据状态、数据格式、图标、图片或图表 | `docs/web-ui-data-standard.md` | `templates/web-ui-data-standard-template.md` |

## 4. 设计原则

1. **操作高效**：减少查找、录入、比较和批量处理的步骤。
2. **保持一致**：相同概念使用相同名称、位置、组件和交互，不为单个页面另设规则。
3. **层级清晰**：一个页面只有一个主要标题，一个操作区域最多只有一个主按钮。
4. **密度适中**：默认使用中等信息密度；高频数据页面可更紧凑，但不能影响阅读和操作。
5. **状态完整**：覆盖正常、等待、无数据、失败、禁用和操作反馈。
6. **减少装饰**：普通后台功能不使用大面积渐变、装饰性插画、玻璃拟态、大标题或大留白。

## 5. 设计令牌

采用公司基线时，只使用 Ant Design Token 和 SEEKWAY 扩展令牌，不得散落无语义的视觉数值或建立第二套主题。现有项目使用原主题系统中的等价令牌。

新项目复制 `templates/seekway-antd-theme.ts` 和 `templates/seekway-theme.css` 到对应的前端路径。前者是 Ant Design 组件令牌的唯一来源；后者只维护侧栏和页面布局等扩展，并在全局入口导入一次。两者不得定义同一令牌。现有项目继续使用原主题配置，只映射 SEEKWAY 语义。

必须在应用根节点启用中文环境和 SEEKWAY 主题：

```tsx
import { App as AntdApp, ConfigProvider } from "antd";
import zhCN from "antd/locale/zh_CN";

import { seekwayAntdTheme } from "./theme/seekway-antd-theme";
import "./styles/seekway-theme.css";

<ConfigProvider locale={zhCN} theme={seekwayAntdTheme}>
  <AntdApp>
    <Root />
  </AntdApp>
</ConfigProvider>;
```

通用交互使用 Ant Design 组件。自定义 React 区域通过 `theme.useToken()` 获取颜色、字体、圆角和阴影；CSS 只引用 `seekway-theme.css` 中的布局扩展变量。DatePicker、Calendar 等日期组件须配置 Day.js 中文环境；项目直接导入 Day.js 时必须将其声明为直接依赖。

### 5.1 颜色

- 颜色按用途命名，不用 `blue-500` 等视觉名称表达业务用途。
- Cover 与应用侧栏使用 `--gradient-sidebar`；渐变起点由 `--color-surface-sidebar-start` 统一管理。
- 侧栏悬停使用半透明的 `--color-surface-sidebar-hover`，不得重新硬编码固定深色。
- 状态颜色必须配合文字、图标或形状，不得只用颜色区分成功、警告和失败。
- 警告图形使用 `colorWarning`，小号警告文字使用 `colorWarningText`；现有主题使用等价令牌。
- 正文和占位文字与背景对比度不低于 `4.5:1`；大号文字以及承载控件边界、状态或含义的图标、边框和焦点指示不低于 `3:1`。
- `colorBorderSecondary` 或等价令牌只用于无语义的分隔线；输入框等控件边界使用 `colorBorder` 或对比度更高的组件 Token。
- 禁用状态不能只降低透明度到无法辨认，仍须保留内容可读性。

### 5.2 字体

- 页面标题使用 `28px`，卡片或分区标题使用 `18px` 或 `20px`，正文默认 `14px`。
- 正文、输入内容和主要操作文字不得小于 `12px`；输入内容默认使用 `14px`，不得照搬参考项目中的 `10px` 小字号。
- 未提供 Inter 或 Noto Sans SC 字体文件时使用系统回退字体，不得自行增加远程字体或生产依赖。
- 正文默认使用常规字重，标题和需要强调的信息使用中等或半粗字重。
- 表格数字使用等宽数字特性；长编号、哈希和代码可使用项目批准的等宽字体。
- 不得仅靠字号表达层级，还应结合间距、字重和位置。

### 5.3 间距、尺寸和圆角

- 使用 `4px` 基础网格，只能从令牌中选择间距。
- 同一表单、筛选区或操作区中的控件高度必须一致。
- 默认控件高度为 `38px`，紧凑控件为 `34px`；主要表单、触摸场景或重要操作可使用 `40px`。
- 圆角用于表达组件边界，普通按钮、标签和输入框不使用胶囊形状。
- 普通记录使用 `48px` 基准行高；包含摘要、状态和操作的复杂业务记录可使用 `84px`，不得机械压缩成单行。

### 5.4 阴影、层级和动效

- 默认通过背景和边框区分层级，阴影只用于浮层、弹窗、抽屉和悬浮控件。
- 轻量浮层使用 `boxShadow`，弹窗和大型浮层使用 `boxShadowSecondary`；现有主题使用等价令牌。
- 层级由项目的 `z-index` 令牌管理，业务组件不得使用任意超大数值。
- 普通过渡时长使用 `120–200ms`，弹窗和抽屉使用 `200–300ms`。
- 动效不得阻塞操作或为纯装饰循环播放；必须支持 `prefers-reduced-motion`。

## 6. 可访问性

项目默认达到 WCAG 2.2 AA：

- 优先使用原生 `button`、`a`、`input`、`table` 等语义元素，不能用 `div` 模拟可交互控件。
- 所有关键功能可仅使用键盘完成，焦点顺序与视觉顺序一致，焦点样式清晰且不被遮挡。
- 表单标签、错误信息、图标按钮和动态反馈必须具有可访问名称或关联关系。
- 自定义菜单、标签页、树、对话框和组合框必须遵循对应的 WAI-ARIA Authoring Practices 键盘模型。
- 目标区域至少满足 WCAG 2.2 的 `24 × 24 CSS px` 要求；SEEKWAY 后台控件默认不小于 `34px` 高。
- 不得仅依赖颜色、位置、形状、声音或悬停表达关键信息。
- 页面缩放到 `200%` 后仍可阅读和操作，文本不得被截断到无法理解。

所有界面默认使用简体中文，同一业务对象只能有一个正式名称。文案应简短、直接并说明下一步，不使用娱乐化表达。

## 7. 工程边界

React、TypeScript、组件决策和依赖约束见 `docs/codex/frontend.md` 与 `docs/codex/code-quality.md`；开发流程和验证要求见 `docs/codex/workflow.md` 与 `docs/codex/verification.md`。

新项目基线只包含 Ant Design 6 和 `@ant-design/icons` 6，不含 `@ant-design/pro-components`、其他 UI 库、CSS 框架或可视化库。组件必须按 `docs/codex/frontend.md` 的决策树选择。

## 8. 界面验收清单

- [ ] 已读取本文件和任务命中的专项规范，未加载无关专项文件。
- [ ] 已逐项验证任务命中的专项规则。
- [ ] 页面目标、信息层级和主操作明确。
- [ ] 复用了项目令牌、组件、图标和相似页面模式。
- [ ] 采用公司基线时，根级 `ConfigProvider`、Ant Design `App`、中文环境和 SEEKWAY 主题已经生效。
- [ ] 任务涉及的加载、空数据、失败、无权限、提交和反馈状态完整。
- [ ] 目标视口下没有意外横向滚动、遮挡和不可操作区域。
- [ ] 关键路径可仅使用键盘完成，焦点清晰且不被遮挡。
- [ ] 对比度、目标尺寸和语义结构达到 WCAG 2.2 AA。
- [ ] 未混入第二套 UI 或图标体系，也未依赖 Ant Design 内部 DOM、内部类名或高优先级全局覆盖。
- [ ] 未擅自改变业务、权限、接口和数据结构，或引入基线之外的依赖。

未实际完成的视觉、交互或可访问性检查必须报告为未验证。

## 9. 参考标准

- [SEEKWAY Web UI Kit V1.2.0](https://www.figma.com/design/eed9GukOv7zM7n04Lu1xUl)
- [Web Content Accessibility Guidelines (WCAG) 2.2](https://www.w3.org/TR/WCAG22/)
- [ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/)
- [Design Tokens Format Module 2025.10](https://www.designtokens.org/tr/2025.10/format/)
