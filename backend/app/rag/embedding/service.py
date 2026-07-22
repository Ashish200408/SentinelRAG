from typing import List
from sentence_transformers import SentenceTransformer
from app.config.settings import settings
import logging

logger = logging.getLogger(__name__)

class EmbeddingService:
    def __init__(self):
        self._model = None

    @property
    def model(self):
        if self._model is None:
            logger.info(f"Loading embedding model: {settings.EMBEDDING_MODEL}")
            self._model = SentenceTransformer(settings.EMBEDDING_MODEL)
        return self._model

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        if not texts:
            return []
        try:
            logger.info(f"Embedding generation started for {len(texts)} texts")
            embeddings = self.model.encode(texts, convert_to_numpy=True)
            logger.info("Embedding generation completed")
            return embeddings.tolist()
        except Exception as e:
            logger.error(f"Failed during embedding generation: {e}")
            raise Exception(f"Embedding Generation Failed: {e}")

embedding_service = EmbeddingService()
