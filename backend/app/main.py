import httpx
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app import crud, schemas
from app.auth import create_access_token
from app.config import settings
from app.database import init_db
from app.deps import get_db

app = FastAPI(title=settings.app_name)
security = HTTPBearer()


@app.on_event("startup")
def startup_event() -> None:
    init_db()
    db = next(get_db())
    try:
        admin = crud.get_user_by_username(db, "admin")
        if not admin:
            crud.create_user(db, "admin", "admin", is_admin=True)
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


def fetch_weather(location: str) -> schemas.WeatherResponse:
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
        travel_advice=travel_advice_for(condition, temp_c, aqi),
    )


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
def weather(location: str):
    return fetch_weather(location)


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


@app.post("/admin/login")
def admin_login(request: Request):
    return {"message": "admin login placeholder", "path": str(request.url)}
