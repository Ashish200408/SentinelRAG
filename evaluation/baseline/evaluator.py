from evaluation.baseline.generator import mock_generate_answer

class BaselineEvaluator:
    def evaluate(self, test_case: dict) -> dict:
        """
        Simulates naive RAG without ContextEvaluator, ConflictDetector, or SelfCorrection.
        """
        context_chunks = test_case["initial_context"]
        context_text = "\n\n".join([f"Document: mock_doc.txt\nContent: {c}" for c in context_chunks])

        prompt = f"""You are an assistant answering questions based strictly on the provided context documents.
Do not use any outside knowledge. If the context does not contain the answer, reply exactly with: "I couldn't find the answer in the uploaded documents."

Context Documents:
{context_text}

Question:
{test_case['question']}
"""
        answer = mock_generate_answer(prompt, test_case)

        return {
            "behavior": "DIRECT_ANSWER",
            "answer": answer
        }

baseline_evaluator = BaselineEvaluator()
