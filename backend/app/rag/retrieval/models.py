from pydantic import BaseModel
from typing import Optional

class RetrievedChunk(BaseModel):
    document_id: str
    filename: str
    chunk_index: int
    chunk_text: str
    similarity_score: float
    page_number: Optional[int] = None
