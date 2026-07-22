import os
import hashlib
import time
from datetime import datetime
from typing import List

from app.rag.ingestion.models import DocumentProcessingResult, ProcessingSummary, IndexingSummary
from app.rag.ingestion.validator import validator
from app.rag.ingestion.extractor import extractor
from app.rag.ocr.tesseract_service import ocr_service
from app.rag.ingestion.cleaner import cleaner
from app.rag.ingestion.metadata import metadata_generator
from app.rag.chunking.deterministic import chunker
from app.rag.embedding.service import embedding_service
from app.providers.qdrant.provider import qdrant_provider
from app.config.thresholds import thresholds
from fastapi import HTTPException

class DocumentProcessor:
    def _generate_sha256(self, file_path: str) -> str:
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def process(self, file_path: str, filename: str, content_type: str) -> DocumentProcessingResult:
        logs: List[str] = []
        start_time = time.time()
        
        def log(msg: str):
            timestamp = datetime.now().isoformat()
            logs.append(f"[{timestamp}] {msg}")

        log("Upload Received")

        try:
            # 2. SHA256 Generation
            sha256 = self._generate_sha256(file_path)
            log("SHA Generated")

            # 3. Validation
            validator.validate(file_path, filename, content_type)
            log("Validation Passed")
            
            file_size = os.path.getsize(file_path)

            # 4. Native Extraction
            raw_text, page_count, pages_with_text = extractor.extract(file_path)
            log("PDF Parsed")
            
            pages_using_ocr = 0

            # 5. OCR Trigger Check
            if len(raw_text.strip()) < thresholds.MIN_NATIVE_TEXT_LENGTH:
                log("OCR Triggered")
                raw_text, page_count, pages_using_ocr = ocr_service.extract(file_path)
                pages_with_text = pages_using_ocr
            else:
                log("OCR Skipped")

            # 6. Cleaning
            cleaned_text = cleaner.clean(raw_text)
            log("Cleaning Completed")

            # 7. Metadata Generation
            metadata = metadata_generator.generate(
                filename=filename,
                file_size=file_size,
                sha256=sha256,
                document_type=content_type
            )
            log("Metadata Generated")

            # 8. Chunking
            chunks = chunker.chunk(cleaned_text)
            log("Chunk Generation Completed")

            # Summary
            processing_time_ms = int((time.time() - start_time) * 1000)
            
            summary = ProcessingSummary(
                pages_processed=page_count,
                pages_with_text=pages_with_text,
                pages_using_ocr=pages_using_ocr,
                total_characters=len(cleaned_text),
                processing_time_ms=processing_time_ms,
                processing_status="COMPLETED"
            )

            # 9. Embedding and Indexing (Phase 3)
            indexing_summary = None
            if chunks:
                log("Generating Embeddings")
                start_indexing = time.time()
                
                embeddings = embedding_service.generate_embeddings(chunks)
                log("Embeddings Generated")
                
                payloads = []
                for i, chunk_text in enumerate(chunks):
                    payloads.append({
                        "document_id": metadata.document_id,
                        "filename": metadata.filename,
                        "chunk_index": i,
                        "chunk_text": chunk_text,
                        "sha256": metadata.sha256,
                        "upload_timestamp": metadata.upload_timestamp.isoformat()
                    })
                
                log("Storing Vectors in Qdrant")
                qdrant_provider.store_vectors(embeddings, payloads)
                indexing_time_ms = int((time.time() - start_indexing) * 1000)
                log("Vectors Stored Successfully")
                
                indexing_summary = IndexingSummary(
                    collection_name=qdrant_provider.collection_name,
                    vectors_stored=len(chunks),
                    indexing_status="COMPLETED",
                    indexing_time_ms=indexing_time_ms
                )
            
            preview = cleaned_text[:500] if cleaned_text else ""
            log("Processing Completed")

            return DocumentProcessingResult(
                metadata=metadata,
                cleaned_text=cleaned_text,
                chunks=chunks,
                preview=preview,
                processing_summary=summary,
                indexing_summary=indexing_summary,
                processing_logs=logs
            )

        except Exception as e:
            log(f"Processing Failed: {str(e)}")
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

processor = DocumentProcessor()
