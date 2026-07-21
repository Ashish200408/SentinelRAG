import os
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.config.settings import settings
from app.rag.ingestion.processor import processor
from app.api.mappers.document_mapper import document_mapper
from app.schemas.document import DocumentResponse

router = APIRouter()

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(file: UploadFile = File(...)):
    # Ensure temp directory exists
    os.makedirs(settings.TEMP_UPLOAD_DIR, exist_ok=True)
    
    # Generate temporary file path
    temp_filename = f"{uuid.uuid4()}_{file.filename}"
    temp_path = os.path.join(settings.TEMP_UPLOAD_DIR, temp_filename)
    
    try:
        # Save uploaded file
        with open(temp_path, "wb") as buffer:
            while chunk := await file.read(8192):
                buffer.write(chunk)
                
        # Process the document
        result = processor.process(
            file_path=temp_path,
            filename=file.filename or "unknown.pdf",
            content_type=file.content_type or "application/pdf"
        )
        
        # Map internal result to external API response
        return document_mapper.map_to_response(result)
        
    finally:
        # Cleanup temporary file regardless of success or failure
        if os.path.exists(temp_path):
            os.remove(temp_path)
