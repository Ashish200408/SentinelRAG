import logging
from typing import List
from app.config.settings import settings
from app.rag.embedding.service import embedding_service
from app.providers.qdrant.provider import qdrant_provider
from app.rag.retrieval.models import RetrievedChunk

logger = logging.getLogger(__name__)

class RetrievalService:
    def retrieve(self, query: str) -> List[RetrievedChunk]:
        """
        Generates query embedding and retrieves top K chunks from Qdrant,
        filtering out chunks below the similarity threshold.
        """
        if not query.strip():
            logger.warning("Empty query received for retrieval")
            return []

        logger.info(f"Generating embedding for query: '{query}'")
        # Generate embedding for a single query text (wrapped in list)
        embeddings = embedding_service.generate_embeddings([query])
        if not embeddings:
            return []
            
        query_vector = embeddings[0]

        logger.info(f"Querying Qdrant collection: {qdrant_provider.collection_name} for top {settings.RETRIEVAL_TOP_K} results")
        
        try:
            raw_response = qdrant_provider.client.query_points(
                collection_name=qdrant_provider.collection_name,
                query=query_vector,
                limit=settings.RETRIEVAL_TOP_K,
                score_threshold=settings.RETRIEVAL_SCORE_THRESHOLD
            )
            search_result = raw_response.points
        except Exception as e:
            logger.error(f"Failed to query Qdrant: {e}")
            raise Exception(f"Qdrant Search Failed: {e}")

        retrieved_chunks = []
        for point in search_result:
            payload = point.payload or {}
            
            chunk = RetrievedChunk(
                document_id=payload.get("document_id", "unknown"),
                filename=payload.get("filename", "unknown"),
                chunk_index=payload.get("chunk_index", 0),
                chunk_text=payload.get("chunk_text", ""),
                similarity_score=point.score,
                page_number=payload.get("page_number")
            )
            retrieved_chunks.append(chunk)

        logger.info(f"Retrieved {len(retrieved_chunks)} chunks above score threshold {settings.RETRIEVAL_SCORE_THRESHOLD}")
        return retrieved_chunks

retrieval_service = RetrievalService()
