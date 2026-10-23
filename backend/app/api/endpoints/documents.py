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

    # Generate temporary file path safely
    safe_filename = os.path.basename(file.filename) if file.filename else "unknown.pdf"
    temp_filename = f"{uuid.uuid4()}_{safe_filename}"
    temp_path = os.path.join(settings.TEMP_UPLOAD_DIR, temp_filename)

    try:
        # Save uploaded file and enforce size limits
        bytes_read = 0
        with open(temp_path, "wb") as buffer:
            while chunk := await file.read(8192):
                bytes_read += len(chunk)
                if bytes_read > settings.MAX_UPLOAD_SIZE_BYTES:
                    raise HTTPException(status_code=400, detail=f"File exceeds maximum allowed size of {settings.MAX_UPLOAD_SIZE_BYTES} bytes.")
                buffer.write(chunk)

        if bytes_read == 0:
            raise HTTPException(status_code=400, detail="Cannot process an empty file.")

        # Process the document
        result = processor.process(
            file_path=temp_path,
            filename=safe_filename,
            content_type=file.content_type or "application/pdf"
        )

        # Map internal result to external API response
        return document_mapper.map_to_response(result)

    except HTTPException:
        raise
    except Exception as e:
        import logging
        logging.getLogger(__name__).exception("Failed to process document upload")
        raise HTTPException(status_code=500, detail="An internal server error occurred while processing the document.")

    finally:
        # Cleanup temporary file regardless of success or failure
        if os.path.exists(temp_path):
            os.remove(temp_path)
