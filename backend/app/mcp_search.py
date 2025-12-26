from __future__ import annotations

import datetime
import logging
from typing import Callable

import httpx
from pydantic import BaseModel, ValidationError
from sqlalchemy.orm import Session

from app import crud

logger = logging.getLogger(__name__)


def _setting_value(db: Session, key: str, default: str) -> str:
    item = crud.get_setting(db, key)
    return item.value if item else default


class MCPItem(BaseModel):
    title: str
    url: str
    summary: str | None = None
    source: str | None = None
    published_at: str | None = None


class MCPResponse(BaseModel):
    items: list[MCPItem]


def parse_streamable_response(lines: list[str]) -> MCPResponse | None:
    for raw in reversed(lines):
        if not raw:
            continue
        if raw.startswith("data:"):
            raw = raw.replace("data:", "", 1).strip()
        if not raw:
            continue
        try:
            payload = MCPResponse.model_validate_json(raw)
            return payload
        except ValidationError:
            continue
    return None


def search_news_via_mcp(db: Session, summarize: Callable[[str, str], str]) -> None:
    """Call MCP search endpoint and persist results.

    Expected MCP response JSON format:
    {"items": [{"title": "", "url": "", "summary": "", "source": "", "published_at": ""}]}
    """
    remotes = [remote for remote in crud.list_mcp_remotes(db) if remote.enabled and remote.base_url]
    keywords = _setting_value(db, "mcp_keywords", "资讯,科技")
    if remotes:
        remote = remotes[0]
        headers = {}
        if remote.auth_type in {"api_key", "token"} and remote.auth_value:
            headers["Authorization"] = f"Bearer {remote.auth_value}"
        base_url = remote.base_url
        timeout = remote.timeout_sec
        protocol = remote.protocol or "http"
    else:
        enabled = _setting_value(db, "mcp_enabled", "false").lower() == "true"
        base_url = _setting_value(db, "mcp_base_url", "")
        api_key = _setting_value(db, "mcp_api_key", "")
        timeout = 10.0
        protocol = "http"
        if not enabled or not base_url:
            logger.info("MCP search disabled or base_url missing")
            return
        headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
    payload = {"query": keywords, "limit": 10}
    try:
        data = fetch_mcp_items(base_url, headers, payload, timeout, protocol)
    except httpx.HTTPError as exc:
        logger.exception("MCP search request failed: %s", exc)
        return
    for item in data.items:
        url = item.url
        if not url or crud.get_news_by_url(db, url):
            continue
        title = item.title or "未命名资讯"
        summary = item.summary or summarize(title, "")
        source = item.source or "MCP"
        published_at = item.published_at or datetime.datetime.now().isoformat()
        crud.create_news_item(
            db,
            title=title,
            summary=summary[:200],
            source=source,
            url=url,
            published_at=published_at,
            tags=["MCP"],
        )


def fetch_mcp_candidates(db: Session, limit: int) -> list[dict]:
    remotes = [remote for remote in crud.list_mcp_remotes(db) if remote.enabled and remote.base_url]
    keywords = _setting_value(db, "mcp_keywords", "资讯,科技")
    if remotes:
        remote = remotes[0]
        headers = {}
        if remote.auth_type in {"api_key", "token"} and remote.auth_value:
            headers["Authorization"] = f"Bearer {remote.auth_value}"
        base_url = remote.base_url
        timeout = remote.timeout_sec
        protocol = remote.protocol or "http"
    else:
        enabled = _setting_value(db, "mcp_enabled", "false").lower() == "true"
        base_url = _setting_value(db, "mcp_base_url", "")
        api_key = _setting_value(db, "mcp_api_key", "")
        timeout = 10.0
        protocol = "http"
        if not enabled or not base_url:
            logger.info("MCP search disabled or base_url missing")
            return []
        headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
    payload = {"query": keywords, "limit": limit}
    try:
        data = fetch_mcp_items(base_url, headers, payload, timeout, protocol)
    except httpx.HTTPError as exc:
        logger.exception("MCP search request failed: %s", exc)
        return []
    candidates = []
    for item in data.items:
        if not item.url:
            continue
        candidates.append(
            {
                "title": item.title or "未命名资讯",
                "url": item.url,
                "summary": item.summary or "",
                "source": item.source or "MCP",
                "published_at": item.published_at or datetime.datetime.now().isoformat(),
                "tags": ["MCP"],
            }
        )
    return candidates


def fetch_mcp_items(
    base_url: str,
    headers: dict,
    payload: dict,
    timeout: float,
    protocol: str,
) -> MCPResponse:
    if protocol == "streamable_http":
        lines = []
        with httpx.stream("POST", base_url, json=payload, headers=headers, timeout=timeout) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    lines.append(line.decode("utf-8", errors="ignore") if isinstance(line, bytes) else line)
        data = parse_streamable_response(lines)
        if not data:
            raise httpx.HTTPError("Streamable MCP response invalid")
        return data
    response = httpx.post(base_url, json=payload, headers=headers, timeout=timeout)
    response.raise_for_status()
    return MCPResponse.model_validate(response.json())
