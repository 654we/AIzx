# API 文档（Phase 1 初版）

## 通用说明
- Base URL: `http://localhost:8000`
- 认证方式：Bearer Token（JWT）
- 统一错误返回：
```json
{ "detail": "错误信息" }
```
- 需要认证的接口在 Header 中携带：
```
Authorization: Bearer <token>
```
- 健康检查：
  - GET /api/health

## 认证
### POST /api/auth/register
- 说明：账号密码注册（Phase 2 完善）
- Body:
```json
{ "username": "string", "password": "string" }
```
- Response:
```json
{ "access_token": "jwt", "token_type": "bearer" }
```

### POST /api/auth/login
- 说明：账号密码登录（Phase 1 提供骨架）
- Body:
```json
{ "username": "string", "password": "string" }
```
- Response:
```json
{ "access_token": "jwt", "token_type": "bearer" }
```

### POST /api/auth/wechat_login
- 说明：微信登录（需要配置 wechat_appid / wechat_secret）
- Body:
```json
{ "code": "string" }
```
- Response:
```json
{ "access_token": "jwt", "token_type": "bearer" }
```

## 用户
### GET /api/user/profile
- 说明：获取用户信息
- Response:
```json
{ "id": 1, "username": "string", "location": "string", "email": "", "phone": "", "avatar_url": "", "subscriptions": [] }
```

### PUT /api/user/profile
- 说明：更新用户资料
- Body:
```json
{ "username": "string", "location": "string", "email": "", "phone": "", "avatar_url": "" }
```

### PUT /api/user/location
- 说明：更新用户地区
- Body:
```json
{ "location": "string" }
```

### PUT /api/user/subscriptions
- 说明：更新订阅标签
- Body:
```json
{ "tags": ["tag1", "tag2"] }
```

### GET /api/user/subscriptions
- 说明：获取订阅标签
- Response:
```json
{ "tags": ["tag1", "tag2"] }
```

### PUT /api/user/password
- 说明：修改密码
- Body:
```json
{ "old_password": "string", "new_password": "string" }
```

## 资讯
### GET /api/news?page=&page_size=
- 说明：需登录后调用；默认按用户订阅标签过滤
- Response:
```json
{
  "items": [],
  "page": 1,
  "page_size": 10,
  "has_more": false
}
```

## 天气
### GET /api/weather?location=
- Response:
```json
{
  "location": { "name": "", "lat": 0.0, "lon": 0.0 },
  "weather": { "condition": "", "temp_c": 0, "humidity": 0, "wind": "", "aqi": 0, "aqi_desc": "", "updated_at": "" },
  "travel_advice": []
}
```
- 说明：location 为城市名称，例如 `上海`

## 日程
### POST /api/schedule/upload
- 说明：上传日程文件（txt/md/csv，<=2MB）
- Header: Authorization Bearer token
- FormData:
  - file: 文件
- Response: 固定格式日程 JSON

### GET /api/schedule/latest
- 说明：获取最新日程
- Header: Authorization Bearer token

## 管理后台
### GET /admin/login
### POST /admin/login
### GET /admin/logout
### GET/POST /admin/settings
- 配置项（摘要）：微信配置、天气配置、资讯抓取开关与来源模式、MCP 配置、AI Provider 配置、AI 路由策略
### GET /admin/users
### GET/POST /admin/news
- 说明：手动新增资讯，可选自动摘要

---

# 增量更新（修复/增强计划）

> 以下为本次修复/增强的新增或改造接口草案，确保前后端字段一致，均为兼容扩展。\n

## 通用错误码
- 400：参数错误\n- 401：未授权\n- 404：资源不存在\n- 409：冲突（例如重复）\n- 500：内部错误\n- 502：第三方服务错误\n
## 资讯概况
### GET /api/news/{news_id}/preview
- 说明：生成并缓存资讯概况\n- Response:\n```json
{
  "title": "string",
  "summary": "string",
  "key_points": ["string"],
  "source_url": "string",
  "fetched_at": "2024-01-01T09:00:00+08:00"
}
```

### POST /api/news/preview
- 说明：直接传入 URL 获取概况\n- Body:\n```json
{ "url": "https://example.com/article" }
```
- Response 同上

