import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app
from app.config.settings import settings
import io

client = TestClient(app)

def test_chat_query_length_limit():
    long_question = "A" * (settings.MAX_CHAT_QUERY_LENGTH + 1)
    response = client.post("/api/v1/chat/query", json={"question": long_question})
    assert response.status_code == 400
    assert "exceeds maximum length" in response.json()["detail"]

def test_chat_query_empty():
    response = client.post("/api/v1/chat/query", json={"question": "   "})
    assert response.status_code == 400
    assert "cannot be empty" in response.json()["detail"]

@patch('app.api.endpoints.documents.document_mapper.map_to_response')
@patch('app.api.endpoints.documents.processor.process')
def test_document_upload_path_traversal(mock_process, mock_mapper):
    mock_process.return_value = MagicMock()
    mock_mapper.return_value = {
        "status": "success",
        "message": "Document processed",
        "data": {
            "document_id": "123",
            "filename": "secret.txt",
            "sha256": "fake",
            "file_size": 100,
            "chunk_count": 1,
            "document_type": "text/plain",
            "upload_timestamp": "timestamp",
            "preview": "preview",
            "processing_summary": {"total_chunks": 1, "successful_chunks": 1, "failed_chunks": 0},
            "indexing_summary": {"vector_store": True, "cache_updated": False}
        }
    }

    # Uploading a file with path traversal characters in filename
    file_content = b"Some valid content."
    response = client.post(
        "/api/v1/documents/upload",
        files={"file": ("../../../../secret.txt", io.BytesIO(file_content), "text/plain")}
    )

    assert response.status_code == 200
    # Process should receive the safely resolved basename
    called_filename = mock_process.call_args[1]["filename"]
    assert called_filename == "secret.txt"

def test_document_empty_upload():
    response = client.post(
        "/api/v1/documents/upload",
        files={"file": ("empty.txt", io.BytesIO(b""), "text/plain")}
    )

    assert response.status_code == 400
    assert "Cannot process an empty file" in response.json()["detail"]

def test_document_upload_max_size():
    # Simulate a file larger than MAX_UPLOAD_SIZE_BYTES
    large_content = b"0" * (settings.MAX_UPLOAD_SIZE_BYTES + 1024)
    response = client.post(
        "/api/v1/documents/upload",
        files={"file": ("large.txt", io.BytesIO(large_content), "text/plain")}
    )

    assert response.status_code == 400
    assert "exceeds maximum allowed size" in response.json()["detail"]

def test_self_correction_max_attempts_guard():
    from app.features.self_correction.service import self_correction_service
    from app.features.context_evaluation.models import ContextEvaluation, ContextQuality

    eval_mock = ContextEvaluation(
        quality=ContextQuality.UNCERTAIN,
        relevance_score=0, answerability_score=0, coverage_score=0,
        best_score=0, average_score=0, reason="test",
        conflict_detected=True,
        conflict_reason="test",
        conflicting_sentences=("A", "B"),
        retrieved_chunks=0
    )

    # Passing 2 should raise the RuntimeError (since 1 is allowed)
    with pytest.raises(RuntimeError) as exc_info:
        self_correction_service.correct("What is the speed?", eval_mock, current_attempts=2)

    assert "Maximum self-correction attempts exceeded" in str(exc_info.value)
