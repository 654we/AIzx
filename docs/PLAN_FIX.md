# 修复/增强规划文档（PLAN_FIX）

## 0. 背景与目标
本轮针对“后端 + 管理后台 + 前端”进行系统性补全与修复，确保**接口与字段全链路一致**，并在不破坏现有功能的前提下完成以下目标：
- 管理后台可配置、可测试、可观测（任务手动触发、定时、用户 CRUD、MCP/天气配置）。
- 资讯阅读体验改为“后端读取并生成概况”，前端展示概况并保留来源链接与操作。
- 日程文件上传支持 doc/docx/xls/xlsx/csv，后端解析 + 智能输出 + 校验，前端课表渲染。
- 我的页面补齐资料编辑与订阅标签管理。
- MCP（远程 + 本地）配置与插件式注册，提供后台连通性测试。
- 天气多 Provider failover，提供国内可用 Provider（高德/和风等）。

> 约束：UI 不出现显眼“AI”字样（用“智能概况/今日提示/出行建议”等替代）。

---

## 1. 现状扫描摘要
- 后端已具备：JWT 登录、资讯分页、天气查询（Open-Meteo）、日程上传（txt/md/csv）、基础管理后台（登录/设置/用户/资讯）。
- 前端已具备：Tab 页面骨架、资讯列表与 webview、天气页、日程页（上传/课表）、我的页（入口有限）。
- 缺口：手动触发/定时配置、MCP 类型细化、多 Provider 天气、后台 CRUD 细化、资讯详情概况化、日程上传格式扩展、我的页编辑与订阅管理。

---

## 2. 数据模型补齐（建议新增/调整）
> 以 SQLAlchemy + SQLite 为基础，新增表为主，保持旧表兼容。

### 2.1 新增表
1) `task_runs`
- 字段：
  - id, task_type, status(success/failed), duration_ms, error_message, log_excerpt, payload_json, created_at
- 用途：记录手动触发与定时任务执行结果（可用于后台列表）。

2) `news_previews`
- 字段：
  - id, news_id(可空), source_url, title, summary, key_points(JSON), fetched_at, cache_ttl_sec
- 用途：资讯概况缓存，避免重复抓取。

3) `schedule_uploads`
- 字段：
  - id, user_id, filename, file_type, file_size, stored_path, status, parsed_text, created_at
- 用途：记录上传元数据与解析文本，关联 latest 输出。

4) `weather_providers`
- 字段：
  - id, name, provider_type(open-meteo/gaode/qweather/baidu), base_url, api_key, timeout_sec,
  - enabled, priority, extra_config(JSON)
- 用途：多 Provider 与 failover 配置。

5) `mcp_remote_configs`
- 字段：
  - id, name, base_url, auth_type(api_key/token/none), auth_value, timeout_sec,
  - enabled, priority

6) `mcp_local_plugins`
- 字段：
  - id, name, module_path, capabilities(JSON), schema(JSON), timeout_sec, enabled, priority

7) `user_subscriptions`
- 字段：
  - id, user_id, tag, enabled
- 用途：从 users.subscriptions 迁移为规范化结构（保留兼容字段，双写同步）。

### 2.2 兼容策略
- 旧字段 `users.subscriptions` 继续保留；读写时同步 `user_subscriptions`。
- `weather`/`news`/`schedule` 原响应字段保持不变，新增字段只做**兼容性扩展**。

---

## 3. 后端功能设计

### 3.1 任务手动触发
- 新增接口：
  - `POST /admin/api/tasks/news_crawl`
  - `POST /admin/api/tasks/weather_refresh`
  - `POST /admin/api/tasks/schedule_analyze`
- 返回：`status`、`duration_ms`、`error_message`、`log_excerpt`、`task_run_id`。
- 任务执行时记录 `task_runs`。

### 3.2 资讯定时任务配置
- 调度器：APScheduler（BackgroundScheduler）
- 后台配置项：
  - cron/interval 表达式
  - enable 开关
  - 每次抓取条数上限、来源开关（RSS/MCP/订阅链接）
- 管理后台显示：下次执行时间、最近执行记录。

### 3.3 MCP（远程 + 本地）
- **远程 MCP**：多配置、优先级、鉴权方式，支持健康检查。
- **本地 MCP**：插件式注册（`backend/app/mcp/providers/*.py`）。
- 插件需声明：name、capabilities、schema、timeout。
- 管理后台：增删改查、启用/禁用、测试连通性。

