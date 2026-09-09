import type { ThemeConfig } from "antd";

/** 只覆盖登录路由的尺寸与必要对比度，其余继承项目 SEEKWAY 主题。 */
export const loginTheme: ThemeConfig = {
  token: { controlHeight: 58, fontSize: 18 },
  components: {
    Form: { itemMarginBottom: 40 },
    Input: { colorBorder: "#82928a", colorTextPlaceholder: "#66736d" },
  },
};
