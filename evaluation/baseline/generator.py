def mock_generate_answer(prompt: str, test_case: dict) -> str:
    """
    Deterministic mock generator used identically by Baseline and SentinelRAG.
    It reads the context from the prompt and outputs claims that are present.
    If no context is provided, it hallucinates an unsupported claim to simulate LLM failure.
    """
    if "Context Documents:" in prompt:
        context_part = prompt.split("Context Documents:")[1].split("Question:")[0].strip()
    else:
        context_part = ""

    if not context_part:
        if test_case.get("unsupported_claims"):
            return test_case["unsupported_claims"][0]
        return "I confidently hallucinate an answer without evidence."

    supported = test_case.get("supported_claims", [])
    unsupported = test_case.get("unsupported_claims", [])
    import re
    def normalize_text(text: str) -> str:
        if not text: return ""
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    norm_context = normalize_text(context_part)
    output_claims = []

    for claim in supported:
        if normalize_text(claim) in norm_context:
            output_claims.append(claim)

    for claim in unsupported:
        if normalize_text(claim) in norm_context:
            output_claims.append(claim)

    if output_claims:
        return " ".join(output_claims)

    return "I couldn't find the answer in the uploaded documents."
