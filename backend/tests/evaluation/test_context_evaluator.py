import pytest
from app.features.context_evaluation.evaluator import ContextEvaluator
from app.features.context_evaluation.models import ContextQuality
from app.rag.retrieval.models import RetrievedChunk
from app.features.context_evaluation.semantic import SemanticEvaluationResult

class MockSemanticEvaluator:
    def __init__(self, result):
        self.result = result
        self.called = False
    
    def evaluate(self, question, chunks_text):
        self.called = True
        if isinstance(self.result, Exception):
            raise self.result
        return self.result

def test_strong_context(monkeypatch):
    evaluator = ContextEvaluator()
    chunks = [
        RetrievedChunk(document_id="1", filename="test.txt", chunk_index=0, chunk_text="test", similarity_score=0.8, page_numbers=[1]),
        RetrievedChunk(document_id="1", filename="test.txt", chunk_index=1, chunk_text="test", similarity_score=0.7, page_numbers=[1])
    ]
    # No need to mock semantic evaluator, it shouldn't be called for strong context
    result = evaluator.evaluate("test query", chunks)
    assert result.quality == ContextQuality.GOOD
    assert result.relevance_score == 0.8

def test_weak_context(monkeypatch):
    evaluator = ContextEvaluator()
    chunks = [
        RetrievedChunk(document_id="1", filename="test.txt", chunk_index=0, chunk_text="test", similarity_score=0.1, page_numbers=[1])
    ]
    result = evaluator.evaluate("test query", chunks)
    assert result.quality == ContextQuality.INSUFFICIENT
    assert result.relevance_score == 0.1

def test_uncertain_context_semantic_true(monkeypatch):
    evaluator = ContextEvaluator()
    mock_semantic = MockSemanticEvaluator(SemanticEvaluationResult(answerable=True, confidence=0.9, reason="test"))
    monkeypatch.setattr("app.features.context_evaluation.evaluator.semantic_evaluator", mock_semantic)
    
    chunks = [
        RetrievedChunk(document_id="1", filename="test.txt", chunk_index=0, chunk_text="test", similarity_score=0.45, page_numbers=[1])
    ]
    result = evaluator.evaluate("test query", chunks)
    
    assert mock_semantic.called
    assert result.quality == ContextQuality.GOOD
    assert result.answerability_score == 0.9
    assert result.reason == "Semantic: test"

def test_uncertain_context_semantic_false(monkeypatch):
    evaluator = ContextEvaluator()
    mock_semantic = MockSemanticEvaluator(SemanticEvaluationResult(answerable=False, confidence=0.8, reason="not found"))
    monkeypatch.setattr("app.features.context_evaluation.evaluator.semantic_evaluator", mock_semantic)
    
    chunks = [
        RetrievedChunk(document_id="1", filename="test.txt", chunk_index=0, chunk_text="test", similarity_score=0.45, page_numbers=[1])
    ]
    result = evaluator.evaluate("test query", chunks)
    
    assert mock_semantic.called
    assert result.quality == ContextQuality.INSUFFICIENT
    assert result.answerability_score == 0.8
    assert result.reason == "Semantic: not found"

def test_uncertain_context_semantic_failure(monkeypatch):
    evaluator = ContextEvaluator()
    mock_semantic = MockSemanticEvaluator(None)
    monkeypatch.setattr("app.features.context_evaluation.evaluator.semantic_evaluator", mock_semantic)
    
    chunks = [
        RetrievedChunk(document_id="1", filename="test.txt", chunk_index=0, chunk_text="test", similarity_score=0.45, page_numbers=[1])
    ]
    result = evaluator.evaluate("test query", chunks)
    
    assert mock_semantic.called
    assert result.quality == ContextQuality.INSUFFICIENT
    assert "defaulting to insufficient context safely" in result.reason
