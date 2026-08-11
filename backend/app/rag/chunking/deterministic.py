from typing import List
from app.config.thresholds import thresholds

class DeterministicChunker:
    def chunk(self, pages: list[dict]) -> list[dict]:
        if not pages:
            return []
            
        full_text = ""
        char_to_page = []
        for page in pages:
            page_num = page["page_number"]
            # Add a newline between pages if we concatenate
            page_text = page["text"] + "\n"
            full_text += page_text
            char_to_page.extend([page_num] * len(page_text))
            
        full_text = full_text.strip()
        if not full_text:
            return []
            
        chunk_size = thresholds.CHUNK_SIZE
        chunk_overlap = thresholds.CHUNK_OVERLAP
        
        chunks = []
        start = 0
        text_length = len(full_text)
        
        while start < text_length:
            end = min(start + chunk_size, text_length)
            
            chunk_text = full_text[start:end]
            
            span_pages = char_to_page[start:end]
            unique_pages = []
            for p in span_pages:
                if p not in unique_pages:
                    unique_pages.append(p)
            
            chunks.append({
                "text": chunk_text,
                "page_numbers": unique_pages
            })
            
            if end == text_length:
                break
                
            start += (chunk_size - chunk_overlap)
            
        return chunks

chunker = DeterministicChunker()
