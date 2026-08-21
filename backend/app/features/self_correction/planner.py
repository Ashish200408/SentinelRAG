import re

class SelfCorrectionPlanner:
    def plan(self, original_query: str, conflict_reason: str) -> str:
        """
        Deterministically generate a corrective query without calling an LLM.
        Avoids including conflicting facts directly to prevent hallucination bias.
        """
        # Clean the original query
        clean_query = original_query.replace("?", "").strip()
        
        # Append targeted retrieval keywords
        corrective_query = f"{clean_query} exact correct value"
        
        return corrective_query

self_correction_planner = SelfCorrectionPlanner()
