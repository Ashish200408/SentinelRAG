# SentinelRAG

SentinelRAG is an enterprise-grade Self-Correcting Retrieval-Augmented Generation (RAG) platform.

## Overview
This platform builds a RAG system over messy, unstructured documents that detects insufficient or conflicting retrieved context and intelligently decides whether to:
- Generate an answer
- Rewrite the search query
- Ask a clarification question
- Return a low-confidence response

## Project Structure
- `backend/`: FastAPI application (Python)
- `frontend/`: React 19 application (Vite, TypeScript)
- `docker/`: Docker configurations
- `docs/`: Project documentation and architecture
- `datasets/`: Data ingestion and evaluation datasets
- `evaluation/`: Output evaluation harnesses
- `infra/`: Infrastructure as Code (Terraform/K8s)
- `scripts/`: Utility scripts

## Getting Started
Please see `ARCHITECTURE.md` for a comprehensive architectural deep dive.

To run the development environment:
```bash
make docker
```
