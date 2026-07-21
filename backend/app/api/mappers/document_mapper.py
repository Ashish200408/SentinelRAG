from app.rag.ingestion.models import DocumentProcessingResult
from app.schemas.document import DocumentResponse, DocumentResponseData

class DocumentResponseMapper:
    def map_to_response(self, result: DocumentProcessingResult) -> DocumentResponse:
        return DocumentResponse(
            status="success",
            data=DocumentResponseData(
                document_id=result.metadata.document_id,
                filename=result.metadata.filename,
                file_size=result.metadata.file_size,
                sha256=result.metadata.sha256,
                document_type=result.metadata.document_type,
                upload_timestamp=result.metadata.upload_timestamp.isoformat(),
                chunk_count=len(result.chunks),
                preview=result.preview,
                processing_summary=result.processing_summary
            )
        )

document_mapper = DocumentResponseMapper()
