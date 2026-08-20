from pydantic import BaseModel
from enum import Enum

class ContextQuality(str, Enum):
    GOOD = "GOOD"
    INSUFFICIENT = "INSUFFICIENT"
    UNCERTAIN = "UNCERTAIN"

class ContextEvaluation(BaseModel):
    quality: ContextQuality
    best_score: float
    average_score: float
    retrieved_chunks: int
    
    # Phase 2 evaluation metrics
    relevance_score: float = 0.0
    answerability_score: float = 0.0
    coverage_score: float = 0.0
    reason: str = ""
