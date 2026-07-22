from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.config.settings import settings
    from app.providers.qdrant.provider import qdrant_provider
    
    if not settings.GEMINI_API_KEY:
        logger.warning("GEMINI_API_KEY is not set. Gemini integration will fail.")
    else:
        try:
            from google import genai
            client = genai.Client(api_key=settings.GEMINI_API_KEY)
            models = [m.name for m in client.models.list() if "flash" in m.name or "pro" in m.name]
            logger.info(f"Available Gemini Models: {models[:5]}")
        except Exception as e:
            logger.error(f"Failed to list Gemini models: {e}")
        
    try:
        qdrant_provider.client.get_collections()
        logger.info("Qdrant connectivity verified.")
    except Exception as e:
        logger.error(f"Qdrant connectivity failed: {e}")
        
    yield

app = FastAPI(
    title="SentinelRAG",
    description="SentinelRAG API",
    version="0.1.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.api.routers import api_router
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def health_check():
    return {"status": "healthy"}
