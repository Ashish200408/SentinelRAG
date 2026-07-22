from typing import List
import logging

from sentence_transformers import SentenceTransformer
from app.config.settings import settings

logger = logging.getLogger(__name__)


class EmbeddingService:
    def __init__(self):
        self._model = None

    def _load_model(self):
        if self._model is None:
            logger.info(f"Loading embedding model: {settings.EMBEDDING_MODEL}")
            self._model = SentenceTransformer(
                settings.EMBEDDING_MODEL,
                device="cpu"
            )
            logger.info("Embedding model loaded successfully.")
        return self._model

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        if not texts:
            return []

        try:
            model = self._load_model()

            logger.info(f"Generating embeddings for {len(texts)} text(s)...")

            embeddings = model.encode(
                texts,
                convert_to_numpy=True,
                show_progress_bar=False
            )

            logger.info("Embedding generation completed.")

            return embeddings.tolist()

        except Exception as e:
            logger.exception("Embedding generation failed")
            raise RuntimeError(f"Embedding Generation Failed: {e}")


embedding_service = EmbeddingService()