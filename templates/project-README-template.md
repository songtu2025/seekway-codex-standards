# 项目名称

## 1. 项目用途

说明本项目解决的业务问题和主要用户。

## 2. 适用范围

说明项目适用的业务范围、用户范围和运行环境。

## 3. 明确不做

- 待填写。
- 待填写。
- 待填写。

## 4. 关键业务规则

以下规则属于项目级业务契约，任何开发和重构不得破坏：

1. 待填写。
2. 待填写。
3. 待填写。

## 5. 技术栈

### 前端

- React
- TypeScript
- Vite

### 后端

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- Alembic

### 部署

- Docker
- Docker Compose
- Nginx
- 阿里云 ECS

## 6. 系统架构

说明前端、API、数据库、Worker 和外部系统之间的关系。

## 7. Web 界面规范

本项目界面规范位于 `docs/web-ui-standard.md`。

- 主要场景：公司内部和后台业务系统。
- 主题令牌：`frontend/src/styles/seekway-theme.css`，并且只在全局样式入口导入一次。
- 组件库：待填写；没有时填写“无”，不得由 Codex 自行引入。
- 图标体系：待填写。
- 主要支持视口：待填写。
- 公司设计来源：[SEEKWAY Web UI Kit V1.2.0](https://www.figma.com/design/eed9GukOv7zM7n04Lu1xUl)。
- 项目设计来源：待填写，例如项目 Figma、现有设计系统或相似页面。
- 页面模板：仅作为参考起点，可按业务组合，不要求整页套用。

## 8. 项目结构

说明主要目录及其职责。

## 9. 本地开发

说明 Windows 环境下的依赖安装和启动方式。

## 10. 测试与检查

项目应保留 Windows 和 Linux / CI 两套检查入口，并保持检查内容一致。

Windows 统一检查入口：

```powershell
.\scripts\check.ps1
```

Linux 或 CI 检查入口：

```bash
./scripts/check.sh
```

## 11. 配置说明

复制 `.env.example` 创建本地 `.env`。

不得将 `.env` 或真实凭据提交到仓库。

## 12. 部署说明

生产环境由部署负责人统一操作。

部署步骤、数据库迁移和回滚方式记录在 `docs/deployment`。
