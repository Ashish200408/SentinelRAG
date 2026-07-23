import io
import os
from typing import Tuple

import fitz
import pytesseract
from PIL import Image

# Configure Tesseract only on Windows
if os.name == "nt":
    pytesseract.pytesseract.tesseract_cmd = (
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )
    os.environ["TESSDATA_PREFIX"] = (
        r"C:\Program Files\Tesseract-OCR\tessdata"
    )

TESSERACT_AVAILABLE = False

try:
    pytesseract.get_tesseract_version()
    TESSERACT_AVAILABLE = True
    print("Tesseract detected.")
except Exception:
    print("Tesseract is not available on this server. OCR disabled.")


class TesseractOCRService:
    def extract(self, file_path: str) -> Tuple[str, int, int]:
        """
        Extract text from PDF using OCR.

        Returns:
            (text, page_count, pages_using_ocr)
        """

        # Skip OCR if Tesseract is unavailable
        if not TESSERACT_AVAILABLE:
            print("Skipping OCR because Tesseract is unavailable.")
            return "", 0, 0

        extracted_text: list[str] = []
        pages_using_ocr = 0
        doc = None

        try:
            doc = fitz.open(file_path)
            page_count = len(doc)

            for page in doc:
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                img = Image.open(io.BytesIO(pix.tobytes("png")))

                # Convert to grayscale
                img = img.convert("L")

                # Increase contrast
                img = img.point(lambda x: 0 if x < 150 else 255)

                # Explicitly convert to string
                text = str(
                    pytesseract.image_to_string(
                        img,
                        config="--oem 3 --psm 6",
                    )
                )

                extracted_text.append(text)

                if text.strip():
                    pages_using_ocr += 1

        except Exception as e:
            raise RuntimeError(f"OCR processing failed: {e}") from e

        finally:
            if doc is not None:
                doc.close()

        return (
            "\n".join(extracted_text),
            page_count,
            pages_using_ocr,
        )


ocr_service = TesseractOCRService()