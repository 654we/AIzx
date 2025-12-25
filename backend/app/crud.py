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


def get_news_by_url(db: Session, url: str) -> models.NewsItem | None:
    return db.query(models.NewsItem).filter(models.NewsItem.url == url).first()


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


def create_schedule_plan(
    db: Session,
    user_id: int,
    source_filename: str,
    payload: str,
    created_at: str,
) -> models.SchedulePlan:
    plan = models.SchedulePlan(
        user_id=user_id,
        source_filename=source_filename,
        payload=payload,
        created_at=created_at,
    )
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return plan


def get_latest_schedule(db: Session, user_id: int) -> models.SchedulePlan | None:
    return (
        db.query(models.SchedulePlan)
        .filter(models.SchedulePlan.user_id == user_id)
        .order_by(models.SchedulePlan.created_at.desc())
        .first()
    )


def get_setting(db: Session, key: str) -> models.Setting | None:
    return db.query(models.Setting).filter(models.Setting.key == key).first()


def upsert_setting(db: Session, key: str, value: str) -> models.Setting:
    setting = get_setting(db, key)
    if setting:
        setting.value = value
    else:
        setting = models.Setting(key=key, value=value)
        db.add(setting)
    db.commit()
    db.refresh(setting)
    return setting


def list_users(db: Session) -> list[models.User]:
    return db.query(models.User).order_by(models.User.id.asc()).all()


def authenticate_user(db: Session, username: str, password: str) -> models.User | None:
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user
