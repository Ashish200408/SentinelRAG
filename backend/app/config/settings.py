import tempfile
from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Application settings
    APP_NAME: str = "SentinelRAG Backend"
    
    # Ingestion pipeline settings
    MAX_UPLOAD_SIZE_BYTES: int = 10 * 1024 * 1024  # 10MB default
    MIN_UPLOAD_SIZE_BYTES: int = 100  # 100 bytes min
    TEMP_UPLOAD_DIR: str = str(Path(tempfile.gettempdir()) / "sentinelrag" / "uploads")

    class Config:
        env_file = ".env.backend"

settings = Settings()
