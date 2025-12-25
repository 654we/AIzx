# 管理后台使用说明

## 1. 登录
1. 启动后端服务：`uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
2. 浏览器访问：`http://localhost:8000/admin/login`
3. 使用初始账号登录：
   - 账号：`admin`
   - 密码：`admin`

## 2. 系统设置
进入【系统设置】可配置：
- 微信登录 AppID/Secret
- 天气接口地址
- 资讯抓取开关（true/false）
- 订阅链接（逗号分隔）
- AI 接口配置（DeepSeek / GLM / OpenAI 兼容）
- AI 路由策略（资讯/天气/日程可选择不同 provider）

说明：
- 当未配置 API Key 时将自动回退为规则/占位生成。

保存后将写入数据库，可用于后续功能调用。

## 3. 用户管理
进入【用户管理】可查看用户列表：
- 用户 ID
- 账号
- 是否管理员
- 位置

## 4. 安全建议
- 首次使用后请修改管理员密码。
- 生产环境建议配置独立的 `admin_session_secret`。
