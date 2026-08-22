import pytest
from app.features.self_correction.planner import self_correction_planner
from app.features.context_evaluation.models import ContextEvaluation, ContextQuality

def create_eval(s1: str, s2: str) -> ContextEvaluation:
    return ContextEvaluation(
        quality=ContextQuality.UNCERTAIN,
        best_score=0.9,
        average_score=0.9,
        retrieved_chunks=2,
        conflict_detected=True,
        conflicting_sentences=(s1, s2)
    )

def test_numeric_conflict():
    query = "What is the CPU speed?"
    s1 = "The CPU operates at 3 GHz."
    s2 = "The CPU operates at 2.5 GHz."

    result = self_correction_planner.plan(query, create_eval(s1, s2))

    assert "CPU speed" in result
    assert "cpu" in result.lower()
    assert "operates" in result.lower()
    assert "ghz" in result.lower()
    assert "3" not in result
    assert "2.5" not in result

def test_explicit_negation_conflict():
    query = "Is the server online?"
    s1 = "The server is online."
    s2 = "The server is not online."

    result = self_correction_planner.plan(query, create_eval(s1, s2))

    assert "server online" in result
    assert "server" in result.lower()
    assert "online" in result.lower()
    assert "not" not in result.lower().split()

def test_categorical_conflict():
    query = "What is the cooling system status?"
    s1 = "The cooling system is enabled."
    s2 = "The cooling system is disabled."

    result = self_correction_planner.plan(query, create_eval(s1, s2))

    assert "cooling system" in result
    assert "enabled" not in result.lower()
    assert "disabled" not in result.lower()

def test_stop_word_filtering():
    query = "Tell me about it."
    s1 = "The cat is on the mat."
    s2 = "The cat is not on the mat."

    result = self_correction_planner.plan(query, create_eval(s1, s2))

    words = result.lower().split()
    stop_words = {"the", "is", "at", "of", "a", "an", "and", "to", "not"}

    for w in stop_words:
        assert w not in words[4:] # ignore "Tell me about it" part

def test_no_useful_intersection():
    query = "What is fact 1?"
    s1 = "Apples are red."
    s2 = "Bananas are yellow."

    result = self_correction_planner.plan(query, create_eval(s1, s2))

    assert "exact correct value" in result

def test_query_preservation():
    query = "Does the system support IPv6?"
    s1 = "IPv6 is supported."
    s2 = "IPv6 is unsupported."

    result = self_correction_planner.plan(query, create_eval(s1, s2))

    assert "Does the system support IPv6" in result
