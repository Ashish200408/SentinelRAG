import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config.settings import settings
from app.features.context_evaluation.evaluator import context_evaluator
from app.features.context_evaluation.models import ContextEvaluation, ContextQuality

client = TestClient(app)

@pytest.mark.integration
def test_phase5_direct_answer(monkeypatch):
    if not settings.GEMINI_API_KEY:
        pytest.skip("GEMINI_API_KEY is not set")
        
    def mock_evaluate(chunks):
        return ContextEvaluation(quality=ContextQuality.GOOD, best_score=0.9, average_score=0.85, retrieved_chunks=len(chunks))
    monkeypatch.setattr(context_evaluator, "evaluate", mock_evaluate)
        
    response = client.post("/api/v1/chat/query", json={"question": "What is CRUD?"})
    assert response.status_code == 200
    data = response.json()
    
    assert data["decision"]["path"] == "DIRECT_ANSWER"
    assert data["decision"]["rewritten"] is False
    assert "confidence" in data["decision"]
    assert data["answer"] is not None
    assert data["clarification"] is None

@pytest.mark.integration
def test_phase5_rewrite_triggered(monkeypatch):
    if not settings.GEMINI_API_KEY:
        pytest.skip("GEMINI_API_KEY is not set")
        
    # We will mock context evaluator to force the first attempt to be LOW_CONFIDENCE 
    # and the second attempt to be GOOD, to ensure the decision engine works.
    original_evaluate = context_evaluator.evaluate
    
    attempt_count = 0
    def mock_evaluate(chunks):
        nonlocal attempt_count
        attempt_count += 1
        if attempt_count == 1:
            return ContextEvaluation(quality=ContextQuality.LOW_CONFIDENCE, best_score=0.4, average_score=0.4, retrieved_chunks=1)
        return ContextEvaluation(quality=ContextQuality.GOOD, best_score=0.9, average_score=0.9, retrieved_chunks=1)
        
    monkeypatch.setattr(context_evaluator, "evaluate", mock_evaluate)

    response = client.post("/api/v1/chat/query", json={"question": "Explain CRUD functions"})
    assert response.status_code == 200
    data = response.json()
    
    assert data["decision"]["path"] == "DIRECT_ANSWER" # because the second attempt was GOOD
    assert data["decision"]["rewritten"] is True
    assert data["decision"]["retrieval_attempts"] == 2
    assert data["decision"]["rewritten_query"] is not None
    assert data["answer"] is not None

@pytest.mark.integration
def test_phase5_ask_clarification():
    if not settings.GEMINI_API_KEY:
        pytest.skip("GEMINI_API_KEY is not set")
        
    response = client.post("/api/v1/chat/query", json={"question": "Tell me about Kubernetes"})
    assert response.status_code == 200
    data = response.json()
    
    assert data["decision"]["path"] == "ASK_FOR_CLARIFICATION"
    assert data["clarification"] is not None
    assert "I couldn't find enough information" in data["clarification"]
    assert data["answer"] is None
