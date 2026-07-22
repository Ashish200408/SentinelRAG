import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config.settings import settings

client = TestClient(app)

from app.features.context_evaluation.evaluator import context_evaluator
from app.features.context_evaluation.models import ContextEvaluation, ContextQuality

@pytest.mark.integration
def test_chat_happy_path(monkeypatch):
    """
    Tests the happy path where a valid question is asked about the indexed documents.
    Requires Qdrant to be running and Gemini API key to be set.
    """
    if not settings.GEMINI_API_KEY:
        pytest.skip("GEMINI_API_KEY is not set")
        
    def mock_evaluate(chunks):
        return ContextEvaluation(quality=ContextQuality.GOOD, best_score=0.9, average_score=0.85, retrieved_chunks=len(chunks))
    monkeypatch.setattr(context_evaluator, "evaluate", mock_evaluate)
        
    response = client.post("/api/v1/chat/query", json={"question": "What is CRUD?"})
    assert response.status_code == 200
    
    data = response.json()
    assert data["answer"] is not None
    assert "I couldn't find the answer" not in data["answer"]
    assert data["chunk_count"] > 0
    assert len(data["sources"]) > 0
    
    # Verify chunk_text is NOT in the response
    for source in data["sources"]:
        assert "chunk_text" not in source
        assert "page_number" in source

@pytest.mark.integration
def test_chat_fallback():
    """
    Tests the fallback path where an irrelevant question is asked.
    Gemini should reply that it couldn't find the answer.
    """
    if not settings.GEMINI_API_KEY:
        pytest.skip("GEMINI_API_KEY is not set")
        
    response = client.post("/api/v1/chat/query", json={"question": "What is the capital of Mars?"})
    assert response.status_code == 200
    
    data = response.json()
    assert data["answer"] is None
    assert data["clarification"] is not None
    assert "I couldn't find enough information" in data["clarification"]
