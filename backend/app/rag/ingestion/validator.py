import os
from app.config.settings import settings
from fastapi import HTTPException

class DocumentValidator:
    def validate(self, file_path: str, filename: str, content_type: str) -> None:
        # Validate extension
        if not filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Invalid file extension. Only PDF is allowed.")
        
        # Validate MIME type
        if content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="Invalid MIME type. Expected application/pdf.")
        
        # Validate file size
        file_size = os.path.getsize(file_path)
        if file_size == 0:
            raise HTTPException(status_code=400, detail="File is empty.")
        if file_size < settings.MIN_UPLOAD_SIZE_BYTES:
            raise HTTPException(status_code=400, detail=f"File is too small. Minimum size is {settings.MIN_UPLOAD_SIZE_BYTES} bytes.")
        if file_size > settings.MAX_UPLOAD_SIZE_BYTES:
            raise HTTPException(status_code=400, detail=f"File is too large. Maximum size is {settings.MAX_UPLOAD_SIZE_BYTES} bytes.")
        
        # Validate PDF header
        with open(file_path, 'rb') as f:
            header = f.read(5)
            if header != b'%PDF-':
                raise HTTPException(status_code=400, detail="Invalid file content. Not a valid PDF file (missing %PDF header).")

validator = DocumentValidator()
