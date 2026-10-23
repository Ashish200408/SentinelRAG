import fitz
from typing import Tuple

class NativeExtractor:
    def extract(self, file_path: str) -> Tuple[list[dict], int, int]:
        """
        Extracts native text from a PDF.
        Returns a tuple of:
        - extracted_pages (List[dict])
        - page_count (int)
        - pages_with_text (int)
        """
        extracted_pages = []
        pages_with_text = 0
        
        try:
            doc = fitz.open(file_path)
            page_count = len(doc)
            for page_num, page in enumerate(doc, start=1):
                text = page.get_text()
                extracted_pages.append({"page_number": page_num, "text": text})
                if len(text.strip()) > 0:
                    pages_with_text += 1
            doc.close()
        except Exception as e:
            raise RuntimeError(f"Failed to parse PDF: {str(e)}")
            
        return extracted_pages, page_count, pages_with_text

extractor = NativeExtractor()
