from __future__ import annotations

import json
from typing import List, Dict
from urllib.parse import quote

import httpx
from bs4 import BeautifulSoup

from ..config import settings


DUCKDUCKGO_HTML = "https://duckduckgo.com/html/?q={query}"
JINA_READER = "https://r.jina.ai/http://{url}"


async def fetch_text(client: httpx.AsyncClient, url: str) -> str:
    try:
        # Use Jina Reader to simplify (no JS) and avoid CORS
        reader_url = JINA_READER.format(url=url)
        r = await client.get(reader_url, timeout=15)
        r.raise_for_status()
        return r.text
    except Exception:
        return ""


async def ddg_search(query: str, k: int | None = None) -> List[Dict]:
    if not settings.web_search_enabled:
        return []
    limit = k or settings.max_web_results
    async with httpx.AsyncClient(follow_redirects=True) as client:
        url = DUCKDUCKGO_HTML.format(query=quote(query))
        r = await client.get(url, timeout=15)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        results = []
        for a in soup.select("a.result__a"):
            href = a.get("href")
            title = a.get_text(strip=True)
            if not href:
                continue
            text = await fetch_text(client, href)
            if not text:
                continue
            results.append({"url": href, "title": title, "content": text[:5000]})
            if len(results) >= limit:
                break
        return results

