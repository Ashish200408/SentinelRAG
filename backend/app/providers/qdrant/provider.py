from qdrant_client import QdrantClient
from qdrant_client.http import models as qdrant_models
from app.config.settings import settings
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class QdrantProvider:
    def __init__(self):
        self.client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY
        )
        self.collection_name = settings.QDRANT_COLLECTION
        self._ensure_collection_exists()

    def _ensure_collection_exists(self):
        try:
            collections = self.client.get_collections().collections
            exists = any(c.name == self.collection_name for c in collections)
            
            if not exists:
                logger.info(f"Creating Qdrant collection: {self.collection_name}")
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=qdrant_models.VectorParams(
                        size=settings.EMBEDDING_DIMENSIONS,
                        distance=qdrant_models.Distance.COSINE
                    )
                )
        except Exception as e:
            logger.error(f"Failed to ensure Qdrant collection exists: {e}")
            raise

    def store_vectors(self, embeddings: List[List[float]], payloads: List[Dict[str, Any]]):
        if not embeddings or not payloads:
            return
            
        if len(embeddings) != len(payloads):
            raise ValueError("Number of embeddings and payloads must match")

        logger.info(f"Vector insertion started for {len(embeddings)} vectors into {self.collection_name}")
        points = []
        for i, (embedding, payload) in enumerate(zip(embeddings, payloads)):
            # Using UUID from payload or generating one is required by Qdrant
            # We'll generate a random UUID for the point ID since chunk ID is not strictly defined
            import uuid
            point_id = str(uuid.uuid4())
            points.append(
                qdrant_models.PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload=payload
                )
            )

        try:
            response = self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            logger.info(f"Qdrant response: {response}")
        except Exception as e:
            logger.error(f"Failed during vector insertion: {e}")
            raise Exception(f"Qdrant Vector Insertion Failed: {e}")

qdrant_provider = QdrantProvider()
