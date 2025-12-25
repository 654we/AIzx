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
    subscriptions: list[str] = []


class UpdateLocation(BaseModel):
    location: str = Field(..., min_length=1, max_length=128)


class UpdateSubscriptions(BaseModel):
    tags: list[str] = []


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
