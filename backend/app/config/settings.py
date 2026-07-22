from pathlib import Path
import tempfile

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Application settings
    APP_NAME: str = "SentinelRAG Backend"

    # Ingestion pipeline settings
    MAX_UPLOAD_SIZE_BYTES: int = 10 * 1024 * 1024
    MIN_UPLOAD_SIZE_BYTES: int = 100
    TEMP_UPLOAD_DIR: str = str(Path(tempfile.gettempdir()) / "sentinelrag" / "uploads")

    # Qdrant
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_API_KEY: str | None = None
    QDRANT_COLLECTION: str = "sentinelrag_docs"

    # Embeddings
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    EMBEDDING_DIMENSIONS: int = 384

    # Gemini
    GEMINI_API_KEY: str | None = None
    GEMINI_MODEL: str = "gemini-3.5-flash-lite"

    # Retrieval
    RETRIEVAL_TOP_K: int = 3
    RETRIEVAL_SCORE_THRESHOLD: float = 0.3
    GOOD_CONTEXT_THRESHOLD: float = 0.45
    LOW_CONTEXT_THRESHOLD: float = 0.25
    MAX_REWRITE_ATTEMPTS: int = 1

    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).resolve().parent.parent.parent.parent / ".env.backend"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
print(f"Gemini API Key Loaded: {bool(settings.GEMINI_API_KEY)}")