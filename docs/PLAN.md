# 项目规划文档（Phase 1 初版）

## 1. 架构概览
- 前端：UniApp（Vue2，目录 `/AIx2`），底部 Tab：资讯/天气/日程/我的。
- 后端：FastAPI + SQLite + SQLAlchemy，提供 REST API + 管理后台入口（Phase 1 先提供基础接口骨架）。
- AI 模块：提供统一 Provider 抽象（Phase 2+ 实现），支持 DeepSeek / GLM / OpenAI 兼容接口。
- 任务调度：APScheduler（Phase 4+）。
- 配置：`.env` + 数据库存储配置（Phase 2+ 完善）。

## 2. 目录结构
```
/AIx2/                 # UniApp 工程（必须在此开发）
/backend/              # Python 后端
  app/
    main.py
    config.py
    database.py
    models.py
    schemas.py
    auth.py
    crud.py
  requirements.txt
  scripts/
/docs/
  PLAN.md
  PROGRESS.md
  API.md
  ADMIN_GUIDE.md       # Phase 6
  USER_GUIDE.md        # Phase 6
/scripts/              # Windows 启动/初始化脚本（Phase 2+）
```

## 3. 数据流（概览）
1. 前端登录获取 token（账号密码/微信）。
2. 前端请求资讯/天气/日程接口，后端读取配置与数据库。
3. 资讯：定时任务拉取 -> 清洗去重 -> 入库 -> 分页返回。
4. 天气：调用第三方天气接口 -> 生成出行建议 -> 返回前端。
5. 日程：上传文档 -> AI 解析 -> 生成固定格式日程 JSON -> 返回前端并存档。

## 4. 接口清单（Phase 1 先定义）
- POST /api/auth/register
- POST /api/auth/login
- POST /api/auth/wechat_login
- GET  /api/user/profile
- PUT  /api/user/location
- PUT  /api/user/subscriptions
- GET  /api/news?page=&page_size=
- GET  /api/weather?location=
- POST /api/schedule/upload
- GET  /api/schedule/latest
- /admin/login
- /admin/settings
- /admin/users

## 5. 阶段拆解
### Phase 1（骨架与基础）
- 文档：`docs/PLAN.md`、`docs/API.md` 初版。
- 后端：FastAPI 启动、数据库模型、管理员初始化（admin/admin）、基础鉴权（JWT）。
- 前端：Tab 四页骨架 + 基础 UI 布局。
- 输出：`docs/PROGRESS.md` 记录。

### Phase 2（登录注册）
- 登录注册、微信登录接口。
- 前端登录/注册页面、token 持久化、退出登录。

### Phase 3（天气）
- 天气接口对接 + 出行建议。
- 位置设置页面。

### Phase 4（资讯）
- 订阅标签、订阅链接、爬虫开关、定时拉取、分页接口。

### Phase 5（日程）
- 上传解析 -> 固定格式日程生成 -> 课表渲染。

### Phase 6（管理后台完善）
- AI 接口管理、路由策略、配置管理、用户管理。
- docs/ADMIN_GUIDE.md、docs/USER_GUIDE.md。

## 6. 验收标准（Phase 1）
- `docs/PLAN.md`、`docs/API.md` 完整可读。
- 后端可启动并返回健康信息。
- 管理员账号初始化为 admin/admin。
- 前端四个 Tab 页面可进入且布局稳定。

## 7. 风险与回滚
- 风险：第三方 API 失败、AI 接口超时、微信登录需要真实 AppID。
- 回滚：保留基础接口与可启动状态；配置改动以 `.env` 回退。

## 8. Windows 命令行说明
- 后端启动（PowerShell）：
  ```powershell
  cd backend
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  pip install -r requirements.txt
  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
  ```
- 前端启动（HBuilderX 运行到模拟器/真机），或使用 uni-app CLI（如已配置）：
  ```powershell
  cd AIx2
  # 使用 HBuilderX 运行，或根据团队 CLI 配置运行
  ```

## 9. 假设与可替代方案
- 假设：FastAPI 在 Windows 环境可用；若出现兼容问题，替代为 Flask。
- 假设：前端使用 uni-ui 组件库；如需要更丰富组件，替代为 uView（需补充安装步骤）。
