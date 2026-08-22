import pytest
from evaluation.metrics.hallucination import calculate_metrics, check_hallucination

def test_check_hallucination():
    case = {
        "should_abstain": True,
        "unsupported_claims": ["bad claim"],
        "supported_claims": ["good claim"]
    }

    # Confident answer when should abstain
    assert check_hallucination(case, "DIRECT_ANSWER", "good claim", ["good claim"]) is True

    # Safe abstention is not a hallucination
    assert check_hallucination(case, "ASK_FOR_CLARIFICATION", "I couldn't find the answer", ["good claim"]) is False

    case_no_abstain = {
        "should_abstain": False,
        "unsupported_claims": ["bad claim"],
        "supported_claims": ["good claim"]
    }

    # Unsupported claim generated
    assert check_hallucination(case_no_abstain, "DIRECT_ANSWER", "bad claim", ["good claim"]) is True

    # Supported claim but not in context
    assert check_hallucination(case_no_abstain, "DIRECT_ANSWER", "good claim", []) is True

    # Valid answer
    assert check_hallucination(case_no_abstain, "DIRECT_ANSWER", "good claim", ["good claim"]) is False

def test_check_hallucination_normalization():
    case = {
        "should_abstain": False,
        "unsupported_claims": ["The server is offline."],
        "supported_claims": ["The server is online."]
    }

    # 1. "The server is online." is supported by "The server is online and healthy."
    assert check_hallucination(case, "DIRECT_ANSWER", "The server is online.", ["The server is online and healthy."]) is False

    # 2. punctuation differences do not create hallucinations
    assert check_hallucination(case, "DIRECT_ANSWER", "The server is online", ["The server is online."]) is False
    assert check_hallucination(case, "DIRECT_ANSWER", "The server is online.", ["The server is online"]) is False

    # 3. genuinely unsupported claims are still detected
    assert check_hallucination(case, "DIRECT_ANSWER", "The server is offline.", ["The server is online and healthy."]) is True

    # 4. claim generated but not in context at all
    assert check_hallucination(case, "DIRECT_ANSWER", "The server is online.", ["The database is running."]) is True

def test_calculate_metrics():
    dataset = [
        {
            "id": "1",
            "category": "ANSWERABLE",
            "should_abstain": False,
            "unsupported_claims": ["bad claim"],
            "supported_claims": ["good claim"],
            "initial_context": ["good claim"],
            "corrective_context": []
        },
        {
            "id": "2",
            "category": "CONFLICTING_CONTEXT",
            "should_abstain": True,
            "unsupported_claims": ["bad claim 2"],
            "supported_claims": ["good claim 2"],
            "initial_context": ["good claim 2", "bad claim 2"],
            "corrective_context": ["good claim 2"]
        }
    ]

    baseline_results = {
        "1": {"behavior": "DIRECT_ANSWER", "answer": "good claim"},
        "2": {"behavior": "DIRECT_ANSWER", "answer": "good claim 2 bad claim 2"}
    }

    sentinel_results = {
        "1": {"behavior": "DIRECT_ANSWER", "answer": "good claim"},
        "2": {"behavior": "DIRECT_ANSWER", "answer": "good claim 2", "corrected": True}
    }

    metrics = calculate_metrics(dataset, baseline_results, sentinel_results)

    assert metrics["baseline"]["hallucinations"] == 1 # Case 2
    assert metrics["baseline"]["correct"] == 1 # Case 1

    assert metrics["sentinelrag"]["hallucinations"] == 0
    assert metrics["sentinelrag"]["correct"] == 2 # Case 2 is corrected

    assert metrics["comparison"]["absolute_hallucination_reduction"] == 50.0
    assert metrics["comparison"]["relative_hallucination_reduction"] == 100.0

    assert metrics["self_correction"]["conflict_cases"] == 1
    assert metrics["self_correction"]["conflicts_resolved"] == 1
