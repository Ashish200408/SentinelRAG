from pydantic import BaseModel, Field
from typing import List, Optional


class SourceMetadata(BaseModel):
    document_id: str
    filename: str
    chunk_index: int
    similarity_score: float
    page_numbers: Optional[list[int]] = None

class DecisionMetadata(BaseModel):
    path: str
    retrieval_quality: str
    rewritten: bool
    original_query: str
    current_query: str
    rewritten_query: Optional[str] = None
    retrieval_attempts: int
    best_similarity: float
    average_similarity: float
    retrieved_chunks: int
    confidence: float
    
    # Phase 2 metrics
    relevance_score: float = 0.0
    answerability_score: float = 0.0
    coverage_score: float = 0.0
    reason: str = ""
    
    # Phase 3 metrics
    conflict_detected: bool = False
    conflict_reason: str = ""


class ChatQueryRequest(BaseModel):
    question: str = Field(..., description="The user's question to be answered from the documents")

class ChatQueryResponse(BaseModel):
    answer: Optional[str] = None
    clarification: Optional[str] = None
    sources: List[SourceMetadata]
    chunk_count: int
    generation_time_ms: int
    decision: DecisionMetadata
