import os
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config.settings import settings
import uuid

client = TestClient(app)

def test_empty_question():
    response = client.post("/api/v1/chat/query", json={"question": "   "})
    assert response.status_code == 400
    assert "Question cannot be empty" in response.json()["detail"]

def test_missing_gemini_key(monkeypatch):
    monkeypatch.setattr(settings, "GEMINI_API_KEY", None)
    # The provider initializes lazily, let's force a re-init by bypassing the singleton or mocking it
    from app.providers.gemini.provider import GeminiProvider
    provider = GeminiProvider()
    with pytest.raises(ValueError, match="GEMINI_API_KEY is not set"):
        _ = provider.client

def test_qdrant_unavailable(monkeypatch):
    monkeypatch.setattr(settings, "QDRANT_URL", "http://localhost:9999")
    from app.providers.qdrant.provider import QdrantProvider
    with pytest.raises(Exception):
        QdrantProvider()

def test_valid_query(monkeypatch):
    # Mock retrieval and gemini
    from app.rag.retrieval.models import RetrievedChunk
    from app.schemas.chat import ChatQueryResponse
    from app.rag.retrieval.service import RetrievalService
    from app.providers.gemini.provider import GeminiProvider
    
    def mock_retrieve(self, q):
        return [
            RetrievedChunk(document_id="1", filename="test.pdf", chunk_index=0, chunk_text="The capital of France is Paris.", similarity_score=0.9, page_number=1)
        ]
    
    def mock_gemini(self, p):
        return "Paris"
        
    monkeypatch.setattr(RetrievalService, "retrieve", mock_retrieve)
    monkeypatch.setattr(GeminiProvider, "generate_answer", mock_gemini)
    
    response = client.post("/api/v1/chat/query", json={"question": "What is the capital of France?"})
    assert response.status_code == 200
    data = response.json()
    assert data["answer"] == "Paris"
    assert len(data["sources"]) == 1
    assert data["chunk_count"] == 1

def test_irrelevant_query(monkeypatch):
    # Mock retrieval and gemini
    from app.rag.retrieval.models import RetrievedChunk
    from app.schemas.chat import ChatQueryResponse
    from app.rag.retrieval.service import RetrievalService
    from app.providers.gemini.provider import GeminiProvider
    
    def mock_retrieve(self, q):
        return [
            RetrievedChunk(document_id="1", filename="test.pdf", chunk_index=0, chunk_text="Apples are red.", similarity_score=0.9, page_number=1)
        ]
    
    def mock_gemini(self, p):
        return "I couldn't find the answer in the uploaded documents."
        
    monkeypatch.setattr(RetrievalService, "retrieve", mock_retrieve)
    monkeypatch.setattr(GeminiProvider, "generate_answer", mock_gemini)
    
    response = client.post("/api/v1/chat/query", json={"question": "What is the capital of France?"})
    assert response.status_code == 200
    data = response.json()
    assert data["answer"] == "I couldn't find the answer in the uploaded documents."

def test_no_indexed_documents(monkeypatch):
    from app.rag.retrieval.service import RetrievalService
    
    def mock_retrieve(self, q):
        return []
        
    monkeypatch.setattr(RetrievalService, "retrieve", mock_retrieve)
    
    response = client.post("/api/v1/chat/query", json={"question": "What is the capital of France?"})
    assert response.status_code == 200
    data = response.json()
    assert data["answer"] is None
    assert data["clarification"] is not None
    assert "I couldn't find enough information" in data["clarification"]
