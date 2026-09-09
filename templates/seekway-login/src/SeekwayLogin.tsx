import { useRef, useState, type CSSProperties } from "react";
import { Alert, Button, ConfigProvider, Form, Input, theme } from "antd";
import zhCN from "antd/locale/zh_CN";
import { loginTheme } from "./login-theme";
import EyeOutlined from "@ant-design/icons/EyeOutlined";
import EyeInvisibleOutlined from "@ant-design/icons/EyeInvisibleOutlined";
import { BrandArtwork } from "./BrandArtwork";
import logo from "./assets/seekway-mark-inverse.svg";
import "./seekway-login.css";

export interface LoginValues {
  account: string;
  password: string;
}
export type LoginResult =
  { success: true } | { success: false; message: string };
export interface SeekwayLoginProps {
  /** 接入方处理认证和跳转；返回的失败消息必须已经脱敏。 */
  onLogin: (values: LoginValues) => Promise<LoginResult>;
  systemName?: string;
  helpText?: string;
}

export function SeekwayLogin({
  onLogin,
  systemName = "登录工作台",
  helpText = "账号问题请联系系统管理员",
}: SeekwayLoginProps) {
  const { token } = theme.useToken();
  const [pending, setPending] = useState(false);
  const [feedback, setFeedback] = useState<LoginResult | null>(null);
  const submitting = useRef(false);
  const variables = {
    "--login-page": token.colorBgLayout,
    "--login-text": token.colorText,
    "--login-muted": token.colorTextSecondary,
    "--login-font": token.fontFamily,
  } as CSSProperties;

  async function submit(values: LoginValues) {
    if (submitting.current) return;
    submitting.current = true;
    setPending(true);
    setFeedback(null);
    try {
      setFeedback(await onLogin(values));
    } catch {
      setFeedback({ success: false, message: "暂时无法登录，请稍后重试" });
    } finally {
      submitting.current = false;
      setPending(false);
    }
  }

  return (
    <ConfigProvider
      theme={loginTheme}
      button={{ autoInsertSpace: false }}
      locale={{
        ...zhCN,
        global: { ...zhCN.global, show: "显示密码", hide: "隐藏密码" },
      }}
    >
      <main className="seekway-login" style={variables}>
        <section className="seekway-login__brand" aria-label="SEEKWAY 品牌">
          <div className="seekway-login__signature">
            <div
              className="seekway-login__logo"
              role="img"
              aria-label="SEEKWAY"
            >
              <img src={logo} alt="" width="48" height="48" />
              <span>SEEKWAY</span>
            </div>
            <p className="seekway-login__brand-meaning">风起为帆，行而成路。</p>
          </div>
          <div className="seekway-login__art">
            <BrandArtwork />
          </div>
        </section>
        <section className="seekway-login__entry" aria-labelledby="login-title">
          <div className="seekway-login__form">
            <header className="seekway-login__heading">
              <h1 id="login-title">{systemName}</h1>
              <p>请输入账号和密码</p>
            </header>
            <Form<LoginValues>
              layout="vertical"
              requiredMark={false}
              onFinish={submit}
              disabled={pending}
              validateTrigger="onBlur"
              scrollToFirstError={{ focus: true }}
            >
              <Form.Item
                name="account"
                label="账号"
                rules={[
                  { required: true, whitespace: true, message: "请输入账号" },
                ]}
              >
                <Input autoComplete="username" placeholder="请输入账号" />
              </Form.Item>
              <Form.Item
                name="password"
                label="密码"
                rules={[{ required: true, message: "请输入密码" }]}
              >
                <Input.Password
                  autoComplete="current-password"
                  placeholder="请输入密码"
                  iconRender={(visible) =>
                    visible ? (
                      <EyeInvisibleOutlined title="隐藏密码" />
                    ) : (
                      <EyeOutlined title="显示密码" />
                    )
                  }
                />
              </Form.Item>
              <Button type="primary" htmlType="submit" block loading={pending}>
                登录
              </Button>
            </Form>
            <div aria-live="polite" aria-atomic="true">
              {feedback && (
                <Alert
                  className="seekway-login__feedback"
                  type={feedback.success ? "success" : "error"}
                  title={feedback.success ? "登录成功" : feedback.message}
                  showIcon
                />
              )}
            </div>
            <p className="seekway-login__help">{helpText}</p>
          </div>
        </section>
      </main>
    </ConfigProvider>
  );
}
