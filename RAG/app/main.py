from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .config import settings
from .rag.ingest import force_rebuild_index
from .rag.retriever import Retriever
from .rag.rag_pipeline import chat_with_rag


app = FastAPI(title="RAG Chatbot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


static_dir = Path(__file__).parent / "static"
static_dir.mkdir(parents=True, exist_ok=True)


retriever: Retriever | None = None


@app.on_event("startup")
async def on_startup() -> None:
    global retriever
    retriever = Retriever(index_dir=settings.index_dir, embedding_model=settings.embedding_model)


@app.post("/api/ingest")
async def ingest() -> dict:
    force_rebuild_index()
    global retriever
    retriever = Retriever(index_dir=settings.index_dir, embedding_model=settings.embedding_model)
    return {"status": "ok"}


@app.post("/api/chat")
async def chat(payload: dict) -> dict:
    question = (payload or {}).get("message", "").strip()
    use_web = bool((payload or {}).get("use_web", False))
    if not question:
        raise HTTPException(status_code=400, detail="message is required")
    if retriever is None:
        raise HTTPException(status_code=500, detail="retriever not ready")
    answer = await chat_with_rag(question=question, retriever=retriever, use_web=use_web)
    return answer

# Mount static last so API routes take precedence
app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")

