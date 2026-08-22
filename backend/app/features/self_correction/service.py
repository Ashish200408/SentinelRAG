from app.features.context_evaluation.models import ContextEvaluation
from app.features.self_correction.planner import self_correction_planner

class SelfCorrectionService:
    def correct(self, original_query: str, evaluation: ContextEvaluation, current_attempts: int = 0) -> str:
        """
        Orchestrates the generation of a corrective query when a conflict is detected.
        """
        if current_attempts > 1:
            raise RuntimeError("Maximum self-correction attempts exceeded. This indicates a pipeline violation.")
        return self_correction_planner.plan(original_query, evaluation)

self_correction_service = SelfCorrectionService()
