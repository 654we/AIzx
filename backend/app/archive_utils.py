from datetime import datetime, timedelta
from threading import Lock
from zoneinfo import ZoneInfo

archive_lock = Lock()
archive_tz = ZoneInfo("Asia/Shanghai")


def get_last_week_range(reference: datetime | None = None) -> tuple[datetime.date, datetime.date, str]:
    base = reference or datetime.now(tz=archive_tz)
    today = base.date()
    last_week = today - timedelta(days=7)
    start = last_week - timedelta(days=last_week.weekday())
    end = start + timedelta(days=6)
    week_key = f"{start.isocalendar().year}-W{start.isocalendar().week:02d}"
    return start, end, week_key
