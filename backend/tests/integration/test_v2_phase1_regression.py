import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.rag.retrieval.models import RetrievedChunk
from app.rag.retrieval.service import RetrievalService
from app.providers.gemini.provider import GeminiProvider

client = TestClient(app)

def test_v2_phase1_regression(monkeypatch):
    """
    Regression test proving that an existing normal RAG query returns:
    - answer
    - sources
    - chunk_count
    - generation_time_ms
    - decision
    And reaches the DIRECT_ANSWER + GOOD path.
    """
    def mock_retrieve(self, q):
        return [
            RetrievedChunk(
                document_id="123",
                filename="regression_test.pdf",
                chunk_index=0,
                chunk_text="This is a test chunk containing the answer.",
                similarity_score=0.95,
                page_numbers=[1, 2]
            )
        ]
    
    def mock_gemini(self, p):
        return "This is the generated answer."
        
    monkeypatch.setattr(RetrievalService, "retrieve", mock_retrieve)
    monkeypatch.setattr(GeminiProvider, "generate_answer", mock_gemini)
    
    response = client.post("/api/v1/chat/query", json={"question": "What is the answer?"})
    
    assert response.status_code == 200
    data = response.json()
    
    # Assert answer exists
    assert "answer" in data
    assert data["answer"] == "This is the generated answer."
    
    # Assert sources exist and have page_numbers
    assert "sources" in data
    assert len(data["sources"]) == 1
    assert data["sources"][0]["page_numbers"] == [1, 2]
    
    # Assert chunk_count
    assert "chunk_count" in data
    assert data["chunk_count"] == 1
    
    # Assert generation_time_ms
    assert "generation_time_ms" in data
    assert type(data["generation_time_ms"]) is int
    
    # Assert decision metadata
    assert "decision" in data
    decision = data["decision"]
    assert decision["path"] == "DIRECT_ANSWER"
    assert decision["retrieval_quality"] == "GOOD"
    assert decision["original_query"] == "What is the answer?"
    assert decision["current_query"] == "What is the answer?"
