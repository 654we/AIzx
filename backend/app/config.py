from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "AIx2 Backend"
    jwt_secret: str = "change_me"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60 * 24
    database_url: str = "sqlite:///./aix2.db"

    class Config:
        env_file = ".env"


settings = Settings()
