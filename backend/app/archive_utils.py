from datetime import datetime, timedelta
from email.utils import parsedate_to_datetime
import logging
from threading import Lock
from zoneinfo import ZoneInfo

archive_lock = Lock()
archive_tz = ZoneInfo("Asia/Shanghai")
logger = logging.getLogger(__name__)


def get_last_week_range(reference: datetime | None = None) -> tuple[datetime.date, datetime.date, str]:
    base = reference or datetime.now(tz=archive_tz)
    today = base.date()
    last_week = today - timedelta(days=7)
    start = last_week - timedelta(days=last_week.weekday())
    end = start + timedelta(days=6)
    week_key = f"{start.isocalendar().year}-W{start.isocalendar().week:02d}"
    return start, end, week_key


def parse_published_date(published_at: str):
    if not published_at:
        return None
    try:
        cleaned = published_at.replace("Z", "+00:00")
        return datetime.fromisoformat(cleaned).date()
    except ValueError:
        pass
    try:
        parsed = parsedate_to_datetime(published_at)
        if parsed:
            return parsed.date()
    except (TypeError, ValueError):
        pass
    logger.warning("Archive date parse failed: %s", published_at)
    return None
