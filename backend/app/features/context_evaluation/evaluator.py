from typing import List
from app.rag.retrieval.models import RetrievedChunk
from app.features.context_evaluation.models import ContextEvaluation, ContextQuality
from app.config.settings import settings

class ContextEvaluator:
    def evaluate(self, chunks: List[RetrievedChunk]) -> ContextEvaluation:
        if not chunks:
            return ContextEvaluation(
                quality=ContextQuality.NO_CONTEXT,
                best_score=0.0,
                average_score=0.0,
                retrieved_chunks=0
            )
            
        scores = [chunk.similarity_score for chunk in chunks]
        best_score = max(scores)
        average_score = sum(scores) / len(scores)
        
        if best_score >= settings.GOOD_CONTEXT_THRESHOLD:
            quality = ContextQuality.GOOD
        else:
            quality = ContextQuality.LOW_CONFIDENCE
            
        return ContextEvaluation(
            quality=quality,
            best_score=best_score,
            average_score=average_score,
            retrieved_chunks=len(chunks)
        )

context_evaluator = ContextEvaluator()
