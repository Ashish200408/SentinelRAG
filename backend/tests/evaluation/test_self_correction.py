import pytest
from unittest.mock import patch, MagicMock

from app.rag.pipeline.rag_service import rag_service
from app.rag.retrieval.models import RetrievedChunk

def create_chunk(text: str, score: float = 0.8) -> RetrievedChunk:
    return RetrievedChunk(
        chunk_id="test_id",
        document_id="test_doc",
        filename="test.txt",
        chunk_index=0,
        similarity_score=score,
        chunk_text=text
    )

@pytest.fixture
def mock_gemini():
    with patch('app.rag.pipeline.rag_service.gemini_provider.generate_answer') as mock:
        mock.return_value = "Mocked answer"
        yield mock

@pytest.fixture
def mock_semantic():
    with patch('app.features.context_evaluation.evaluator.semantic_evaluator.evaluate') as mock:
        mock_result = MagicMock()
        mock_result.answerable = True
        mock_result.confidence = 0.9
        mock_result.reason = "Mock semantic reason"
        mock.return_value = mock_result
        yield mock

@pytest.fixture
def mock_retrieval():
    with patch('app.rag.pipeline.rag_service.retrieval_service.retrieve') as mock:
        yield mock

def test_1_conflict_resolved_after_correction(mock_retrieval, mock_gemini):
    # Initial retrieval: conflict (3 GHz vs 2.5 GHz)
    mock_retrieval.side_effect = [
        [
            create_chunk("The processor operates at 3 GHz."),
            create_chunk("The processor operates at 2.5 GHz.")
        ],
        # Second retrieval: resolved (both agree)
        [
            create_chunk("The processor operates at 3 GHz."),
            create_chunk("The processor clock speed is 3 GHz.")
        ]
    ]

    response = rag_service.answer_query("What is the processor clock speed?")

    assert mock_retrieval.call_count == 2
    assert response.decision.conflict_resolved is True
    assert response.decision.correction_attempts == 1
    assert response.decision.path == "DIRECT_ANSWER"

def test_2_conflict_persists(mock_retrieval, mock_gemini):
    # Initial and second retrieval: same conflict
    mock_retrieval.side_effect = [
        [
            create_chunk("The processor operates at 3 GHz."),
            create_chunk("The processor operates at 2.5 GHz.")
        ],
        [
            create_chunk("The processor operates at 3 GHz."),
            create_chunk("The processor operates at 2.5 GHz.")
        ]
    ]

    response = rag_service.answer_query("What is the processor clock speed?")

    assert mock_retrieval.call_count == 2
    assert response.decision.conflict_resolved is False
    assert response.decision.correction_attempts == 1
    assert response.decision.path in ["ASK_FOR_CLARIFICATION", "CONFLICT_DETECTED"]
    assert response.answer is None

def test_3_corrective_retrieval_insufficient(mock_retrieval, mock_gemini):
    # Initial: conflict. Second: insufficient (low scores)
    mock_retrieval.side_effect = [
        [
            create_chunk("The processor operates at 3 GHz."),
            create_chunk("The processor operates at 2.5 GHz.")
        ],
        [
            create_chunk("It is a processor.", score=0.1)
        ]
    ]

    response = rag_service.answer_query("What is the processor clock speed?")

    assert mock_retrieval.call_count == 2
    assert response.decision.conflict_resolved is False
    assert response.decision.correction_attempts == 1
    assert response.decision.path in ["ASK_FOR_CLARIFICATION", "REWRITE_QUERY"]
    assert response.answer is None

def test_4_no_conflict(mock_retrieval, mock_gemini):
    # Initial: consistent context
    mock_retrieval.return_value = [
        create_chunk("The processor operates at 3 GHz."),
        create_chunk("The processor clock speed is 3 GHz.")
    ]

    response = rag_service.answer_query("What is the processor clock speed?")

    assert mock_retrieval.call_count == 1
    assert response.decision.correction_attempts == 0
    assert response.decision.corrective_query is None
    assert response.decision.path == "DIRECT_ANSWER"

def test_5_strong_context(mock_retrieval, mock_gemini):
    mock_retrieval.return_value = [
        create_chunk("The capital of France is Paris.", score=0.9)
    ]

    response = rag_service.answer_query("What is the capital of France?")

    assert mock_retrieval.call_count == 1
    assert response.decision.correction_attempts == 0
    assert response.decision.path == "DIRECT_ANSWER"

def test_6_maximum_attempt_guard(mock_retrieval, mock_gemini):
    # Setup infinite conflict
    mock_retrieval.return_value = [
        create_chunk("The processor operates at 3 GHz."),
        create_chunk("The processor operates at 2.5 GHz.")
    ]

    response = rag_service.answer_query("What is the processor clock speed?")

    assert mock_retrieval.call_count == 2
    assert response.decision.correction_attempts == 1

def test_7_corrective_query_quality(mock_retrieval, mock_gemini):
    mock_retrieval.side_effect = [
        [
            create_chunk("The processor operates at 3 GHz."),
            create_chunk("The processor operates at 2.5 GHz.")
        ],
        [
            create_chunk("The processor operates at 3 GHz.", score=0.9)
        ]
    ]

    response = rag_service.answer_query("What is the processor clock speed?")

    assert response.decision.correction_attempts == 1
    corrective = response.decision.corrective_query
    assert corrective is not None
    assert "processor clock speed" in corrective.lower()
    assert "exact" in corrective.lower()
    assert "2.5" not in corrective
    assert "3" not in corrective

def test_8_existing_phase_2_regression(mock_retrieval, mock_gemini, mock_semantic):
    # Semantic evaluation fallback for uncertain scores without conflict
    mock_retrieval.return_value = [
        create_chunk("The basic structure involves ALU and memory.", score=0.4) # UNCERTAIN score
    ]

    response = rag_service.answer_query("What is the Basic Structure of Computers?")

    assert mock_retrieval.call_count == 1
    assert response.decision.correction_attempts == 0
    assert response.decision.path == "DIRECT_ANSWER"
    mock_semantic.assert_called_once()
