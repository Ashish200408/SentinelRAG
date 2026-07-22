import time
import logging
from app.rag.retrieval.service import retrieval_service
from app.providers.gemini.provider import gemini_provider
from app.schemas.chat import ChatQueryResponse, DecisionMetadata
from app.rag.retrieval.models import RetrievedChunk
from app.features.context_evaluation.evaluator import context_evaluator
from app.features.decision.engine import decision_engine
from app.features.query_rewrite.service import query_rewrite_service
from app.config.settings import settings

logger = logging.getLogger(__name__)

class RAGService:
    def answer_query(self, question: str) -> ChatQueryResponse:
        start_time = time.time()
        
        current_query = question
        attempt = 0
        rewritten = False
        rewritten_query = None
        
        logger.info("Question received")
        
        while attempt <= settings.MAX_REWRITE_ATTEMPTS:
            attempt += 1
            
            if attempt == 2:
                logger.info("Second retrieval completed")
            else:
                logger.info("Retrieval completed")
                
            chunks = retrieval_service.retrieve(current_query)
            logger.info(f"Retrieved {len(chunks)} chunks")
            
            evaluation = context_evaluator.evaluate(chunks)
            logger.info(f"Context evaluated")
            logger.info(f"Best similarity = {evaluation.best_score}")
            logger.info(f"Average similarity = {evaluation.average_score}")
            
            decision = decision_engine.decide(evaluation, attempt)
            logger.info(f"Decision = {decision}")
            
            if decision == "DIRECT_ANSWER":
                break
                
            if decision == "REWRITE_QUERY":
                current_query = query_rewrite_service.rewrite(question)
                rewritten = True
                rewritten_query = current_query
                logger.info("Query rewritten")
                continue
                
            if decision == "ASK_FOR_CLARIFICATION":
                break
                
        # After loop
        answer = None
        clarification = None
        
        if decision == "DIRECT_ANSWER":
            logger.info("RAGService: Generating answer with Gemini")
            context_text = "\n\n".join([f"Document: {c.filename}\nContent: {c.chunk_text}" for c in chunks])
            prompt = f"""You are an assistant answering questions based strictly on the provided context documents.
Do not use any outside knowledge. If the context does not contain the answer, reply exactly with: "I couldn't find the answer in the uploaded documents."

Context Documents:
{context_text}

Question:
{question}
"""
            answer = gemini_provider.generate_answer(prompt)
        else: # ASK_FOR_CLARIFICATION
            clarification = "I couldn't find enough information in the uploaded documents. Could you clarify your question or upload a document containing this topic?"

        generation_time_ms = int((time.time() - start_time) * 1000)
        
        decision_meta = DecisionMetadata(
            path=decision,
            retrieval_quality=evaluation.quality.value,
            rewritten=rewritten,
            rewritten_query=rewritten_query,
            retrieval_attempts=attempt,
            best_similarity=evaluation.best_score,
            average_similarity=evaluation.average_score,
            retrieved_chunks=len(chunks),
            confidence=evaluation.best_score
        )
        
        return ChatQueryResponse(
            answer=answer,
            clarification=clarification,
            sources=[c.model_dump(exclude={"chunk_text"}) for c in chunks],
            chunk_count=len(chunks),
            generation_time_ms=generation_time_ms,
            decision=decision_meta
        )

rag_service = RAGService()
