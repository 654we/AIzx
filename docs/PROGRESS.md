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

## Fix Phase 2
- 状态：已完成
- 完成内容：
  - 管理后台新增任务触发、定时任务配置、MCP 管理、天气 Provider 管理页面
  - 新增 admin API：任务触发、scheduler 配置、MCP/天气/用户 CRUD
  - MCP 远程配置支持多实例与测试，本地插件支持注册与测试
  - 用户管理支持搜索、详情、启用/停用、重置密码、订阅标签编辑
- 文件清单：
  - backend/app/main.py
  - backend/app/models.py
  - backend/app/crud.py
  - backend/app/schemas.py
  - backend/app/mcp/registry.py
  - backend/app/mcp/providers/demo.py
  - backend/app/mcp/providers/__init__.py
  - backend/app/mcp/__init__.py
  - backend/app/news_crawler.py
  - backend/app/mcp_search.py
  - backend/app/templates/admin_settings.html
  - backend/app/templates/admin_users.html
  - backend/app/templates/admin_news.html
  - backend/app/templates/admin_tasks.html
  - backend/app/templates/admin_scheduler.html
  - backend/app/templates/admin_mcp.html
  - backend/app/templates/admin_weather.html
  - backend/app/templates/admin_user_detail.html
  - docs/PROGRESS.md
- 下一步：
  - Phase 3 天气多 Provider failover + 国内 Provider 落地
- 风险：
  - Cron 表达式需管理员正确输入，否则调度创建可能失败

## Fix Phase 3
- 状态：已完成
- 完成内容：
  - 天气 Provider 抽象接入 failover（按优先级依次尝试）
  - 默认注入 Open-Meteo 与高德天气模板（高德默认禁用，需配置 key）
  - 天气 Provider 测试改为真实调用并支持 test_location
- 文件清单：
  - backend/app/main.py
  - backend/app/templates/admin_weather.html
  - docs/PROGRESS.md
- 下一步：
  - Phase 4 资讯详情改造（preview 概况 + 前端详情页）
- 风险：
  - 高德/第三方 Provider 需要有效 key 才可用

## Fix Phase 4
- 状态：已完成
- 完成内容：
  - 新增资讯预览接口并支持缓存（news_id 或 url）
  - 前端资讯详情改为展示智能概况 + 来源链接与操作按钮
- 文件清单：
  - backend/app/main.py
  - backend/app/models.py
  - backend/app/crud.py
  - backend/app/schemas.py
  - AIx2/pages/news/index.vue
  - AIx2/pages/news/detail.vue
  - AIx2/pages.json
  - docs/PROGRESS.md
- 下一步：
  - Phase 5 日程文件上传增强（doc/docx/xls/xlsx/csv）
- 风险：
  - 资讯源站访问受限时预览可能失败，需要前端提示与重试

## Fix Phase 5
- 状态：已完成
- 完成内容：
  - 日程上传支持 doc/docx/xls/xlsx/csv/txt/md 解析与元数据记录
  - 后端增加文本解析与日程校验排序逻辑
  - 前端上传扩展格式并显示上传进度
- 文件清单：
  - backend/requirements.txt
  - backend/app/models.py
  - backend/app/crud.py
  - backend/app/main.py
  - AIx2/pages/schedule/index.vue
  - docs/PROGRESS.md
- 下一步：
  - Phase 6 我的页面补齐（资料编辑 + 订阅标签管理）
- 风险：
  - .doc 文档解析为兼容兜底，复杂格式可能解析不完整

## Fix Phase 6
- 状态：已完成
- 完成内容：
  - 新增账号信息编辑与订阅标签管理页面入口
  - 后端支持用户资料更新、订阅标签获取与密码修改
  - 用户模型补充邮箱/手机号/头像链接字段
- 文件清单：
  - backend/app/models.py
  - backend/app/schemas.py
  - backend/app/crud.py
  - backend/app/main.py
  - AIx2/pages/mine/index.vue
  - AIx2/pages/mine/profile.vue
  - AIx2/pages/mine/subscriptions.vue
  - AIx2/pages.json
  - docs/API.md
  - docs/PROGRESS.md
- 下一步：
  - 全链路回归自测与文档补齐（如需）
- 风险：
  - 用户名冲突将返回 409，需要前端提示

## Fix Phase 7
- 状态：已完成
- 完成内容：
  - 定时任务配置对无效 cron 做容错并回退到间隔模式
  - 管理后台显示调度错误提示
- 文件清单：
  - backend/app/main.py
  - backend/app/templates/admin_scheduler.html
  - docs/PROGRESS.md
- 下一步：
  - 继续全链路回归测试与缺陷修复
- 风险：
  - 需在后台提示管理员修正 cron 表达式

## Fix Phase 8
- 状态：已完成
- 完成内容：
  - MCP 远程配置新增 protocol 字段（支持 http 与 streamable_http）
  - MCP 搜索支持解析 streamable_http 流式响应
- 文件清单：
  - backend/app/models.py
  - backend/app/schemas.py
  - backend/app/crud.py
  - backend/app/main.py
  - backend/app/mcp_search.py
  - backend/app/templates/admin_mcp.html
  - docs/API.md
  - docs/PROGRESS.md
- 下一步：
  - 验证第三方 MCP 流式返回结构与字段映射
- 风险：
  - 远程 MCP 响应格式不符合 items 结构会导致解析失败
