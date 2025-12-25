from __future__ import annotations

import datetime
import logging
from typing import Iterable

import feedparser
from sqlalchemy.orm import Session

from app import crud

logger = logging.getLogger(__name__)


def parse_feed(url: str) -> Iterable[dict]:
    parsed = feedparser.parse(url)
    if parsed.bozo:
        logger.warning("Feed parse error: %s", parsed.bozo_exception)
    for entry in parsed.entries:
        yield {
            "title": entry.get("title", "") or "未命名资讯",
            "url": entry.get("link", ""),
            "summary": entry.get("summary", "") or "",
            "source": parsed.feed.get("title", "订阅源"),
            "published_at": entry.get("published", "") or datetime.datetime.now().isoformat(),
        }


def crawl_feeds(db: Session, feed_urls: list[str], summarize, limit: int | None = None) -> int:
    created = 0
    for url in feed_urls:
        try:
            for item in parse_feed(url):
                if not item["url"]:
                    continue
                if crud.get_news_by_url(db, item["url"]):
                    continue
                summary_text = item["summary"]
                if not summary_text:
                    summary_text = summarize(item["title"], "")
                crud.create_news_item(
                    db,
                    title=item["title"],
                    summary=summary_text[:200],
                    source=item["source"],
                    url=item["url"],
                    published_at=item["published_at"],
                    tags=["订阅"],
                )
                created += 1
                if limit is not None and created >= limit:
                    return created
        except Exception as exc:
            logger.exception("Feed crawl failed: %s", exc)
    return created
