import logging
logging.basicConfig(level=logging.INFO)

from app.rag.retrieval.service import retrieval_service

chunks = retrieval_service.retrieve("What is CRUD?")
print(f"Returned {len(chunks)} chunks.")
for c in chunks:
    print(c)
