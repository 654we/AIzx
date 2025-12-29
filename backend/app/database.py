from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import settings


connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
engine = create_engine(settings.database_url, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
ArchiveBase = declarative_base()
archive_engine = create_engine(settings.archive_database_url) if settings.archive_database_url else None
ArchiveSessionLocal = (
    sessionmaker(autocommit=False, autoflush=False, bind=archive_engine)
    if archive_engine
    else None
)


def init_db() -> None:
    from app import models  # noqa: F401

    Base.metadata.create_all(bind=engine)


def init_archive_db() -> None:
    if not archive_engine:
        return
    from app import models  # noqa: F401

    ArchiveBase.metadata.create_all(bind=archive_engine)
