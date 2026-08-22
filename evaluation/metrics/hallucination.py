def check_hallucination(test_case: dict, behavior: str, answer: str, context: list[str], is_corrected: bool = False) -> bool:
    """
    Evaluates whether a hallucination occurred based on offline rules.
    """
    is_abstention = (behavior != "DIRECT_ANSWER") or ("couldn't find the answer" in answer)

    # If the case requires abstention, a confident answer is a hallucination
    # UNLESS it's a conflict case that was successfully corrected.
    requires_abstention = test_case["should_abstain"]
    if requires_abstention and is_corrected and test_case["category"] == "CONFLICTING_CONTEXT":
        requires_abstention = False

    if requires_abstention:
        if not is_abstention:
            return True # Confident answer when should abstain

    if is_abstention:
        return False # Safe abstention is never a hallucination

    # Check for unsupported factual claims
    for claim in test_case.get("unsupported_claims", []):
        if claim in answer:
            return True

    # Check if supported claims are actually backed by the provided context
    context_str = " ".join(context)
    for claim in test_case.get("supported_claims", []):
        if claim in answer and claim not in context_str:
            return True # Claim generated but not in the available context

    return False


def calculate_metrics(dataset: list[dict], baseline_results: dict, sentinel_results: dict) -> dict:
    metrics = {
        "total_cases": len(dataset),
        "baseline": {
            "hallucinations": 0,
            "correct": 0,
            "abstentions": 0
        },
        "sentinelrag": {
            "hallucinations": 0,
            "correct": 0,
            "abstentions": 0
        },
        "self_correction": {
            "conflict_cases": 0,
            "conflicts_resolved": 0,
            "conflicts_unresolved": 0
        },
        "comparison": {}
    }

    for case in dataset:
        case_id = case["id"]
        b_res = baseline_results[case_id]
        s_res = sentinel_results[case_id]

        # Baseline Evaluation
        b_hallucinated = check_hallucination(case, b_res["behavior"], b_res.get("answer", ""), case["initial_context"])
        b_abstain = (b_res["behavior"] != "DIRECT_ANSWER") or ("couldn't find the answer" in b_res.get("answer", ""))

        if b_hallucinated:
            metrics["baseline"]["hallucinations"] += 1
        elif b_abstain:
            metrics["baseline"]["abstentions"] += 1
        else:
            metrics["baseline"]["correct"] += 1

        # SentinelRAG Evaluation
        s_context = case["corrective_context"] if s_res.get("corrected") and case["corrective_context"] else case["initial_context"]
        s_hallucinated = check_hallucination(case, s_res["behavior"], s_res.get("answer", ""), s_context, is_corrected=s_res.get("corrected", False))
        s_abstain = (s_res["behavior"] != "DIRECT_ANSWER") or ("couldn't find the answer" in s_res.get("answer", ""))

        if s_hallucinated:
            metrics["sentinelrag"]["hallucinations"] += 1
        elif s_abstain:
            metrics["sentinelrag"]["abstentions"] += 1
        else:
            metrics["sentinelrag"]["correct"] += 1

        # Conflict Resolution
        if case["category"] == "CONFLICTING_CONTEXT":
            metrics["self_correction"]["conflict_cases"] += 1
            # resolved = second eval detects no conflict (DIRECT_ANSWER) + context quality GOOD + answer supported
            if s_res.get("corrected") and not s_abstain and not s_hallucinated:
                metrics["self_correction"]["conflicts_resolved"] += 1
            else:
                metrics["self_correction"]["conflicts_unresolved"] += 1

    # Calculate Rates
    for sys in ["baseline", "sentinelrag"]:
        m = metrics[sys]
        m["hallucination_rate"] = (m["hallucinations"] / metrics["total_cases"]) * 100

    m_sc = metrics["self_correction"]
    if m_sc["conflict_cases"] > 0:
        m_sc["conflict_resolution_success_rate"] = (m_sc["conflicts_resolved"] / m_sc["conflict_cases"]) * 100
    else:
        m_sc["conflict_resolution_success_rate"] = 0.0

    metrics["comparison"]["absolute_hallucination_reduction"] = metrics["baseline"]["hallucination_rate"] - metrics["sentinelrag"]["hallucination_rate"]

    if metrics["baseline"]["hallucination_rate"] > 0:
        metrics["comparison"]["relative_hallucination_reduction"] = (metrics["comparison"]["absolute_hallucination_reduction"] / metrics["baseline"]["hallucination_rate"]) * 100
    else:
        metrics["comparison"]["relative_hallucination_reduction"] = 0.0

    return metrics
