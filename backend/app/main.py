import json
import os
from datetime import datetime, timedelta

import httpx
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi import UploadFile
from fastapi import Form
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.ai_router import build_provider, get_route, provider_ready
from app.auth import create_access_token
from app.config import settings
from app.database import init_db
from app.deps import get_db

app = FastAPI(title=settings.app_name)
app.add_middleware(SessionMiddleware, secret_key=settings.admin_session_secret)
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))
security = HTTPBearer()


@app.on_event("startup")
def startup_event() -> None:
    init_db()
    db = next(get_db())
    try:
        admin = crud.get_user_by_username(db, "admin")
        if not admin:
            crud.create_user(db, "admin", "admin", is_admin=True)
        existing_news = db.query(models.NewsItem).count()
        if existing_news == 0:
            crud.create_news_item(
                db,
                title="欢迎使用资讯频道",
                summary="这里展示最新资讯内容，后续将接入订阅与抓取。",
                source="系统",
                url="https://example.com/welcome",
                published_at="2024-01-01T09:00:00+08:00",
                tags=["推荐"],
            )
    finally:
        db.close()


def fetch_wechat_openid(code: str) -> str:
    if not settings.wechat_appid or not settings.wechat_secret:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="WeChat config missing")
    params = {
        "appid": settings.wechat_appid,
        "secret": settings.wechat_secret,
        "js_code": code,
        "grant_type": "authorization_code",
    }
    try:
        response = httpx.get(settings.wechat_base_url, params=params, timeout=5.0)
        response.raise_for_status()
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="WeChat request failed") from exc
    data = response.json()
    if data.get("errcode"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=data.get("errmsg", "WeChat error"))
    openid = data.get("openid")
    if not openid:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="WeChat openid missing")
    return openid


def aqi_description(aqi: int) -> str:
    if aqi <= 50:
        return "优"
    if aqi <= 100:
        return "良"
    if aqi <= 150:
        return "轻度"
    if aqi <= 200:
        return "中度"
    if aqi <= 300:
        return "重度"
    return "严重"


def travel_advice_for(condition: str, temp_c: float, aqi: int) -> list[str]:
    advice = []
    if "雨" in condition:
        advice.append("短时有降水，建议随身携带雨具。")
    if temp_c >= 30:
        advice.append("气温偏高，外出注意防晒补水。")
    if temp_c <= 5:
        advice.append("气温较低，外出注意保暖。")
    if aqi > 100:
        advice.append("空气质量一般，敏感人群减少户外活动。")
    if not advice:
        advice.append("天气舒适，适合常规出行安排。")
    return advice[:2]


def travel_advice_from_ai(db: Session, condition: str, temp_c: float, aqi: int) -> list[str]:
    route = get_route(db, "ai_route_weather", "openai")
    if not provider_ready(db, route):
        return travel_advice_for(condition, temp_c, aqi)
    provider = build_provider(route, db)
    prompt = (
        "请根据以下天气信息给出两条简短出行建议，每条不超过20字："
        f"天气={condition}，温度={temp_c}C，AQI={aqi}。"
        "只返回用中文短句，每条建议一行。"
    )
    try:
        text = provider.generate(prompt)
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        return lines[:2] if lines else travel_advice_for(condition, temp_c, aqi)
    except Exception:
        return travel_advice_for(condition, temp_c, aqi)


