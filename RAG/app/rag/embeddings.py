from __future__ import annotations

from typing import List

import numpy as np
from openai import OpenAI

from ..config import settings


_client: OpenAI | None = None


def get_client() -> OpenAI:
    global _client
    if _client is None:
        if not settings.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY is not set")
        _client = OpenAI(
            api_key=settings.openai_api_key,
            base_url=settings.openai_base_url or None,
        )
    return _client


def _estimate_tokens(text: str) -> int:
    # Rough heuristic: ~4 chars per token
    return max(1, len(text) // 4)


def embed_texts(texts: List[str]) -> np.ndarray:
    """Embed texts with batching to respect per-request token limits."""
    if not texts:
        return np.zeros((0, 1536), dtype=np.float32)

    client = get_client()

    MAX_TOKENS_PER_REQUEST = 250_000
    MAX_ITEMS_PER_BATCH = 128

    batches: list[list[str]] = []
    current_batch: list[str] = []
    current_tokens = 0

    for t in texts:
        t_tokens = _estimate_tokens(t)
        if (
            current_batch
            and (current_tokens + t_tokens > MAX_TOKENS_PER_REQUEST or len(current_batch) >= MAX_ITEMS_PER_BATCH)
        ):
            batches.append(current_batch)
            current_batch = []
            current_tokens = 0
        current_batch.append(t)
        current_tokens += t_tokens

    if current_batch:
        batches.append(current_batch)

    all_vectors: list[np.ndarray] = []
    for batch in batches:
        # Primary path: batch request
        try:
            resp = client.embeddings.create(model=settings.embedding_model, input=batch)
            vectors = [np.array(item.embedding, dtype=np.float32) for item in resp.data]
            all_vectors.append(np.vstack(vectors))
            continue
        except Exception:
            # Fallback to per-item to get as much as possible
            for item in batch:
                try:
                    resp = client.embeddings.create(model=settings.embedding_model, input=[item])
                    vec = np.array(resp.data[0].embedding, dtype=np.float32)
                    all_vectors.append(vec.reshape(1, -1))
                except Exception:
                    # Skip problematic item to avoid blocking entire indexing
                    pass

    if not all_vectors:
        return np.zeros((0, 1536), dtype=np.float32)
    return np.vstack(all_vectors)

