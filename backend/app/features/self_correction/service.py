from app.features.context_evaluation.models import ConflictResult
from app.features.self_correction.planner import self_correction_planner

class SelfCorrectionService:
    def correct(self, original_query: str, conflict_result: ConflictResult) -> str:
        """
        Orchestrates the generation of a corrective query when a conflict is detected.
        """
        return self_correction_planner.plan(original_query, conflict_result.reason)

self_correction_service = SelfCorrectionService()
