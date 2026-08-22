import json
import os
import datetime
from unittest.mock import patch
from evaluation.baseline.evaluator import baseline_evaluator
from app.rag.pipeline.rag_service import rag_service
from app.rag.retrieval.models import RetrievedChunk
from evaluation.metrics.hallucination import calculate_metrics
from evaluation.baseline.generator import mock_generate_answer

def run_benchmark():
    with open('evaluation/datasets/self_correction_benchmark.json', 'r') as f:
        dataset = json.load(f)

    baseline_results = {}
    sentinel_results = {}

    # Run Baseline
    for case in dataset:
        baseline_results[case["id"]] = baseline_evaluator.evaluate(case)

    # Run SentinelRAG (Offline Mocking)
    def create_mock_retrieve(case):
        chunks1 = [RetrievedChunk(chunk_id=f"1_{i}", document_id="doc1", filename="mock", chunk_index=0, similarity_score=0.9, chunk_text=c) for i, c in enumerate(case["initial_context"])]
        chunks2 = [RetrievedChunk(chunk_id=f"2_{i}", document_id="doc1", filename="mock", chunk_index=0, similarity_score=0.9, chunk_text=c) for i, c in enumerate(case.get("corrective_context", []))]

        call_count = [0]
        def mock_retrieve(query):
            call_count[0] += 1
            if call_count[0] == 1:
                return chunks1
            if chunks2:
                return chunks2
            return chunks1

        return mock_retrieve

    for case in dataset:
        mock_retrieve_func = create_mock_retrieve(case)

        # Patch retrieval and generation boundaries
        with patch('app.rag.pipeline.rag_service.retrieval_service.retrieve', side_effect=mock_retrieve_func):
            with patch('app.rag.pipeline.rag_service.gemini_provider.generate_answer', side_effect=lambda p: mock_generate_answer(p, case)):
                response = rag_service.answer_query(case["question"])
                sentinel_results[case["id"]] = {
                    "behavior": response.decision.path,
                    "answer": response.answer if response.answer else response.clarification,
                    "corrected": response.decision.correction_attempts > 0
                }

    # Calculate Metrics
    metrics = calculate_metrics(dataset, baseline_results, sentinel_results)

    # Save Results
    os.makedirs('evaluation/results', exist_ok=True)
    result_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "metrics": metrics,
        "per_case_results": []
    }

    for case in dataset:
        cid = case["id"]
        result_data["per_case_results"].append({
            "id": cid,
            "category": case["category"],
            "baseline": baseline_results[cid],
            "sentinelrag": sentinel_results[cid]
        })

    with open('evaluation/results/self_correction_benchmark.json', 'w') as f:
        json.dump(result_data, f, indent=2)

    # Print Report
    print("========================================")
    print("SentinelRAG Hallucination Benchmark")
    print("========================================")
    print("NOTE: Controlled offline benchmark")
    print("========================================")
    print(f"Total cases: {metrics['total_cases']}\n")
    print("BASELINE\n--------")
    print(f"Hallucinations: {metrics['baseline']['hallucinations']}")
    print(f"Correct: {metrics['baseline']['correct']}")
    print(f"Safe abstentions: {metrics['baseline']['abstentions']}")
    print(f"Hallucination rate: {metrics['baseline']['hallucination_rate']:.1f}%\n")
    print("SENTINELRAG\n-----------")
    print(f"Hallucinations: {metrics['sentinelrag']['hallucinations']}")
    print(f"Correct: {metrics['sentinelrag']['correct']}")
    print(f"Safe abstentions: {metrics['sentinelrag']['abstentions']}")
    print(f"Hallucination rate: {metrics['sentinelrag']['hallucination_rate']:.1f}%\n")
    print("IMPROVEMENT\n-----------")
    print(f"Absolute reduction: {metrics['comparison']['absolute_hallucination_reduction']:.1f} percentage points")
    print(f"Relative reduction: {metrics['comparison']['relative_hallucination_reduction']:.1f}%\n")
    print("CONFLICT CASES\n--------------")
    print(f"Total: {metrics['self_correction']['conflict_cases']}")
    print(f"Resolved: {metrics['self_correction']['conflicts_resolved']}")
    print(f"Safely rejected: {metrics['self_correction']['conflicts_unresolved']}")
    print("========================================")

if __name__ == "__main__":
    run_benchmark()
