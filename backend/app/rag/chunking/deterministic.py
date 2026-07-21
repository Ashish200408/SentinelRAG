from typing import List
from app.config.thresholds import thresholds

class DeterministicChunker:
    def chunk(self, text: str) -> List[str]:
        if not text:
            return []
            
        chunk_size = thresholds.CHUNK_SIZE
        chunk_overlap = thresholds.CHUNK_OVERLAP
        
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = min(start + chunk_size, text_length)
            
            # If we are not at the end of the text, try to find a nice boundary (e.g., newline or space)
            # We'll stick to strict deterministic character counts for now as requested.
            # "No semantic chunking." - user
            chunk = text[start:end]
            chunks.append(chunk)
            
            if end == text_length:
                break
                
            start += (chunk_size - chunk_overlap)
            
        return chunks

chunker = DeterministicChunker()
