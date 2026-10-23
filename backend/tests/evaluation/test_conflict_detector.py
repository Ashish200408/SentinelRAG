import pytest
from app.features.context_evaluation.conflict import conflict_detector
from app.rag.retrieval.models import RetrievedChunk

def create_chunk(index: int, text: str) -> RetrievedChunk:
    return RetrievedChunk(
        document_id="doc1",
        filename="test.txt",
        chunk_index=index,
        chunk_text=text,
        similarity_score=0.9
    )

def test_no_conflict_for_consistent_context():
    query = "What is the processor clock speed?"
    chunks = [
        create_chunk(0, "The processor operates at 3 GHz."),
        create_chunk(1, "The processor operates at 3 GHz.")
    ]
    result = conflict_detector.detect(query, chunks)
    assert not result.conflict_detected
    assert result.conflicting_sentences == ("", "")

def test_conflict_for_different_numeric_values():
    query = "What is the processor clock speed?"
    chunks = [
        create_chunk(0, "The processor operates at 3 GHz."),
        create_chunk(1, "The processor operates at 2.5 GHz.")
    ]
    result = conflict_detector.detect(query, chunks)
    assert result.conflict_detected
    assert "numeric" in result.reason.lower()
    assert result.conflicting_chunk_indices == [0, 1]
    assert result.conflicting_sentences == ("The processor operates at 3 GHz.", "The processor operates at 2.5 GHz.")

def test_conflict_for_explicit_negation():
    query = "Is the cooling system operational?"
    chunks = [
        create_chunk(0, "The cooling system is operational."),
        create_chunk(1, "The cooling system is not operational.")
    ]
    result = conflict_detector.detect(query, chunks)
    assert result.conflict_detected
    assert "negation" in result.reason.lower()
    assert result.conflicting_sentences == ("The cooling system is operational.", "The cooling system is not operational.")

def test_conflict_for_opposing_categorical_values():
    query = "Is the cooling system enabled?"
    chunks = [
        create_chunk(0, "The cooling system is enabled."),
        create_chunk(1, "The cooling system is disabled.")
    ]
    result = conflict_detector.detect(query, chunks)
    assert result.conflict_detected
    assert "categorical" in result.reason.lower()
    assert result.conflicting_sentences == ("The cooling system is enabled.", "The cooling system is disabled.")

def test_no_conflict_for_unrelated_facts():
    query = "What is the processor clock speed?"
    chunks = [
        create_chunk(0, "The processor operates at 3 GHz."),
        create_chunk(1, "The processor architecture is 64-bit.")
    ]
    result = conflict_detector.detect(query, chunks)
    assert not result.conflict_detected
    assert result.conflicting_sentences == ("", "")

def test_no_conflict_with_single_chunk():
    query = "What is the processor clock speed?"
    chunks = [
        create_chunk(0, "The processor operates at 3 GHz.")
    ]
    result = conflict_detector.detect(query, chunks)
    assert not result.conflict_detected
    assert result.conflicting_sentences == ("", "")

def test_empty_context():
    query = "What is the processor clock speed?"
    chunks = []
    result = conflict_detector.detect(query, chunks)
    assert not result.conflict_detected
    assert result.conflicting_sentences == ("", "")

def test_multiple_consistent_chunks():
    query = "Is the cooling system enabled?"
    chunks = [
        create_chunk(0, "The cooling system is enabled."),
        create_chunk(1, "The cooling system is enabled."),
        create_chunk(2, "The cooling system is enabled.")
    ]
    result = conflict_detector.detect(query, chunks)
    assert not result.conflict_detected
    assert result.conflicting_sentences == ("", "")

def test_numeric_conflict_with_units():
    query = "What are the specs?"
    chunks = [
        create_chunk(0, "GPU memory is 8GB."),
        create_chunk(1, "GPU memory is 16GB.")
    ]
    result = conflict_detector.detect(query, chunks)
    assert result.conflict_detected
    assert result.conflicting_sentences == ("GPU memory is 8GB.", "GPU memory is 16GB.")

def test_numeric_conflict_decimals_with_units():
    query = "What is the frequency?"
    chunks = [
        create_chunk(0, "Processor operates at 2.5GHz."),
        create_chunk(1, "Processor operates at 3.0GHz.")
    ]
    result = conflict_detector.detect(query, chunks)
    assert result.conflict_detected
    assert result.conflicting_sentences == ("Processor operates at 2.5GHz.", "Processor operates at 3.0GHz.")

def test_numeric_conflict_large_numbers_with_units():
    query = "What is the capacity?"
    chunks = [
        create_chunk(0, "Battery capacity is 5000mAh."),
        create_chunk(1, "Battery capacity is 4000mAh.")
    ]
    result = conflict_detector.detect(query, chunks)
    assert result.conflict_detected

def test_unrelated_facts_with_different_units():
    query = "What are the specs?"
    chunks = [
        create_chunk(0, "Battery capacity is 5000mAh."),
        create_chunk(1, "CPU cache is 16MB.")
    ]
    result = conflict_detector.detect(query, chunks)
    assert not result.conflict_detected

def test_identical_numeric_values_with_units():
    query = "What are the specs?"
    chunks = [
        create_chunk(0, "GPU memory is 8GB."),
        create_chunk(1, "GPU memory is 8GB.")
    ]
    result = conflict_detector.detect(query, chunks)
    assert not result.conflict_detected
