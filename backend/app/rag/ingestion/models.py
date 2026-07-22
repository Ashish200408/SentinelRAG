from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid

class DocumentMetadata(BaseModel):
    document_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    filename: str
    file_size: int
    sha256: str
    document_type: str
    upload_timestamp: datetime = Field(default_factory=datetime.now)

class ProcessingSummary(BaseModel):
    pages_processed: int = 0
    pages_with_text: int = 0
    pages_using_ocr: int = 0
    total_characters: int = 0
    processing_time_ms: int = 0
    processing_status: str = "PENDING"

class IndexingSummary(BaseModel):
    collection_name: str = ""
    vectors_stored: int = 0
    indexing_status: str = "PENDING"
    indexing_time_ms: int = 0

class DocumentProcessingResult(BaseModel):
    metadata: DocumentMetadata
    cleaned_text: str = ""
    chunks: List[str] = Field(default_factory=list)
    preview: str = ""
    processing_summary: ProcessingSummary = Field(default_factory=ProcessingSummary)
    indexing_summary: Optional[IndexingSummary] = None
    processing_logs: List[str] = Field(default_factory=list)
