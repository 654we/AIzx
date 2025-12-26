from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.archive_utils import archive_lock, get_last_week_range, parse_published_date


def test_get_last_week_range_monday_start():
    ref = datetime(2024, 3, 6, 9, 0, tzinfo=ZoneInfo("Asia/Shanghai"))
    start, end, week_key = get_last_week_range(ref)
    assert start.weekday() == 0
    assert end.weekday() == 6
    assert week_key.startswith("2024-W")


def test_archive_lock_prevents_overlap():
    acquired = archive_lock.acquire(blocking=False)
    try:
        assert acquired is True
        assert archive_lock.acquire(blocking=False) is False
    finally:
        if acquired:
            archive_lock.release()


def test_parse_published_date_iso():
    parsed = parse_published_date("2024-03-01T12:00:00+08:00")
    assert parsed is not None
    assert parsed.isoformat() == "2024-03-01"


def test_parse_published_date_rfc2822():
    parsed = parse_published_date("Mon, 02 Jan 2006 15:04:05 GMT")
    assert parsed is not None
    assert parsed.isoformat() == "2006-01-02"
