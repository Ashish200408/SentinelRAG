import fitz
from typing import Tuple

class NativeExtractor:
    def extract(self, file_path: str) -> Tuple[str, int, int]:
        """
        Extracts native text from a PDF.
        Returns a tuple of:
        - extracted_text (str)
        - page_count (int)
        - pages_with_text (int)
        """
        extracted_text = []
        pages_with_text = 0
        
        try:
            doc = fitz.open(file_path)
            page_count = len(doc)
            for page in doc:
                text = page.get_text()
                extracted_text.append(text)
                if len(text.strip()) > 0:
                    pages_with_text += 1
            doc.close()
        except Exception as e:
            raise RuntimeError(f"Failed to parse PDF: {str(e)}")
            
        return "\n".join(extracted_text), page_count, pages_with_text

extractor = NativeExtractor()
