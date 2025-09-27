from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

import numpy as np


@dataclass
class Index:
    vectors: np.ndarray  # shape (N, D)
    metadatas: List[dict]


def save_index(index_dir: str | Path, vectors: np.ndarray, metadatas: List[dict]) -> None:
    path = Path(index_dir)
    path.mkdir(parents=True, exist_ok=True)
    np.save(str(path / "vectors.npy"), vectors)
    with (path / "metadatas.json").open("w", encoding="utf-8") as f:
        json.dump(metadatas, f, ensure_ascii=False, indent=2)


def load_index(index_dir: str | Path) -> Index | None:
    path = Path(index_dir)
    vec_path = path / "vectors.npy"
    meta_path = path / "metadatas.json"
    if not vec_path.exists() or not meta_path.exists():
        return None
    vectors = np.load(str(vec_path))
    metadatas = json.loads(meta_path.read_text(encoding="utf-8"))
    return Index(vectors=vectors, metadatas=metadatas)


def cosine_similarity(query: np.ndarray, matrix: np.ndarray) -> np.ndarray:
    # normalize
    q = query / (np.linalg.norm(query) + 1e-10)
    m = matrix / (np.linalg.norm(matrix, axis=1, keepdims=True) + 1e-10)
    return m @ q


def top_k_similar(query_vec: np.ndarray, index: Index, k: int = 5) -> List[Tuple[float, dict]]:
    sims = cosine_similarity(query_vec, index.vectors)
    order = np.argsort(-sims)[:k]
    return [(float(sims[i]), index.metadatas[i]) for i in order]

