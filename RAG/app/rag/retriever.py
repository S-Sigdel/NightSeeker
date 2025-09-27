from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

import numpy as np

from ..config import settings
from .embeddings import embed_texts
from .index_store import load_index, top_k_similar


@dataclass
class Retriever:
    index_dir: str
    embedding_model: str

    def __post_init__(self) -> None:
        self._index = load_index(self.index_dir)
        if self._index is None:
            self._vectors = np.zeros((0, 1536), dtype=np.float32)
        else:
            self._vectors = self._index.vectors

    def search(self, query: str, k: int = 5) -> List[Tuple[float, dict]]:
        if self._index is None or self._index.vectors.shape[0] == 0:
            return []
        query_vec = embed_texts([query])[0]
        return top_k_similar(query_vec, self._index, k=k)

