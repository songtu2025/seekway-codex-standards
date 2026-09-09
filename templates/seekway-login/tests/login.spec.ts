import { expect, test } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

test("品牌文案包含完整两句及标点", async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto("/");
  const artwork = page.getByRole("img", {
    name: "SEEK THE WAY YOU WANT. LIVE THE LIFE YOU FOUND.",
    exact: true,
  });
  await expect(artwork).toBeVisible();
  await page.evaluate(() => document.fonts.ready);
  expect((await artwork.locator("text").allTextContents()).join(" ")).toBe(
    "SEEK THE WAY YOU WANT. LIVE THE LIFE YOU FOUND.",
  );
  const fits = await artwork.evaluate((svg) => {
    const view = (svg as SVGSVGElement).viewBox.baseVal;
    return [...svg.querySelectorAll("text")].every((text) => {
      const box = text.getBBox();
      return (
        box.y >= 0 &&
        box.y + box.height <= view.height &&
        box.x + box.width <= view.width
      );
    });
  });
  expect(fits).toBe(true);
});

test("Logo 下方展示品牌寓意", async ({ page }) => {
  await page.goto("/");
  const meaning = page.getByText("风起为帆，行而成路。", { exact: true });
  await expect(meaning).toBeVisible();
  const logo = page.getByRole("img", { name: "SEEKWAY", exact: true });
  const [logoBox, meaningBox] = await Promise.all([
    logo.boundingBox(),
    meaning.boundingBox(),
  ]);
  expect(logoBox).not.toBeNull();
  expect(meaningBox).not.toBeNull();
  if (logoBox && meaningBox) {
    expect(meaningBox.y).toBeGreaterThan(logoBox.y + logoBox.height);
  }
});

test("可访问性与纯键盘登录路径", async ({ page }) => {
  await page.goto("/");
  await page.keyboard.press("Tab");
  await expect(page.getByLabel("账号", { exact: true })).toBeFocused();
  await page.keyboard.type("preview");
  await page.keyboard.press("Tab");
  await expect(page.getByLabel("密码", { exact: true })).toBeFocused();
  await page.keyboard.type("example-only");
  await page.keyboard.press("Tab");
  await expect(page.getByRole("button", { name: "显示密码" })).toBeFocused();
  await page.keyboard.press("Space");
  await expect(page.getByLabel("密码", { exact: true })).toHaveAttribute(
    "type",
    "text",
  );
  await page.keyboard.press("Tab");
  await expect(
    page.getByRole("button", { name: "登录", exact: true }),
  ).toBeFocused();
  const report = await new AxeBuilder({ page })
    .withTags(["wcag2a", "wcag2aa", "wcag21aa", "wcag22aa"])
    .analyze();
  expect(report.violations).toEqual([]);
  await page.keyboard.press("Enter");
  await expect(page.getByText("这是模板预览，尚未连接登录服务")).toBeVisible();
});

for (const zoom of [1.25, 1.5, 2]) {
  test(`页面缩放 ${zoom * 100}% 保留主操作`, async ({ page }) => {
    await page.setViewportSize({ width: 1440, height: 900 });
    await page.goto("/");
    await page.evaluate((scale) => {
      document.documentElement.style.zoom = String(scale);
    }, zoom);
    expect(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= innerWidth,
      ),
    ).toBe(true);
    const button = page.getByRole("button", { name: "登录", exact: true });
    await button.scrollIntoViewIfNeeded();
    await expect(button).toBeInViewport();
    await button.click();
    await expect(page.getByText("请输入账号", { exact: true })).toBeVisible();
  });
}

test("校验、密码可见性、提交与失败反馈", async ({ page }) => {
  const errors: string[] = [];
  page.on("pageerror", (error) => errors.push(error.message));
  await page.goto("/");
  await expect(page).toHaveTitle("SEEKWAY 登录页模板");
  await page.getByRole("button", { name: "登录", exact: true }).click();
  await expect(page.getByText("请输入账号", { exact: true })).toBeVisible();
  const passwordError = page.getByText("请输入密码", { exact: true });
  await expect(passwordError).toBeVisible();
  await expect(async () => {
    const errorBox = await passwordError.boundingBox();
    const buttonBox = await page
      .getByRole("button", { name: "登录", exact: true })
      .boundingBox();
    expect(errorBox).not.toBeNull();
    expect(buttonBox).not.toBeNull();
    if (errorBox && buttonBox) {
      expect(buttonBox.y - errorBox.y - errorBox.height).toBeGreaterThanOrEqual(
        8,
      );
    }
  }).toPass();
  await page.getByLabel("账号", { exact: true }).fill("preview");
  await page.getByLabel("密码", { exact: true }).fill("example-only");
  await page.getByRole("button", { name: "显示密码" }).focus();
  await page.keyboard.press("Enter");
  await expect(page.getByLabel("密码", { exact: true })).toHaveAttribute(
    "type",
    "text",
  );
  await page.getByRole("button", { name: "隐藏密码" }).click();
  await expect(page.getByLabel("密码", { exact: true })).toHaveAttribute(
    "type",
    "password",
  );
  await page.getByLabel("密码", { exact: true }).press("Enter");
  await expect(page.getByLabel("账号", { exact: true })).toBeDisabled();
  await expect(page.getByText("这是模板预览，尚未连接登录服务")).toBeVisible();
  await expect(page.getByLabel("账号", { exact: true })).toHaveValue("preview");
  expect(errors).toEqual([]);
});

test("模拟成功不存储凭据", async ({ page }) => {
  await page.goto("/?demo=success");
  await page.getByLabel("账号", { exact: true }).fill("preview");
  await page.getByLabel("密码", { exact: true }).fill("example-only");
  await page.getByRole("button", { name: "登录", exact: true }).click();
  await expect(page.getByText("登录成功", { exact: true })).toBeVisible();
  expect(
    await page.evaluate(() => localStorage.length + sessionStorage.length),
  ).toBe(0);
});

for (const [width, height] of [
  [1024, 640],
  [1280, 720],
  [1440, 900],
  [1586, 992],
  [1920, 1080],
  [375, 812],
  [720, 450],
]) {
  test(`视口 ${width} × ${height} 无横向溢出`, async ({ page }) => {
    await page.setViewportSize({ width, height });
    await page.goto("/");
    await page.evaluate(() => document.fonts.ready);
    if (width <= 760) {
      await expect(
        page.getByText("SEEK THE WAY YOU WANT.", { exact: true }),
      ).toBeVisible();
      await expect(
        page.getByText("LIVE THE LIFE YOU FOUND.", { exact: true }),
      ).toBeVisible();
    }
    await expect(
      page.getByRole("heading", { name: "登录工作台" }),
    ).toBeVisible();
    expect(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= innerWidth,
      ),
    ).toBe(true);
    await page
      .getByRole("button", { name: "登录", exact: true })
      .scrollIntoViewIfNeeded();
    await expect(
      page.getByRole("button", { name: "登录", exact: true }),
    ).toBeInViewport();
  });
}
