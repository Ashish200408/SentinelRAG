from typing import List
import logging
from app.rag.retrieval.models import RetrievedChunk
from app.features.context_evaluation.models import ContextEvaluation, ContextQuality
from app.config.settings import settings
from app.features.context_evaluation.semantic import semantic_evaluator
from app.features.context_evaluation.conflict import conflict_detector

logger = logging.getLogger(__name__)

class ContextEvaluator:
    def evaluate(self, question: str, chunks: List[RetrievedChunk]) -> ContextEvaluation:
        if not chunks:
            return ContextEvaluation(
                quality=ContextQuality.INSUFFICIENT,
                best_score=0.0,
                average_score=0.0,
                retrieved_chunks=0,
                relevance_score=0.0,
                answerability_score=0.0,
                coverage_score=0.0,
                reason="No context retrieved."
            )
            
        scores = [chunk.similarity_score for chunk in chunks]
        best_score = max(scores)
        average_score = sum(scores) / len(scores)
        
        # Deterministic coverage: ratio of chunks above low threshold
        good_chunks = sum(1 for s in scores if s >= settings.LOW_CONTEXT_THRESHOLD)
        coverage_score = good_chunks / len(scores)
        
        # Detect conflict
        conflict_result = conflict_detector.detect(question, chunks)

        # 1. Deterministic Evaluation
        if best_score < settings.LOW_CONTEXT_THRESHOLD:
            quality = ContextQuality.INSUFFICIENT
            reason = "Deterministic: Best retrieval score is below the low confidence threshold."
        elif best_score >= settings.STRONG_CONTEXT_THRESHOLD:
            quality = ContextQuality.GOOD
            reason = "Deterministic: Very strong retrieval score found."
        else:
            quality = ContextQuality.UNCERTAIN
            reason = "Deterministic: Context quality is uncertain based on similarity scores."
            
        # 2. Semantic Evaluation for UNCERTAIN cases without conflict
        answerability_score = 0.0
        if quality == ContextQuality.UNCERTAIN and not conflict_result.conflict_detected:
            chunks_text = "\n\n".join([f"Document: {c.filename}\nContent: {c.chunk_text}" for c in chunks])
            logger.info("Evaluating context semantically due to uncertain deterministic score.")
            semantic_result = semantic_evaluator.evaluate(question, chunks_text)
            
            if semantic_result:
                answerability_score = semantic_result.confidence
                if semantic_result.answerable:
                    quality = ContextQuality.GOOD
                    reason = f"Semantic: {semantic_result.reason}"
                else:
                    quality = ContextQuality.INSUFFICIENT
                    reason = f"Semantic: {semantic_result.reason}"
            else:
                # Safe fallback if semantic evaluation fails
                logger.warning("Semantic evaluator failed. Falling back to safe deterministic default (INSUFFICIENT).")
                quality = ContextQuality.INSUFFICIENT
                reason = "Semantic evaluator failed, defaulting to insufficient context safely."
            
        return ContextEvaluation(
            quality=quality,
            best_score=best_score,
            average_score=average_score,
            retrieved_chunks=len(chunks),
            relevance_score=best_score,
            answerability_score=answerability_score,
            coverage_score=coverage_score,
            reason=reason,
            conflict_detected=conflict_result.conflict_detected,
            conflict_confidence=conflict_result.confidence,
            conflict_reason=conflict_result.reason,
            conflicting_chunk_indices=conflict_result.conflicting_chunk_indices
        )

context_evaluator = ContextEvaluator()
