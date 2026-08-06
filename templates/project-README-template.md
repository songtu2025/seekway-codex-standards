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

## 7. 项目结构

说明主要目录及其职责。

## 8. 本地开发

说明 Windows 环境下的依赖安装和启动方式。

## 9. 测试与检查

Windows 统一检查入口：

```powershell
.\scripts\check.ps1
```

Linux 或 CI 检查入口：

```bash
./scripts/check.sh
```

## 10. 配置说明

复制 `.env.example` 创建本地 `.env`。

不得将 `.env` 或真实凭据提交到仓库。

## 11. 部署说明

生产环境由部署负责人统一操作。

部署步骤、数据库迁移和回滚方式记录在 `docs/deployment`。
