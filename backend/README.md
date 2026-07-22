# SentinelRAG Backend

This is the FastAPI backend for SentinelRAG. It provides endpoints for document ingestion (chunking, embedding, vector storage) and retrieval-augmented generation (RAG) using Gemini and Qdrant.

## Required Environment Variables

Before running the backend, create a `.env.backend` file at the root of the project (`c:\SentinelRAG\.env.backend`) with the following required variables:

```env
GEMINI_API_KEY=your_google_gemini_api_key
GEMINI_MODEL=gemini-3.5-flash-lite
QDRANT_URL=http://localhost:6333
QDRANT_COLLECTION=sentinelrag_docs
RETRIEVAL_TOP_K=3
RETRIEVAL_SCORE_THRESHOLD=0.3
```

## How to Run the Backend

To run the backend server in development mode with live reloading:

```bash
cd backend
uv run uvicorn app.main:app --reload
```
The server will start at `http://127.0.0.1:8000`.

## How to Upload Documents

You can upload PDF or TXT documents to the ingestion pipeline using the `/api/v1/documents/upload` endpoint. 
It supports multiple files in a single request.

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/documents/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "files=@/path/to/your/document.pdf"
```

## How to Query the System

To ask a question based on the uploaded documents, use the `/api/v1/chat/query` endpoint:

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/chat/query" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is CRUD?"}'
```

The system will return the generated answer along with the source metadata (document IDs, filenames, page numbers, etc.) used to construct the answer.
