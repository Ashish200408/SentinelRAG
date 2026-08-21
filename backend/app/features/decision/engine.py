from app.features.context_evaluation.models import ContextEvaluation, ContextQuality
from app.config.settings import settings
import logging

logger = logging.getLogger(__name__)

class DecisionEngine:
    def decide(self, evaluation: ContextEvaluation, attempt: int, correction_attempts: int = 0) -> str:
        if evaluation.conflict_detected:
            if correction_attempts == 0:
                return "SELF_CORRECT"
            return "ASK_FOR_CLARIFICATION"
            
        if evaluation.quality == ContextQuality.GOOD:
            return "DIRECT_ANSWER"
            
        if evaluation.quality in (ContextQuality.INSUFFICIENT, ContextQuality.UNCERTAIN):
            if evaluation.quality == ContextQuality.UNCERTAIN:
                logger.warning("Uncertain quality reached DecisionEngine, handling safely as INSUFFICIENT.")
            if attempt <= settings.MAX_REWRITE_ATTEMPTS:
                return "REWRITE_QUERY"
            return "ASK_FOR_CLARIFICATION"
            
        return "ASK_FOR_CLARIFICATION"

decision_engine = DecisionEngine()
