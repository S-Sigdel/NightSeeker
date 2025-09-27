## RAG Chatbot (FastAPI + OpenAI)

This project provides a minimal Retrieval-Augmented Generation (RAG) chatbot over local documents in the current directory.

### Features
- FastAPI backend with a simple chat UI
- Ingestion from common text formats (.txt, .md, .py, .json) and PDFs
- Chunking + OpenAI embeddings, local NumPy index, cosine similarity search
- Chat endpoint with RAG context and source attributions

### Quickstart
1. Ensure your `.env` file contains at least:
   - `OPENAI_API_KEY=...`
   - Optional: `OPENAI_BASE_URL=...` (for non-default endpoints)
   - Optional: `EMBEDDING_MODEL=text-embedding-3-small`
   - Optional: `CHAT_MODEL=gpt-4o-mini`

2. Install deps and run the server:
```bash
bash run.sh
```

3. Open `http://127.0.0.1:8000/` to chat.

4. Re-ingest documents anytime:
```bash
curl -X POST http://127.0.0.1:8000/ingest
```

### Notes
- Index files are stored under `index/`.
- The server will auto-ingest on first run if no index exists.

