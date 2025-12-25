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
{ "id": 1, "username": "string", "location": "string", "subscriptions": [] }
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
### /admin/login
### /admin/settings
### /admin/users
### /admin/logout
### /admin/news
