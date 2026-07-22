from pydantic import BaseModel
from enum import Enum

class ContextQuality(str, Enum):
    GOOD = "GOOD"
    LOW_CONFIDENCE = "LOW_CONFIDENCE"
    NO_CONTEXT = "NO_CONTEXT"

class ContextEvaluation(BaseModel):
    quality: ContextQuality
    best_score: float
    average_score: float
    retrieved_chunks: int
