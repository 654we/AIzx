from __future__ import annotations

import datetime
import logging
from typing import Callable

import httpx
from sqlalchemy.orm import Session

from app import crud

logger = logging.getLogger(__name__)


def _setting_value(db: Session, key: str, default: str) -> str:
    item = crud.get_setting(db, key)
    return item.value if item else default


def search_news_via_mcp(db: Session, summarize: Callable[[str, str], str]) -> None:
    """Call MCP search endpoint and persist results.

    Expected MCP response JSON format:
    {"items": [{"title": "", "url": "", "summary": "", "source": "", "published_at": ""}]}
    """
    enabled = _setting_value(db, "mcp_enabled", "false").lower() == "true"
    base_url = _setting_value(db, "mcp_base_url", "")
    api_key = _setting_value(db, "mcp_api_key", "")
    keywords = _setting_value(db, "mcp_keywords", "资讯,科技")
    if not enabled or not base_url:
        logger.info("MCP search disabled or base_url missing")
        return
    headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
    payload = {"query": keywords, "limit": 10}
    try:
        response = httpx.post(base_url, json=payload, headers=headers, timeout=10.0)
        response.raise_for_status()
    except httpx.HTTPError as exc:
        logger.exception("MCP search request failed: %s", exc)
        return
    data = response.json()
    items = data.get("items", [])
    for item in items:
        url = item.get("url")
        if not url or crud.get_news_by_url(db, url):
            continue
        title = item.get("title") or "未命名资讯"
        summary = item.get("summary") or summarize(title, "")
        source = item.get("source") or "MCP"
        published_at = item.get("published_at") or datetime.datetime.now().isoformat()
        crud.create_news_item(
            db,
            title=title,
            summary=summary[:200],
            source=source,
            url=url,
            published_at=published_at,
            tags=["MCP"],
        )
