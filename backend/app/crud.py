import secrets
from datetime import datetime

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
    content_hash: str = "",
    dedupe_group_id: str = "",
    dedupe_keep_reason: str = "",
    dedupe_merged_urls: str = "[]",
) -> models.NewsItem:
    item = models.NewsItem(
        title=title,
        summary=summary,
        source=source,
        url=url,
        published_at=published_at,
        tags=",".join(tags),
        content_hash=content_hash,
        dedupe_group_id=dedupe_group_id,
        dedupe_keep_reason=dedupe_keep_reason,
        dedupe_merged_urls=dedupe_merged_urls,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def get_news_by_url(db: Session, url: str) -> models.NewsItem | None:
    return db.query(models.NewsItem).filter(models.NewsItem.url == url).first()


def get_news_preview_by_news_id(db: Session, news_id: int) -> models.NewsPreview | None:
    return db.query(models.NewsPreview).filter(models.NewsPreview.news_id == news_id).first()


def get_news_preview_by_url(db: Session, url: str) -> models.NewsPreview | None:
    return db.query(models.NewsPreview).filter(models.NewsPreview.source_url == url).first()


def upsert_news_preview(
    db: Session,
    news_id: int | None,
    source_url: str,
    title: str,
    summary: str,
    key_points: str,
    fetched_at: str,
    cache_ttl_sec: int,
) -> models.NewsPreview:
    preview = None
    if news_id:
        preview = get_news_preview_by_news_id(db, news_id)
    if not preview:
        preview = get_news_preview_by_url(db, source_url)
    if preview:
        preview.news_id = news_id
        preview.source_url = source_url
        preview.title = title
        preview.summary = summary
        preview.key_points = key_points
        preview.fetched_at = fetched_at
        preview.cache_ttl_sec = cache_ttl_sec
    else:
        preview = models.NewsPreview(
            news_id=news_id,
            source_url=source_url,
            title=title,
            summary=summary,
            key_points=key_points,
            fetched_at=fetched_at,
            cache_ttl_sec=cache_ttl_sec,
        )
        db.add(preview)
    db.commit()
    db.refresh(preview)
    return preview


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


def create_schedule_upload(
    db: Session,
    user_id: int,
    filename: str,
    file_type: str,
    file_size: int,
    stored_path: str,
    status: str,
    parsed_text: str,
    created_at: str,
) -> models.ScheduleUpload:
    upload = models.ScheduleUpload(
        user_id=user_id,
        filename=filename,
        file_type=file_type,
        file_size=file_size,
        stored_path=stored_path,
        status=status,
        parsed_text=parsed_text,
        created_at=created_at,
    )
    db.add(upload)
    db.commit()
    db.refresh(upload)
    return upload


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


def list_users_filtered(db: Session, query: str | None = None) -> list[models.User]:
    base = db.query(models.User)
    if query:
        base = base.filter(models.User.username.contains(query))
    return base.order_by(models.User.id.asc()).all()


def get_user_by_id(db: Session, user_id: int) -> models.User | None:
    return db.query(models.User).filter(models.User.id == user_id).first()


def set_user_active(db: Session, user: models.User, is_active: bool) -> models.User:
    user.is_active = is_active
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user_profile(
    db: Session,
    user: models.User,
    username: str,
    location: str,
    subscriptions: list[str],
    email: str = "",
    phone: str = "",
    avatar_url: str = "",
) -> models.User:
    user.username = username
    user.location = location
    user.email = email
    user.phone = phone
    user.avatar_url = avatar_url
    user.subscriptions = ",".join(subscriptions)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def reset_user_password(db: Session, user: models.User, new_password: str) -> models.User:
    user.password_hash = hash_password(new_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_task_run(
    db: Session,
    task_type: str,
    status: str,
    duration_ms: int,
    error_message: str,
    log_excerpt: str,
    payload_json: str,
) -> models.TaskRun:
    run = models.TaskRun(
        task_type=task_type,
        status=status,
        duration_ms=duration_ms,
        error_message=error_message,
        log_excerpt=log_excerpt,
        payload_json=payload_json,
        created_at=datetime.now().isoformat(),
    )
    db.add(run)
    db.commit()
    db.refresh(run)
    return run


def list_task_runs(db: Session, limit: int = 20) -> list[models.TaskRun]:
    return (
        db.query(models.TaskRun)
        .order_by(models.TaskRun.created_at.desc())
        .limit(limit)
        .all()
    )


def create_weather_provider(
    db: Session,
    name: str,
    provider_type: str,
    base_url: str,
    api_key: str,
    timeout_sec: int,
    enabled: bool,
    priority: int,
    extra_config: str,
) -> models.WeatherProvider:
    provider = models.WeatherProvider(
        name=name,
        provider_type=provider_type,
        base_url=base_url,
        api_key=api_key,
        timeout_sec=timeout_sec,
        enabled=enabled,
        priority=priority,
        extra_config=extra_config,
    )
    db.add(provider)
    db.commit()
    db.refresh(provider)
    return provider


def list_weather_providers(db: Session) -> list[models.WeatherProvider]:
    return db.query(models.WeatherProvider).order_by(models.WeatherProvider.priority.asc()).all()


def get_weather_provider(db: Session, provider_id: int) -> models.WeatherProvider | None:
    return db.query(models.WeatherProvider).filter(models.WeatherProvider.id == provider_id).first()


def update_weather_provider(
    db: Session,
    provider: models.WeatherProvider,
    name: str,
    provider_type: str,
    base_url: str,
    api_key: str,
    timeout_sec: int,
    enabled: bool,
    priority: int,
    extra_config: str,
) -> models.WeatherProvider:
    provider.name = name
    provider.provider_type = provider_type
    provider.base_url = base_url
    provider.api_key = api_key
    provider.timeout_sec = timeout_sec
    provider.enabled = enabled
    provider.priority = priority
    provider.extra_config = extra_config
    db.add(provider)
    db.commit()
    db.refresh(provider)
    return provider


def delete_weather_provider(db: Session, provider: models.WeatherProvider) -> None:
    db.delete(provider)
    db.commit()


def create_mcp_remote(
    db: Session,
    name: str,
    base_url: str,
    protocol: str,
    auth_type: str,
    auth_value: str,
    extra_config: str,
    timeout_sec: int,
    enabled: bool,
    priority: int,
) -> models.MCPRemoteConfig:
    remote = models.MCPRemoteConfig(
        name=name,
        base_url=base_url,
        protocol=protocol,
        auth_type=auth_type,
        auth_value=auth_value,
        extra_config=extra_config,
        timeout_sec=timeout_sec,
        enabled=enabled,
        priority=priority,
    )
    db.add(remote)
    db.commit()
    db.refresh(remote)
    return remote


def list_mcp_remotes(db: Session) -> list[models.MCPRemoteConfig]:
    return db.query(models.MCPRemoteConfig).order_by(models.MCPRemoteConfig.priority.asc()).all()


def get_mcp_remote(db: Session, remote_id: int) -> models.MCPRemoteConfig | None:
    return db.query(models.MCPRemoteConfig).filter(models.MCPRemoteConfig.id == remote_id).first()


def update_mcp_remote(
    db: Session,
    remote: models.MCPRemoteConfig,
    name: str,
    base_url: str,
    protocol: str,
    auth_type: str,
    auth_value: str,
    extra_config: str,
    timeout_sec: int,
    enabled: bool,
    priority: int,
) -> models.MCPRemoteConfig:
    remote.name = name
    remote.base_url = base_url
    remote.protocol = protocol
    remote.auth_type = auth_type
    remote.auth_value = auth_value
    remote.extra_config = extra_config
    remote.timeout_sec = timeout_sec
    remote.enabled = enabled
    remote.priority = priority
    db.add(remote)
    db.commit()
    db.refresh(remote)
    return remote


def delete_mcp_remote(db: Session, remote: models.MCPRemoteConfig) -> None:
    db.delete(remote)
    db.commit()


def create_mcp_local(
    db: Session,
    name: str,
    module_path: str,
    command: str,
    args_json: str,
    env_json: str,
    capabilities: str,
    schema: str,
    timeout_sec: int,
    enabled: bool,
    priority: int,
) -> models.MCPLocalPlugin:
    local = models.MCPLocalPlugin(
        name=name,
        module_path=module_path,
        command=command,
        args_json=args_json,
        env_json=env_json,
        capabilities=capabilities,
        schema=schema,
        timeout_sec=timeout_sec,
        enabled=enabled,
        priority=priority,
    )
    db.add(local)
    db.commit()
    db.refresh(local)
    return local


def list_mcp_locals(db: Session) -> list[models.MCPLocalPlugin]:
    return db.query(models.MCPLocalPlugin).order_by(models.MCPLocalPlugin.priority.asc()).all()


def get_mcp_local(db: Session, local_id: int) -> models.MCPLocalPlugin | None:
    return db.query(models.MCPLocalPlugin).filter(models.MCPLocalPlugin.id == local_id).first()


def update_mcp_local(
    db: Session,
    local: models.MCPLocalPlugin,
    name: str,
    module_path: str,
    command: str,
    args_json: str,
    env_json: str,
    capabilities: str,
    schema: str,
    timeout_sec: int,
    enabled: bool,
    priority: int,
) -> models.MCPLocalPlugin:
    local.name = name
    local.module_path = module_path
    local.command = command
    local.args_json = args_json
    local.env_json = env_json
    local.capabilities = capabilities
    local.schema = schema
    local.timeout_sec = timeout_sec
    local.enabled = enabled
    local.priority = priority
    db.add(local)
    db.commit()
    db.refresh(local)
    return local


def delete_mcp_local(db: Session, local: models.MCPLocalPlugin) -> None:
    db.delete(local)
    db.commit()

def authenticate_user(db: Session, username: str, password: str) -> models.User | None:
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user
