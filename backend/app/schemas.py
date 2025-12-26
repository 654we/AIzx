from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=64)


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=128)


class UserLogin(UserBase):
    password: str = Field(..., min_length=6, max_length=128)


class WechatLogin(BaseModel):
    code: str = Field(..., min_length=1, max_length=128)


class UserProfile(BaseModel):
    id: int
    username: str
    location: str = ""
    email: str = ""
    phone: str = ""
    avatar_url: str = ""
    subscriptions: list[str] = []


class UpdateLocation(BaseModel):
    location: str = Field(..., min_length=1, max_length=128)


class UpdateSubscriptions(BaseModel):
    tags: list[str] = []


class UpdateUserProfile(BaseModel):
    username: str = Field(..., min_length=3, max_length=64)
    location: str = ""
    email: str = ""
    phone: str = ""
    avatar_url: str = ""


class UpdateUserPassword(BaseModel):
    old_password: str = Field(..., min_length=6, max_length=128)
    new_password: str = Field(..., min_length=6, max_length=128)


class WeatherLocation(BaseModel):
    name: str
    lat: float
    lon: float


class WeatherInfo(BaseModel):
    condition: str
    temp_c: float
    humidity: int
    wind: str
    aqi: int
    aqi_desc: str
    updated_at: str


class WeatherResponse(BaseModel):
    location: WeatherLocation
    weather: WeatherInfo
    travel_advice: list[str]


class NewsItem(BaseModel):
    id: int
    title: str
    summary: str
    source: str
    url: str
    published_at: str
    tags: list[str]


class NewsResponse(BaseModel):
    items: list[NewsItem]
    page: int
    page_size: int
    has_more: bool


class NewsPreviewResponse(BaseModel):
    title: str
    summary: str
    key_points: list[str]
    source_url: str
    fetched_at: str


class ScheduleMeta(BaseModel):
    source_filename: str
    generated_at: str
    timezone: str
    version: str = "1.0"


class ScheduleBlock(BaseModel):
    start: str
    end: str
    title: str
    location: str
    type: str
    notes: str


class ScheduleDay(BaseModel):
    date: str
    day_of_week: int
    blocks: list[ScheduleBlock]


class ScheduleResponse(BaseModel):
    meta: ScheduleMeta
    week: list[ScheduleDay]
    tips: list[str]


class TaskRunResponse(BaseModel):
    id: int
    task_type: str
    status: str
    duration_ms: int
    error_message: str = ""
    log_excerpt: str = ""
    payload_json: str = ""
    created_at: str


class SchedulerConfig(BaseModel):
    news_crawler_enabled: bool
    cron: str = ""
    interval_minutes: int = 30
    limit: int = 20
    sources: dict[str, bool]


class MCPRemoteConfigPayload(BaseModel):
    name: str
    base_url: str
    auth_type: str = "none"
    auth_value: str = ""
    timeout_sec: int = 10
    enabled: bool = True
    priority: int = 1


class MCPLocalPluginPayload(BaseModel):
    name: str
    module_path: str
    capabilities: list[str]
    schema: dict
    timeout_sec: int = 10
    enabled: bool = True
    priority: int = 1


class WeatherProviderPayload(BaseModel):
    name: str
    provider_type: str
    base_url: str
    api_key: str = ""
    timeout_sec: int = 5
    enabled: bool = True
    priority: int = 1
    extra_config: dict = {}


class UserAdminPayload(BaseModel):
    username: str
    location: str = ""
    subscriptions: list[str] = []
    is_active: bool = True
