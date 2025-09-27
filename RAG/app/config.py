from __future__ import annotations

import os
from dataclasses import dataclass
from typing import List

from dotenv import load_dotenv


load_dotenv()


@dataclass
class Settings:
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_base_url: str | None = os.getenv("OPENAI_BASE_URL")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    chat_model: str = os.getenv("CHAT_MODEL", "gpt-4o-mini")
    index_dir: str = os.getenv("INDEX_DIR", "index")
    web_search_enabled: bool = os.getenv("WEB_SEARCH_ENABLED", "true").lower() in {"1","true","yes"}
    max_web_results: int = int(os.getenv("MAX_WEB_RESULTS", "4"))

    # Chunking
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "1500"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "200"))

    # File discovery
    include_exts: List[str] = tuple(
        os.getenv(
            "DOC_EXTS",
            ".txt,.md,.pdf,.py,.json,.yaml,.yml,.rst,.csv,.ts,.tsx,.js,.jsx",
        ).split(",")
    )  # type: ignore[assignment]
    exclude_dirs: List[str] = tuple(
        os.getenv(
            "EXCLUDE_DIRS",
            ".git,.venv,venv,node_modules,app,index,__pycache__,.mypy_cache,.pytest_cache,dist,build",
        ).split(",")
    )  # type: ignore[assignment]


settings = Settings()

if not settings.openai_api_key:
    # Delay hard failure until first API call so app can still boot and show UI
    pass

