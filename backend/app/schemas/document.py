from pydantic import BaseModel
from typing import Optional, Any
from app.rag.ingestion.models import ProcessingSummary, IndexingSummary

class DocumentResponseData(BaseModel):
    document_id: str
    filename: str
    file_size: int
    sha256: str
    document_type: str
    upload_timestamp: str
    chunk_count: int
    preview: str
    processing_summary: ProcessingSummary
    indexing_summary: Optional[IndexingSummary] = None

class DocumentResponse(BaseModel):
    status: str = "success"
    data: DocumentResponseData
