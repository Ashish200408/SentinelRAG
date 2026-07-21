import fitz
import pytesseract
from PIL import Image
import io
from typing import Tuple

class TesseractOCRService:
    def extract(self, file_path: str) -> Tuple[str, int, int]:
        """
        Extracts text from a PDF using OCR (Tesseract).
        Returns a tuple of:
        - extracted_text (str)
        - page_count (int)
        - pages_using_ocr (int)
        """
        extracted_text = []
        pages_using_ocr = 0
        
        try:
            doc = fitz.open(file_path)
            page_count = len(doc)
            
            for page in doc:
                # Render page to image
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2x zoom for better OCR
                img = Image.open(io.BytesIO(pix.tobytes("png")))
                
                # Perform OCR
                text = pytesseract.image_to_string(img)
                extracted_text.append(text)
                if len(text.strip()) > 0:
                    pages_using_ocr += 1
            
            doc.close()
        except Exception as e:
            raise RuntimeError(f"OCR processing failed: {str(e)}")
            
        return "\n".join(extracted_text), page_count, pages_using_ocr

ocr_service = TesseractOCRService()