## 日程上传（增强）
### POST /api/schedule/upload
- 说明：支持 doc/docx/xls/xlsx/csv/txt/md\n- FormData:\n  - file: 文件\n- Response（固定格式）:\n```json
{
  "meta": { "source_filename": "", "generated_at": "", "timezone": "Asia/Shanghai", "version": "1.0" },
  "week": [
    { "date": "YYYY-MM-DD", "day_of_week": 1, "blocks": [{ "start": "HH:MM", "end": "HH:MM", "title": "", "location": "", "type": "study|work|life|health|other", "notes": "" }] }
  ],
  "tips": ["", ""]
}
```

## 用户资料与订阅
### GET /api/user/profile
### PUT /api/user/profile
- Body:\n```json
{ "username": "string", "location": "string", "avatar_url": "string" }
```

### GET /api/user/subscriptions
### PUT /api/user/subscriptions
- Body:\n```json
{ "tags": ["tag1", "tag2"] }
```

### PUT /api/user/password
- Body:\n```json
{ "old_password": "string", "new_password": "string" }
```

## 管理后台（任务触发）
### POST /admin/api/tasks/news_crawl
- Body:\n```json
{ "user_id": 1, "limit": 20 }
```
- Response:\n```json
{ "status": "success", "duration_ms": 1200, "error_message": "", "log_excerpt": "", "task_run_id": 1 }
```

### POST /admin/api/tasks/weather_refresh
- Body:\n```json
{ "location": "上海" }
```

### POST /admin/api/tasks/schedule_analyze
- Body:\n```json
{ "upload_id": 1 }
```

## 定时任务配置
### GET /admin/api/scheduler
### PUT /admin/api/scheduler
- Body:\n```json
{
  "news_crawler_enabled": true,
  "cron": "0 */1 * * *",
  "interval_minutes": 30,
  "limit": 20,
  "sources": { "rss": true, "mcp": false, "feeds": true }
}
```
- Response:\n```json
{ "next_run_at": "2024-01-01T09:00:00+08:00", "last_runs": [] }
```

## MCP 远程配置
### GET /admin/api/mcp/remotes
### POST /admin/api/mcp/remotes
### PUT /admin/api/mcp/remotes/{id}
### DELETE /admin/api/mcp/remotes/{id}
- Schema:\n```json
{ "name": "", "base_url": "", "protocol": "http|streamable_http", "auth_type": "api_key|token|none", "auth_value": "", "timeout_sec": 10, "enabled": true, "priority": 1 }
```

### POST /admin/api/mcp/remotes/{id}/test
- Response:\n```json
{ "status": "success", "duration_ms": 500, "error_message": "" }
```

## MCP 本地插件
### GET /admin/api/mcp/locals
### POST /admin/api/mcp/locals
### PUT /admin/api/mcp/locals/{id}
### DELETE /admin/api/mcp/locals/{id}
- Schema:\n```json
{ "name": "", "module_path": "app.mcp.providers.demo", "capabilities": ["search"], "schema": {}, "timeout_sec": 10, "enabled": true, "priority": 1 }
```

### POST /admin/api/mcp/locals/{id}/test
- Response:\n```json
{ "status": "success", "duration_ms": 300, "error_message": "" }
```

## 天气 Provider 管理
### GET /admin/api/weather/providers
### POST /admin/api/weather/providers
### PUT /admin/api/weather/providers/{id}
### DELETE /admin/api/weather/providers/{id}
- Schema:\n```json
{ "name": "", "provider_type": "open-meteo|gaode|qweather|baidu", "base_url": "", "api_key": "", "timeout_sec": 5, "enabled": true, "priority": 1, "extra_config": {} }
```

### POST /admin/api/weather/providers/{id}/test
- Response:\n```json
{ "status": "success", "provider": "gaode", "duration_ms": 800, "error_message": "", "failover_count": 0 }
```

## 管理后台用户 CRUD
### GET /admin/api/users
### GET /admin/api/users/{id}
### POST /admin/api/users
### PUT /admin/api/users/{id}
### DELETE /admin/api/users/{id}
- Response 示例:\n```json
{ "id": 1, "username": "", "location": "", "subscriptions": ["tag1"], "is_active": true }
```
