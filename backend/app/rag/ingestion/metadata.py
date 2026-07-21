from app.rag.ingestion.models import DocumentMetadata

class MetadataGenerator:
    def generate(self, filename: str, file_size: int, sha256: str, document_type: str = "application/pdf") -> DocumentMetadata:
        """
        Generates standard metadata for a document.
        """
        return DocumentMetadata(
            filename=filename,
            file_size=file_size,
            sha256=sha256,
            document_type=document_type
        )

metadata_generator = MetadataGenerator()
