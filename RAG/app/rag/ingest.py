from __future__ import annotations

from pathlib import Path
from typing import List

import numpy as np

from ..config import settings
from .files import iter_files, load_document_text
from .chunking import chunk_text
from .embeddings import embed_texts
from .index_store import save_index, load_index


def collect_corpus() -> tuple[List[str], List[dict]]:
    texts: List[str] = []
    metadatas: List[dict] = []
    for path in iter_files("."):
        content = load_document_text(path)
        if not content:
            continue
        chunks = chunk_text(content)
        for idx, chunk in enumerate(chunks):
            if not chunk.strip():
                continue
            texts.append(chunk)
            metadatas.append({
                "source": str(path),
                "chunk_index": idx,
                "text": chunk,
            })
    return texts, metadatas


def build_index() -> None:
    texts, metadatas = collect_corpus()
    if not texts:
        # create empty index placeholders
        vectors = np.zeros((0, 1536), dtype=np.float32)
        save_index(settings.index_dir, vectors, metadatas)
        return
    # If API key is missing, skip embedding at startup
    if not settings.openai_api_key:
        return
    vectors = embed_texts(texts)
    save_index(settings.index_dir, vectors, metadatas)


def build_index_if_needed() -> bool:
    idx = load_index(settings.index_dir)
    if idx is not None:
        return True
    build_index()
    return True


def force_rebuild_index() -> None:
    build_index()

