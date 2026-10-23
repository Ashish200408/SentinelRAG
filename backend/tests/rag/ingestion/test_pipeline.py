import pytest
import os
from fastapi import HTTPException
from app.rag.chunking.deterministic import chunker
from app.rag.ingestion.cleaner import cleaner
from app.config.thresholds import thresholds

def test_chunker():
    pages = [{"page_number": 1, "text": "a" * 2000}]
    thresholds.CHUNK_SIZE = 800
    thresholds.CHUNK_OVERLAP = 150
    chunks = chunker.chunk(pages)
    
    assert len(chunks) > 0
    assert len(chunks[0]["text"]) == 800
    assert len(chunks[1]["text"]) == 800

def test_cleaner():
    pages = [{"page_number": 1, "text": "Hello   World\n\n\n\nTesting\r\nLine"}]
    cleaned = cleaner.clean(pages)
    assert cleaned[0]["text"] == "Hello World\nTesting\nLine"
