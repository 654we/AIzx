from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "AIx2 Backend"
    jwt_secret: str = "change_me"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60 * 24
    database_url: str = "sqlite:///./aix2.db"
    wechat_appid: str = ""
    wechat_secret: str = ""
    wechat_base_url: str = "https://api.weixin.qq.com/sns/jscode2session"

    class Config:
        env_file = ".env"


settings = Settings()
