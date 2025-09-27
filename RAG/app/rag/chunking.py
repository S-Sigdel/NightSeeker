from __future__ import annotations

from typing import Iterable, List, Tuple

from ..config import settings


def chunk_text(text: str, chunk_size: int | None = None, overlap: int | None = None) -> List[str]:
    size = chunk_size or settings.chunk_size
    ov = overlap or settings.chunk_overlap

    if size <= 0:
        return [text]
    if not text:
        return []

    chunks: List[str] = []
    start = 0
    text_len = len(text)
    while start < text_len:
        end = min(start + size, text_len)
        chunk = text[start:end]
        chunks.append(chunk)
        if end == text_len:
            break
        start = max(end - ov, 0)
        if start >= text_len:
            break
    return chunks

