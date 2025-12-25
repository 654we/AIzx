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
