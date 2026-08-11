from fastapi import APIRouter, HTTPException
from app.schemas.chat import ChatQueryRequest, ChatQueryResponse
from app.rag.pipeline.rag_service import rag_service

router = APIRouter()

@router.post("/query", response_model=ChatQueryResponse)
def query_documents(request: ChatQueryRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
        
    try:
        return rag_service.answer_query(request.question)
    except Exception as e:
        import logging
        logging.getLogger(__name__).exception("Failed to process chat query")
        raise HTTPException(status_code=500, detail="An internal server error occurred while processing the chat query.")
