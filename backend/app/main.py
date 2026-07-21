from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="SentinelRAG",
    description="SentinelRAG API",
    version="0.1.0",
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
