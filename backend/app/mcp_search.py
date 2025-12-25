from __future__ import annotations

import logging
from typing import Callable

from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


def search_news_via_mcp(db: Session, summarize: Callable[[str, str], str]) -> None:
    """Placeholder for MCP search integration.

    This function should be replaced with actual MCP tool calls when available.
    """
    logger.info("MCP search is not configured; skipping news search")
