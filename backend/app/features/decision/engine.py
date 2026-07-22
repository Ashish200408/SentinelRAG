from app.features.context_evaluation.models import ContextEvaluation, ContextQuality
from app.config.settings import settings

class DecisionEngine:
    def decide(self, evaluation: ContextEvaluation, attempt: int) -> str:
        if evaluation.quality == ContextQuality.GOOD:
            return "DIRECT_ANSWER"
            
        if evaluation.quality == ContextQuality.LOW_CONFIDENCE:
            if attempt <= settings.MAX_REWRITE_ATTEMPTS:
                return "REWRITE_QUERY"
            return "ASK_FOR_CLARIFICATION"
            
        # NO_CONTEXT
        return "ASK_FOR_CLARIFICATION"

decision_engine = DecisionEngine()
