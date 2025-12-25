from sqlalchemy import Boolean, Column, Integer, String

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)
    location = Column(String(128), default="")
    subscriptions = Column(String(512), default="")
    wechat_openid = Column(String(128), unique=True, nullable=True, index=True)


class NewsItem(Base):
    __tablename__ = "news_items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(256), nullable=False)
    summary = Column(String(512), nullable=False)
    source = Column(String(128), nullable=False)
    url = Column(String(512), unique=True, nullable=False)
    published_at = Column(String(64), nullable=False)
    tags = Column(String(256), default="")
