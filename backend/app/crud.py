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


def create_news_item(
    db: Session,
    title: str,
    summary: str,
    source: str,
    url: str,
    published_at: str,
    tags: list[str],
) -> models.NewsItem:
    item = models.NewsItem(
        title=title,
        summary=summary,
        source=source,
        url=url,
        published_at=published_at,
        tags=",".join(tags),
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def list_news(db: Session, tags: list[str], page: int, page_size: int) -> tuple[list[models.NewsItem], int]:
    query = db.query(models.NewsItem)
    if tags:
        filters = [models.NewsItem.tags.like(f"%{tag}%") for tag in tags]
        for clause in filters:
            query = query.filter(clause)
    total = query.count()
    items = (
        query.order_by(models.NewsItem.published_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    return items, total


def authenticate_user(db: Session, username: str, password: str) -> models.User | None:
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user