### 3.4 天气多 Provider failover
- 抽象 `WeatherProvider`，基于优先级依次调用。
- 失败自动切换：超时/HTTP/解析错误。
- 记录 provider、失败原因、切换次数到 `task_runs`。
- 国内 Provider：优先落地高德/和风（可直接使用 key），百度仅提供配置模板（可选）。

### 3.5 用户管理 CRUD
- 管理后台支持：列表、详情、搜索、启用/禁用、重置密码、软删除。
- 支持编辑订阅标签与地区。

### 3.6 资讯预览（概况）
- 新增：`/api/news/preview` 或 `/api/news/{id}/preview`
- 后端读取网页并生成摘要/要点，支持缓存。
- 返回字段：`title, summary, key_points, source_url, fetched_at`。

### 3.7 日程文件上传增强
- 支持扩展格式：`doc/docx/xls/xlsx/csv`。
- 解析文本：`python-docx` + `openpyxl` + 内置 `csv`。
- AI 生成固定日程 JSON + 校验/冲突处理。
- 存储 latest，供前端渲染。

### 3.8 用户资料与订阅管理
- 新增/完善接口：
  - `GET/PUT /api/user/profile`
  - `GET/PUT /api/user/subscriptions`
  - `PUT /api/user/password`
- 前端新增“账号信息编辑页”“订阅标签管理页”。

---

## 4. 管理后台页面规划
1) 任务测试/触发页
- 新闻抓取 / 天气刷新 / 日程分析，一键触发
- 列表展示最近执行记录

2) 定时任务配置页
- cron/interval 编辑
- 下次执行时间

3) MCP 管理页
- 远程 MCP 列表、启用、测试
- 本地 MCP 列表、启用、注册说明

4) 天气 Provider 管理页
- 新增/编辑 Provider
- 测试调用结果

5) 用户管理页增强
- CRUD + 订阅标签编辑 + 软删除

---

## 5. 前端页面改动点
1) 资讯详情页
- 改为请求 `/api/news/:id/preview` 获取概况
- 底部保留：来源链接 + 复制 + 打开原文

2) 日程页
- 文件上传扩展：doc/docx/xls/xlsx/csv
- 显示上传进度与解析结果

3) 我的页
- 新增入口：资料编辑 / 订阅标签管理
- 支持修改昵称/密码/地区/订阅标签

---

## 6. 接口一致性清单（前后端对齐）
> 该清单确保字段一致、避免“只改一边”。

- 资讯列表页：
  - 后端 `/api/news` 返回 `items[].id/title/summary/source/url/published_at/tags`
  - 前端使用 `id` 打开详情 -> 调用 `/api/news/{id}/preview`

- 资讯详情页：
  - 后端 `preview` 返回 `title/summary/key_points/source_url/fetched_at`
  - 前端展示概况 + 源链接 + 复制/打开按钮

- 日程上传页：
  - 后端 `/api/schedule/upload` 返回 `meta/week/tips`
  - 前端依据 `week.blocks` 渲染课表

- 用户资料页：
  - 后端 `/api/user/profile` 返回 `id/username/location/subscriptions`
  - 前端可修改昵称/地区/密码，并同步 `subscriptions`

- 订阅标签页：
  - 后端 `/api/user/subscriptions` 返回 `tags` 列表
  - 前端新增/删除/选择后保存

- 天气页：
  - 后端 `/api/weather` 返回 `location/weather/travel_advice`
  - 前端保持字段一致显示

---

## 7. Phase 实施顺序
### Phase 1：文档与接口基线
- 输出 `docs/PLAN_FIX.md`
- 更新 `docs/API.md`
- 输出接口一致性清单

### Phase 2：管理后台增强
- 任务手动触发 + 定时任务配置
- MCP 管理 + 天气 Provider 管理 + 用户 CRUD

### Phase 3：天气多 Provider failover
- 抽象 Provider + failover + 国内 Provider 落地

### Phase 4：资讯详情改造
- 后端 preview + 前端详情页

### Phase 5：日程上传增强
- doc/docx/xls/xlsx/csv 解析 + 课表渲染

### Phase 6：我的页面补齐 + 回归
- 资料编辑 + 订阅标签管理
- 全链路自测与文档更新

---

## 8. 风险与缓解
- 第三方 API 失败：提供 failover + 超时 + 降级策略。
- MCP 远程不可用：后台提供测试与启停。
- AI 生成质量不稳定：后端校验兜底。
- UI 兼容：避免新增破坏字段，采用新增字段方式扩展。
