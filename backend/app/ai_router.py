from __future__ import annotations

from sqlalchemy.orm import Session

from app.ai import DeepSeekProvider, GLMProvider, OpenAICompatProvider, ProviderConfig
from app.crud import get_setting


def setting_value(db: Session, key: str, default: str) -> str:
    item = get_setting(db, key)
    return item.value if item else default


def build_provider(name: str, db: Session):
    if name == "deepseek":
        return DeepSeekProvider(
            ProviderConfig(
                api_key=setting_value(db, "ai_deepseek_api_key", ""),
                base_url=setting_value(db, "ai_deepseek_base_url", "https://api.deepseek.com"),
                model=setting_value(db, "ai_deepseek_model", "deepseek-chat"),
            )
        )
    if name == "glm":
        return GLMProvider(
            ProviderConfig(
                api_key=setting_value(db, "ai_glm_api_key", ""),
                base_url=setting_value(db, "ai_glm_base_url", "https://open.bigmodel.cn/api/paas/v4"),
                model=setting_value(db, "ai_glm_model", "glm-4"),
            )
        )
    return OpenAICompatProvider(
        ProviderConfig(
            api_key=setting_value(db, "ai_openai_api_key", ""),
            base_url=setting_value(db, "ai_openai_base_url", "https://api.openai.com/v1"),
            model=setting_value(db, "ai_openai_model", "gpt-4o-mini"),
        )
    )


def get_route(db: Session, key: str, default: str) -> str:
    return setting_value(db, key, default)
