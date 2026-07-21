class Thresholds:
    # Native extraction is considered successful when extracted text >= this value
    MIN_NATIVE_TEXT_LENGTH: int = 100

    # Chunking
    CHUNK_SIZE: int = 800
    CHUNK_OVERLAP: int = 150

thresholds = Thresholds()
