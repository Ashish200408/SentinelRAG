import os
import io
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

# Check whether Tesseract is available
try:
    print("Using Tesseract:", pytesseract.pytesseract.tesseract_cmd)
    print("Detected Version:", pytesseract.get_tesseract_version())
    TESSERACT_AVAILABLE = True
except Exception:
    print("Tesseract not found. OCR functionality will be unavailable.")
    TESSERACT_AVAILABLE = False


class TesseractOCRService:
    def extract(self, file_path: str) -> Tuple[str, int, int]:
        """
        Extract text from PDF using OCR.

        Returns:
            (text, page_count, pages_using_ocr)
        """

        if not TESSERACT_AVAILABLE:
            raise RuntimeError(
                "Tesseract OCR is not installed on this server."
            )

        extracted_text = []
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

                text = pytesseract.image_to_string(
                    img,
                    config="--oem 3 --psm 6",
                )

                extracted_text.append(text)

                if text.strip():
                    pages_using_ocr += 1

        except Exception as e:
            raise RuntimeError(f"OCR processing failed: {e}")

        finally:
            if doc is not None:
                doc.close()

        return (
            "\n".join(extracted_text),
            page_count,
            pages_using_ocr,
        )


ocr_service = TesseractOCRService()