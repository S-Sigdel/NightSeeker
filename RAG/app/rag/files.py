from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable, List

from ..config import settings


TEXT_EXTS = {".txt", ".md", ".py", ".json", ".yaml", ".yml", ".rst", ".csv", ".ts", ".tsx", ".js", ".jsx"}
PDF_EXTS = {".pdf"}


def iter_files(root: str | Path = ".") -> Iterable[Path]:
    root = Path(root)
    excluded = set(settings.exclude_dirs)
    include_exts = set(ext.strip().lower() for ext in settings.include_exts if ext.strip())
    for dirpath, dirnames, filenames in os.walk(root):
        # prune excluded directories
        dirnames[:] = [d for d in dirnames if d not in excluded and not d.startswith(".")]
        for name in filenames:
            ext = Path(name).suffix.lower()
            if include_exts and ext not in include_exts:
                continue
            yield Path(dirpath) / name


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""


def read_pdf(path: Path) -> str:
    try:
        from pypdf import PdfReader

        reader = PdfReader(str(path))
        text = []
        for page in reader.pages:
            text.append(page.extract_text() or "")
        return "\n".join(text)
    except Exception:
        return ""


def load_document_text(path: Path) -> str:
    ext = path.suffix.lower()
    if ext in TEXT_EXTS:
        return read_text(path)
    if ext in PDF_EXTS:
        return read_pdf(path)
    return ""

