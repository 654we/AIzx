from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.archive_utils import archive_lock, get_last_week_range


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
