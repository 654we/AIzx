import secrets

from sqlalchemy.orm import Session

from app import models
from app.auth import hash_password, verify_password


def get_user_by_username(db: Session, username: str) -> models.User | None:
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_openid(db: Session, openid: str) -> models.User | None:
    return db.query(models.User).filter(models.User.wechat_openid == openid).first()


def create_user(db: Session, username: str, password: str, is_admin: bool = False) -> models.User:
    user = models.User(
        username=username,
        password_hash=hash_password(password),
        is_admin=is_admin,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_wechat_user(db: Session, username: str, openid: str) -> models.User:
    random_password = secrets.token_urlsafe(16)
    user = models.User(
        username=username,
        password_hash=hash_password(random_password),
        wechat_openid=openid,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, username: str, password: str) -> models.User | None:
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user