def fetch_weather(db: Session, location: str) -> schemas.WeatherResponse:
    if not location:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Location required")
    try:
        geo_resp = httpx.get(
            settings.weather_geo_url,
            params={"name": location, "count": 1, "language": "zh", "format": "json"},
            timeout=5.0,
        )
        geo_resp.raise_for_status()
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Geo request failed") from exc
    geo_data = geo_resp.json()
    results = geo_data.get("results") or []
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Location not found")
    info = results[0]
    lat = info.get("latitude")
    lon = info.get("longitude")
    name = info.get("name")
    try:
        weather_resp = httpx.get(
            settings.weather_api_url,
            params={
                "latitude": lat,
                "longitude": lon,
                "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
                "timezone": "Asia/Shanghai",
            },
            timeout=5.0,
        )
        weather_resp.raise_for_status()
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Weather request failed") from exc
    weather_data = weather_resp.json()
    current = weather_data.get("current") or {}
    temp_c = float(current.get("temperature_2m", 0))
    humidity = int(current.get("relative_humidity_2m", 0))
    wind_speed = current.get("wind_speed_10m", 0)
    condition = "晴"
    weather_code = current.get("weather_code")
    if weather_code in {51, 53, 55, 61, 63, 65, 80, 81, 82}:
        condition = "雨"
    elif weather_code in {71, 73, 75, 85, 86}:
        condition = "雪"
    elif weather_code in {2, 3}:
        condition = "多云"
    aqi = 60
    aqi_desc = aqi_description(aqi)
    return schemas.WeatherResponse(
        location=schemas.WeatherLocation(name=name, lat=lat, lon=lon),
        weather=schemas.WeatherInfo(
            condition=condition,
            temp_c=temp_c,
            humidity=humidity,
            wind=f"{wind_speed} km/h",
            aqi=aqi,
            aqi_desc=aqi_desc,
            updated_at=current.get("time", ""),
        ),
        travel_advice=travel_advice_from_ai(db, condition, temp_c, aqi),
    )


def build_schedule_plan(source_filename: str) -> schemas.ScheduleResponse:
    today = datetime.now()
    week = []
    for offset in range(5):
        day = today + timedelta(days=offset)
        date_str = day.strftime("%Y-%m-%d")
        week.append(
            schemas.ScheduleDay(
                date=date_str,
                day_of_week=day.isoweekday(),
                blocks=[
                    schemas.ScheduleBlock(
                        start="09:00",
                        end="10:30",
                        title="待办事项",
                        location="待定",
                        type="other",
                        notes="示例日程，上传内容解析将在后续阶段完善。",
                    )
                ],
            )
        )
    return schemas.ScheduleResponse(
        meta=schemas.ScheduleMeta(
            source_filename=source_filename,
            generated_at=datetime.now().isoformat(),
            timezone="Asia/Shanghai",
        ),
        week=week,
        tips=["上传更多日程内容以生成更准确的计划。"],
    )


def schedule_from_ai(db: Session, source_filename: str, content: str) -> schemas.ScheduleResponse:
    route = get_route(db, "ai_route_schedule", "glm")
    if not provider_ready(db, route):
        return build_schedule_plan(source_filename)
    provider = build_provider(route, db)
    prompt = (
        "请根据以下日程内容生成固定格式JSON，不要包含多余文字。"
        "JSON格式：{\"meta\": {\"source_filename\": \"\", \"generated_at\": \"ISO8601\", \"timezone\": \"Asia/Shanghai\", \"version\": \"1.0\"},"
        "\"week\": [{\"date\": \"YYYY-MM-DD\", \"day_of_week\": 1, \"blocks\": [{\"start\": \"HH:MM\", \"end\": \"HH:MM\","
        "\"title\": \"\", \"location\": \"\", \"type\": \"study|work|life|health|other\", \"notes\": \"\"}]}],"
        "\"tips\": [\"\", \"\"]}"
        "确保 blocks 时间不重叠，按 start 升序。内容如下：\n"
        f"{content}"
    )
    try:
        raw = provider.generate(prompt)
        data = json.loads(raw)
        return schemas.ScheduleResponse(**data)
    except Exception:
        return build_schedule_plan(source_filename)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        username: str | None = payload.get("sub")
        if not username:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except JWTError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc
    user = crud.get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/api/auth/register", response_model=schemas.Token)
