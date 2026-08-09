from __future__ import annotations

import os
from dataclasses import dataclass
from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    openai_api_key: str
    openai_chat_model: str = "gpt-4o-mini"
    openai_temperature: float = 0.0
    serpapi_api_key: str = ""
    tavily_api_key: str = ""


def get_settings() -> Settings:
    """Load app settings from environment variables."""

    return Settings(
        openai_api_key=os.getenv("OPENAI_API_KEY", "").strip(),
        openai_chat_model=os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini").strip(),
        openai_temperature=float(os.getenv("OPENAI_TEMPERATURE", "0")),
        serpapi_api_key=os.getenv("SERPAPI_API_KEY", "").strip(),
        tavily_api_key=os.getenv("TAVILY_API_KEY", "").strip(),
    )
