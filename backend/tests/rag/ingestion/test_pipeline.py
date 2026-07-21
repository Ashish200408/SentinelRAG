import pytest
import os
from fastapi import HTTPException
from app.rag.chunking.deterministic import chunker
from app.rag.ingestion.cleaner import cleaner
from app.config.thresholds import thresholds

def test_chunker():
    text = "a" * 2000
    thresholds.CHUNK_SIZE = 800
    thresholds.CHUNK_OVERLAP = 150
    chunks = chunker.chunk(text)
    
    assert len(chunks) > 0
    assert len(chunks[0]) == 800
    assert len(chunks[1]) == 800

def test_cleaner():
    raw = "Hello   World\n\n\n\nTesting\r\nLine"
    cleaned = cleaner.clean(raw)
    assert cleaned == "Hello World\nTesting\nLine"