def register(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = crud.get_user_by_username(db, payload.username)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    user = crud.create_user(db, payload.username, payload.password)
    token = create_access_token(user.username)
    return {"access_token": token, "token_type": "bearer"}


@app.post("/api/auth/login", response_model=schemas.Token)
def login(payload: schemas.UserLogin, db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, payload.username, payload.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(user.username)
    return {"access_token": token, "token_type": "bearer"}


@app.post("/api/auth/wechat_login", response_model=schemas.Token)
def wechat_login(payload: schemas.WechatLogin, db: Session = Depends(get_db)):
    openid = fetch_wechat_openid(payload.code)
    user = crud.get_user_by_openid(db, openid)
    if not user:
        username = f"wx_{openid[:16]}"
        user = crud.create_wechat_user(db, username, openid)
    token = create_access_token(user.username)
    return {"access_token": token, "token_type": "bearer"}


@app.get("/api/weather", response_model=schemas.WeatherResponse)
def weather(location: str, db: Session = Depends(get_db)):
    return fetch_weather(db, location)


@app.get("/api/news", response_model=schemas.NewsResponse)
def news(
    page: int = 1,
    page_size: int = 10,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    page = max(page, 1)
    page_size = min(max(page_size, 1), 50)
    tags = [tag for tag in current_user.subscriptions.split(",") if tag]
    items, total = crud.list_news(db, tags, page, page_size)
    mapped = [
        schemas.NewsItem(
            id=item.id,
            title=item.title,
            summary=item.summary,
            source=item.source,
            url=item.url,
            published_at=item.published_at,
            tags=[tag for tag in item.tags.split(",") if tag],
        )
        for item in items
    ]
    return schemas.NewsResponse(
        items=mapped,
        page=page,
        page_size=page_size,
        has_more=page * page_size < total,
    )


@app.post("/api/schedule/upload", response_model=schemas.ScheduleResponse)
def upload_schedule(
    file: UploadFile,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not file.filename:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File required")
    if not file.filename.lower().endswith((".txt", ".md", ".csv")):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported file type")
    content = file.file.read()
    if len(content) > 2 * 1024 * 1024:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File too large")
    os.makedirs("uploads", exist_ok=True)
    stored_path = os.path.join("uploads", f"{current_user.id}_{file.filename}")
    with open(stored_path, "wb") as f:
        f.write(content)
    content_text = content.decode("utf-8", errors="ignore")
    plan = schedule_from_ai(db, file.filename, content_text)
    payload = plan.model_dump_json()
    crud.create_schedule_plan(
        db,
        user_id=current_user.id,
        source_filename=file.filename,
        payload=payload,
        created_at=datetime.now().isoformat(),
    )
    return plan


@app.get("/api/schedule/latest", response_model=schemas.ScheduleResponse)
def latest_schedule(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    plan = crud.get_latest_schedule(db, current_user.id)
    if not plan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No schedule found")
    return schemas.ScheduleResponse(**json.loads(plan.payload))


@app.get("/api/user/profile", response_model=schemas.UserProfile)
def profile(current_user=Depends(get_current_user)):
    subscriptions = [tag for tag in current_user.subscriptions.split(",") if tag]
    return schemas.UserProfile(
        id=current_user.id,
        username=current_user.username,
        location=current_user.location,
        subscriptions=subscriptions,
    )


@app.put("/api/user/location")
def update_location(
    payload: schemas.UpdateLocation,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    current_user.location = payload.location
    db.add(current_user)
    db.commit()
    return {"status": "ok"}


@app.put("/api/user/subscriptions")
def update_subscriptions(
    payload: schemas.UpdateSubscriptions,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    current_user.subscriptions = ",".join(payload.tags)
    db.add(current_user)
    db.commit()
    return {"status": "ok"}


@app.get("/admin/login")
def admin_login(request: Request):
    return templates.TemplateResponse("admin_login.html", {"request": request, "error": ""})


@app.post("/admin/login")
def admin_login_post(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    user = crud.authenticate_user(db, username, password)
    if not user or not user.is_admin:
        return templates.TemplateResponse(
            "admin_login.html",
            {"request": request, "error": "账号或密码错误"},
        )
    request.session["admin_user"] = user.username
    return RedirectResponse(url="/admin/settings", status_code=status.HTTP_302_FOUND)


def require_admin(request: Request):
    if not request.session.get("admin_user"):
        return RedirectResponse(url="/admin/login", status_code=status.HTTP_302_FOUND)
    return None


@app.get("/admin/logout")
def admin_logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/admin/login", status_code=status.HTTP_302_FOUND)


@app.get("/admin/settings")
def admin_settings(request: Request, db: Session = Depends(get_db)):
    redirect = require_admin(request)
    if redirect:
        return redirect
    def setting_value(key: str, default: str) -> str:
        item = crud.get_setting(db, key)
        return item.value if item else default

    settings_map = {
        "wechat_appid": setting_value("wechat_appid", ""),
        "wechat_secret": setting_value("wechat_secret", ""),
        "weather_geo_url": setting_value("weather_geo_url", settings.weather_geo_url),
        "weather_api_url": setting_value("weather_api_url", settings.weather_api_url),
        "news_crawler_enabled": setting_value("news_crawler_enabled", "false"),
        "news_feed_urls": setting_value("news_feed_urls", ""),
        "ai_deepseek_api_key": setting_value("ai_deepseek_api_key", ""),
        "ai_deepseek_base_url": setting_value("ai_deepseek_base_url", "https://api.deepseek.com"),
        "ai_deepseek_model": setting_value("ai_deepseek_model", "deepseek-chat"),
        "ai_glm_api_key": setting_value("ai_glm_api_key", ""),
        "ai_glm_base_url": setting_value("ai_glm_base_url", "https://open.bigmodel.cn/api/paas/v4"),
        "ai_glm_model": setting_value("ai_glm_model", "glm-4"),
        "ai_openai_api_key": setting_value("ai_openai_api_key", ""),
        "ai_openai_base_url": setting_value("ai_openai_base_url", "https://api.openai.com/v1"),
        "ai_openai_model": setting_value("ai_openai_model", "gpt-4o-mini"),
        "ai_route_news": setting_value("ai_route_news", "deepseek"),
        "ai_route_weather": setting_value("ai_route_weather", "openai"),
        "ai_route_schedule": setting_value("ai_route_schedule", "glm"),
    }
    return templates.TemplateResponse(
        "admin_settings.html",
        {"request": request, "settings": settings_map},
    )


@app.post("/admin/settings")
def admin_settings_post(
    request: Request,
    wechat_appid: str = Form(""),
    wechat_secret: str = Form(""),
    weather_geo_url: str = Form(""),
    weather_api_url: str = Form(""),
    news_crawler_enabled: str = Form("false"),
    news_feed_urls: str = Form(""),
    ai_deepseek_api_key: str = Form(""),
    ai_deepseek_base_url: str = Form(""),
    ai_deepseek_model: str = Form(""),
    ai_glm_api_key: str = Form(""),
    ai_glm_base_url: str = Form(""),
    ai_glm_model: str = Form(""),
    ai_openai_api_key: str = Form(""),
    ai_openai_base_url: str = Form(""),
    ai_openai_model: str = Form(""),
    ai_route_news: str = Form("deepseek"),
    ai_route_weather: str = Form("openai"),
    ai_route_schedule: str = Form("glm"),
    db: Session = Depends(get_db),
):
    redirect = require_admin(request)
    if redirect:
        return redirect
    crud.upsert_setting(db, "wechat_appid", wechat_appid)
    crud.upsert_setting(db, "wechat_secret", wechat_secret)
    crud.upsert_setting(db, "weather_geo_url", weather_geo_url)
    crud.upsert_setting(db, "weather_api_url", weather_api_url)
    crud.upsert_setting(db, "news_crawler_enabled", news_crawler_enabled)
    crud.upsert_setting(db, "news_feed_urls", news_feed_urls)
    crud.upsert_setting(db, "ai_deepseek_api_key", ai_deepseek_api_key)
    crud.upsert_setting(db, "ai_deepseek_base_url", ai_deepseek_base_url)
    crud.upsert_setting(db, "ai_deepseek_model", ai_deepseek_model)
    crud.upsert_setting(db, "ai_glm_api_key", ai_glm_api_key)
    crud.upsert_setting(db, "ai_glm_base_url", ai_glm_base_url)
    crud.upsert_setting(db, "ai_glm_model", ai_glm_model)
    crud.upsert_setting(db, "ai_openai_api_key", ai_openai_api_key)
    crud.upsert_setting(db, "ai_openai_base_url", ai_openai_base_url)
    crud.upsert_setting(db, "ai_openai_model", ai_openai_model)
    crud.upsert_setting(db, "ai_route_news", ai_route_news)
    crud.upsert_setting(db, "ai_route_weather", ai_route_weather)
    crud.upsert_setting(db, "ai_route_schedule", ai_route_schedule)
    return RedirectResponse(url="/admin/settings", status_code=status.HTTP_302_FOUND)


@app.get("/admin/users")
def admin_users(request: Request, db: Session = Depends(get_db)):
    redirect = require_admin(request)
    if redirect:
        return redirect
    users = crud.list_users(db)
    return templates.TemplateResponse(
        "admin_users.html",
        {"request": request, "users": users},
    )
