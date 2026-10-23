import re
from app.features.context_evaluation.models import ContextEvaluation

class SelfCorrectionPlanner:
    def plan(self, original_query: str, evaluation: ContextEvaluation) -> str:
        """
        Deterministically generate a corrective query without calling an LLM.
        Avoids including conflicting facts directly to prevent hallucination bias.
        """
        clean_query = original_query.replace("?", "").strip()

        s1, s2 = evaluation.conflicting_sentences
        if not s1 or not s2:
            return f"{clean_query} exact correct value"

        def get_tokens(s: str) -> list[str]:
            s = s.lower()
            # Remove punctuation
            s = re.sub(r'[^\w\s]', '', s)
            # Remove numeric values with optional units
            s = re.sub(r'\b\d+(?:\.\d+)?([a-zA-Z]+)?\b', '', s)
            tokens = s.split()
            stop_words = {"the", "is", "at", "of", "a", "an", "and", "to", "not", "in", "on", "for", "with", "are", "was", "were"}
            return [t for t in tokens if t not in stop_words]

        t1 = get_tokens(s1)
        t2 = get_tokens(s2)

        # Intersection preserving relative order of the first sentence
        intersection = []
        seen = set()
        for t in t1:
            if t in t2 and t not in seen:
                intersection.append(t)
                seen.add(t)

        if not intersection:
            return f"{clean_query} exact correct value"

        intersect_str = " ".join(intersection)

        return f"{clean_query} {intersect_str}"

self_correction_planner = SelfCorrectionPlanner()
