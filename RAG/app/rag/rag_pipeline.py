from __future__ import annotations

from typing import List

from openai import OpenAI

from ..config import settings
from .retriever import Retriever
from ..websearch.search import ddg_search
from .embeddings import get_client


SYSTEM_PROMPT = (
    "You are a helpful programming assistant. Answer based on the provided context snippets from the user's local docs. "
    "If the answer isn't in the context, say you are unsure and suggest where to look."
)


def build_messages(question: str, contexts: List[dict], web_snippets: List[dict] | None = None) -> list:
    context_text = "\n\n".join(
        f"Source: {c.get('source')}\n---\n{c.get('text', '')}" for c in contexts
    )
    web_text = ""
    if web_snippets:
        web_text = "\n\n" + "\n\n".join(
            f"Web: {w.get('title')} ({w.get('url')})\n---\n{w.get('content','')}" for w in web_snippets
        )
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": ("Use the following context to answer the question.\n\n" + context_text + web_text + "\n\nQuestion: " + question),
        },
    ]


async def chat_with_rag(question: str, retriever: Retriever, use_web: bool = False) -> dict:
    results = retriever.search(question, k=5)
    contexts: List[dict] = []
    for score, meta in results:
        contexts.append({
            "source": meta.get("source"),
            "score": score,
            "text": meta.get("text", ""),
        })

    web_snippets: List[dict] = []
    if use_web:
        try:
            web_snippets = await ddg_search(question, k=3)
        except Exception:
            web_snippets = []

    messages = build_messages(question, contexts, web_snippets)
    client: OpenAI = get_client()
    chat = client.chat.completions.create(
        model=settings.chat_model,
        messages=messages,
        temperature=0.2,
    )
    content = chat.choices[0].message.content or ""
    return {"answer": content, "sources": contexts, "web": web_snippets}

