# 进度记录

## Phase 1
- 状态：已完成
- 完成内容：
  - 输出 docs/PLAN.md 与 docs/API.md 初版
  - FastAPI 后端骨架（JWT/SQLite/管理员初始化）
  - UniApp 前端四个 Tab 页面骨架
- 文件清单：
  - docs/PLAN.md
  - docs/API.md
  - docs/PROGRESS.md
  - backend/requirements.txt
  - backend/app/config.py
  - backend/app/database.py
  - backend/app/models.py
  - backend/app/schemas.py
  - backend/app/auth.py
  - backend/app/crud.py
  - backend/app/deps.py
  - backend/app/main.py
  - AIx2/pages.json
  - AIx2/pages/news/index.vue
  - AIx2/pages/weather/index.vue
  - AIx2/pages/schedule/index.vue
  - AIx2/pages/mine/index.vue
  - AIx2/static/tab/*.png
- 下一步：
  - Phase 2 登录/注册与微信登录接口
  - 前端登录/注册页面与 token 持久化
- 遗留问题：
  - 管理后台界面待实现
  - 真实图标待替换

## Phase 2
- 状态：已完成
- 完成内容：
  - 账号密码注册/登录接口
  - 微信登录接口（需要配置 wechat_appid / wechat_secret）
  - 前端登录/注册页面与 token 持久化
- 文件清单：
  - backend/requirements.txt
  - backend/app/config.py
  - backend/app/models.py
  - backend/app/schemas.py
  - backend/app/crud.py
  - backend/app/main.py
  - AIx2/pages/auth/login.vue
  - AIx2/pages/auth/register.vue
  - AIx2/pages/mine/index.vue
  - AIx2/pages.json
  - AIx2/utils/request.js
  - docs/API.md
- 下一步：
  - Phase 3 天气接口与位置设置
- 遗留问题：
  - 微信登录需配置真实 AppID/Secret

## Phase 3
- 状态：已完成
- 完成内容：
  - 天气接口对接与出行建议生成（Open-Meteo）
  - 位置设置页面与天气页联动
- 文件清单：
  - backend/app/config.py
  - backend/app/main.py
  - backend/app/schemas.py
  - AIx2/pages/location/index.vue
  - AIx2/pages/weather/index.vue
  - AIx2/pages/mine/index.vue
  - AIx2/pages.json
  - docs/API.md
- 下一步：
  - Phase 4 资讯聚合与订阅标签管理
- 遗留问题：
  - 天气接口无 AQI 数据源，当前使用默认 AQI 占位值

## Phase 4
- 状态：已完成
- 完成内容：
  - 资讯分页接口与订阅标签过滤
  - 前端资讯列表拉取与详情跳转
- 文件清单：
  - backend/app/models.py
  - backend/app/schemas.py
  - backend/app/crud.py
  - backend/app/main.py
  - AIx2/pages/news/index.vue
  - AIx2/pages/webview/index.vue
  - AIx2/pages.json
  - docs/API.md
- 下一步：
  - Phase 5 日程上传与课表渲染
- 遗留问题：
  - 资讯聚合抓取与定时任务待实现

## Phase 5
- 状态：已完成
- 完成内容：
  - 日程文件上传与固定格式日程返回
  - 前端日程页上传与课表渲染
- 文件清单：
  - backend/app/models.py
  - backend/app/schemas.py
  - backend/app/crud.py
  - backend/app/main.py
  - AIx2/pages/schedule/index.vue
  - docs/API.md
- 下一步：
  - Phase 6 管理后台完善
- 遗留问题：
  - 日程解析与 AI 生成逻辑待补充

## Phase 6
- 状态：已完成
- 完成内容：
  - 管理后台登录、系统设置、用户管理页面
  - 基于数据库的配置持久化
  - 新增管理后台使用与用户说明文档
- 文件清单：
  - backend/app/config.py
  - backend/app/models.py
  - backend/app/crud.py
  - backend/app/main.py
  - backend/app/templates/admin_login.html
  - backend/app/templates/admin_settings.html
  - backend/app/templates/admin_users.html
  - backend/requirements.txt
  - docs/ADMIN_GUIDE.md
  - docs/USER_GUIDE.md
  - docs/PROGRESS.md
- 下一步：
  - 补充 AI 路由策略与配置项详情
  - 对接 AI 生成逻辑

## Phase 7
- 状态：已完成
- 完成内容：
  - AI Provider 抽象与路由策略接入天气/日程
  - AI 配置项在管理后台可编辑
- 文件清单：
  - backend/app/ai.py
  - backend/app/ai_router.py
  - backend/app/main.py
  - backend/app/templates/admin_settings.html
  - docs/ADMIN_GUIDE.md
  - docs/PROGRESS.md
- 下一步：
  - 资讯聚合与 AI 摘要整合

## Phase 8
- 状态：已完成
- 完成内容：
  - 管理后台新增资讯管理与 AI 摘要生成
- 文件清单：
  - backend/app/main.py
  - backend/app/templates/admin_news.html
  - backend/app/templates/admin_settings.html
  - backend/app/templates/admin_users.html
  - docs/ADMIN_GUIDE.md
  - docs/API.md
  - docs/PROGRESS.md
- 下一步：
  - 资讯自动抓取与定时任务

## Phase 9
- 状态：已完成
- 完成内容：
  - 资讯 RSS 抓取与定时任务
  - 自动摘要接入 AI Provider（可降级）
- 文件清单：
  - backend/app/news_crawler.py
  - backend/app/main.py
  - backend/app/crud.py
  - backend/requirements.txt
  - docs/ADMIN_GUIDE.md
  - docs/PROGRESS.md
- 下一步：
  - 完善 MCP 搜索与爬虫模式

## Phase 10
- 状态：已完成
- 完成内容：
  - MCP 搜索配置与来源模式配置
  - MCP 搜索占位实现与后台可配置
- 文件清单：
  - backend/app/mcp_search.py
  - backend/app/main.py
  - backend/app/templates/admin_settings.html
  - docs/ADMIN_GUIDE.md
  - docs/PROGRESS.md
- 下一步：
  - 对接真实 MCP 搜索与数据解析

## Phase 11
- 状态：已完成
- 完成内容：
  - MCP 搜索关键词配置与实际请求调用
  - MCP 搜索结果入库与去重
- 文件清单：
  - backend/app/mcp_search.py
  - backend/app/main.py
  - backend/app/templates/admin_settings.html
  - docs/ADMIN_GUIDE.md
  - docs/PROGRESS.md
- 下一步：
  - 完善 MCP 返回格式校验与错误告警

## Phase 12
- 状态：已完成
- 完成内容：
  - MCP 搜索响应结构校验与异常日志
- 文件清单：
  - backend/app/mcp_search.py
  - docs/PROGRESS.md
- 下一步：
  - 增加告警/通知机制

## Fix Phase 1
- 状态：已完成
- 完成内容：
  - 输出 docs/PLAN_FIX.md（本轮修复增强规划）
  - 更新 docs/API.md 增量接口草案
  - 提供接口一致性清单（PLAN_FIX 中）
- 文件清单：
  - docs/PLAN_FIX.md
  - docs/API.md
  - docs/PROGRESS.md
- 下一步：
  - Phase 2 管理后台增强（手动触发、定时任务、用户 CRUD、MCP/天气配置）
- 风险：
  - 后续接口变更需严格同步前端与文档
