import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { App as AntdApp, ConfigProvider } from "antd";
import zhCN from "antd/locale/zh_CN";
import { seekwayAntdTheme } from "../../seekway-antd-theme";
import "../../seekway-theme.css";
import { SeekwayLogin, type LoginResult } from "./SeekwayLogin";
import "./preview.css";

/** 仅用于预览；不读取、保存或发送凭据，不是认证实现。 */
async function previewLogin(): Promise<LoginResult> {
  await new Promise((resolve) => setTimeout(resolve, 800));
  return new URLSearchParams(location.search).get("demo") === "success"
    ? { success: true }
    : { success: false, message: "这是模板预览，尚未连接登录服务" };
}

const root = document.getElementById("root");
if (!root) throw new Error("缺少页面挂载节点");
createRoot(root).render(
  <StrictMode>
    <ConfigProvider locale={zhCN} theme={seekwayAntdTheme}>
      <AntdApp>
        <SeekwayLogin onLogin={previewLogin} />
      </AntdApp>
    </ConfigProvider>
  </StrictMode>,
);
