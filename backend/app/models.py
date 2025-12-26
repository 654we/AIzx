from sqlalchemy import Boolean, Column, Integer, String, UniqueConstraint
from sqlalchemy import Text

from app.database import Base, ArchiveBase


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    location = Column(String(128), default="")
    email = Column(String(128), default="")
    phone = Column(String(32), default="")
    avatar_url = Column(String(512), default="")
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
    content_hash = Column(String(64), default="", index=True)
    dedupe_group_id = Column(String(64), default="")
    dedupe_keep_reason = Column(Text, default="")
    dedupe_merged_urls = Column(Text, default="[]")


class NewsPreview(Base):
    __tablename__ = "news_previews"

    id = Column(Integer, primary_key=True, index=True)
    news_id = Column(Integer, nullable=True, index=True)
    source_url = Column(String(512), nullable=False, index=True)
    title = Column(String(256), nullable=False)
    summary = Column(String(512), nullable=False)
    key_points = Column(Text, default="[]")
    fetched_at = Column(String(64), nullable=False)
    cache_ttl_sec = Column(Integer, default=3600)


class SchedulePlan(Base):
    __tablename__ = "schedule_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    source_filename = Column(String(256), nullable=False)
    payload = Column(Text, nullable=False)
    created_at = Column(String(64), nullable=False)


class ScheduleUpload(Base):
    __tablename__ = "schedule_uploads"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    filename = Column(String(256), nullable=False)
    file_type = Column(String(32), nullable=False)
    file_size = Column(Integer, default=0)
    stored_path = Column(String(512), nullable=False)
    status = Column(String(32), default="uploaded")
    parsed_text = Column(Text, default="")
    created_at = Column(String(64), nullable=False)


class Setting(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(128), unique=True, nullable=False)
    value = Column(Text, nullable=False)


class TaskRun(Base):
    __tablename__ = "task_runs"

    id = Column(Integer, primary_key=True, index=True)
    task_type = Column(String(64), nullable=False)
    status = Column(String(32), nullable=False)
    duration_ms = Column(Integer, default=0)
    error_message = Column(String(512), default="")
    log_excerpt = Column(Text, default="")
    payload_json = Column(Text, default="")
    created_at = Column(String(64), nullable=False)


class WeatherProvider(Base):
    __tablename__ = "weather_providers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False)
    provider_type = Column(String(64), nullable=False)
    base_url = Column(String(256), nullable=False)
    api_key = Column(String(256), default="")
    timeout_sec = Column(Integer, default=5)
    enabled = Column(Boolean, default=True)
    priority = Column(Integer, default=1)
    extra_config = Column(Text, default="{}")


class MCPRemoteConfig(Base):
    __tablename__ = "mcp_remote_configs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False)
    base_url = Column(String(256), nullable=False)
    protocol = Column(String(32), default="http")
    auth_type = Column(String(32), default="none")
    auth_value = Column(String(256), default="")
    extra_config = Column(Text, default="{}")
    timeout_sec = Column(Integer, default=10)
    enabled = Column(Boolean, default=True)
    priority = Column(Integer, default=1)


class MCPLocalPlugin(Base):
    __tablename__ = "mcp_local_plugins"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False)
    module_path = Column(String(256), nullable=False)
    command = Column(String(128), default="")
    args_json = Column(Text, default="[]")
    env_json = Column(Text, default="{}")
    capabilities = Column(Text, default="[]")
    schema = Column(Text, default="{}")
    timeout_sec = Column(Integer, default=10)
    enabled = Column(Boolean, default=True)
    priority = Column(Integer, default=1)


class ArchiveNewsItem(ArchiveBase):
    __tablename__ = "archive_news_items"
    __table_args__ = (UniqueConstraint("url", "archive_week", name="uniq_url_week"),)

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(256), nullable=False)
    summary = Column(String(512), nullable=False)
    source = Column(String(128), nullable=False)
    url = Column(String(512), nullable=False, index=True)
    published_at = Column(String(64), nullable=False)
    tags = Column(String(256), default="")
    content_hash = Column(String(64), default="")
    archive_week = Column(String(16), nullable=False, index=True)
