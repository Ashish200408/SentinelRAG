# SentinelRAG Architecture

This document describes the architectural foundation for Phase 1 of SentinelRAG, a Self-Correcting Retrieval-Augmented Generation (RAG) platform.

## Layered Architecture & Clean Architecture

SentinelRAG enforces a Strict Clean Architecture to ensure separation of concerns, testability, and independence from frameworks and external services. The system is conceptually divided into layers:

1. **API / Presentation Layer (`backend/app/api/`)**: FastAPI routers that handle HTTP transport, authentication extraction, and request validation. Routers contain **no business logic**; they delegate strictly to the Service layer.
2. **Service Layer (`backend/app/services/`)**: Contains the core business rules. Services orchestrate domain logic but do not interact directly with databases or external APIs.
3. **Repository Layer (`backend/app/repositories/`)**: Abstracted data access layer. Repositories handle database interactions (via SQLAlchemy/PostgreSQL/Redis) and return domain schemas.
4. **Providers Layer (`backend/app/providers/`)**: Isolates all third-party integrations (e.g., Gemini SDK, Qdrant SDK, OCR APIs). Business logic must **never** directly call external SDKs. Only Providers communicate with external systems.
5. **Global Interfaces Layer (`backend/app/rag/interfaces/`)**: Defines the abstract contracts that Providers and Repositories must implement. This enforces the **Dependency Inversion Principle**.

## Dependency Flow

Dependencies must always point **inwards** toward the core domain logic:
- Routers -> Services
- Services -> Interfaces
- Providers/Repositories -> Interfaces (implementing them)

Every service, provider, and repository is injected via **FastAPI Depends** to ensure high testability and pluggability.

## The Common Package

Located at `backend/app/common/`, this package prevents code duplication by providing shared, cross-cutting utilities used across the backend.
- `exceptions/`: Shared application exceptions.
- `responses/`: Standard API response models.
- `types/`: Shared Python type definitions and aliases.
- `utils/`: Reusable helper functions.
- `validators/`: Common validation logic.

These utilities are strictly independent of business logic and avoid coupling modules.

## Monitoring & Observability

SentinelRAG enforces a strict separation between runtime monitoring and distributed observability:
- **Monitoring (`backend/app/monitoring/`)**: Responsible for health checks, readiness probes, liveness probes, latency tracking, resource usage, and basic performance metrics.
- **Observability (`backend/app/observability/`)**: Dedicated to deep telemetry, including OpenTelemetry, distributed tracing, structured JSON logging, and correlation IDs for request tracking.

## AI & RAG Module Architecture

The core of SentinelRAG resides in `backend/app/rag/`. This folder anticipates the modular nature of the AI platform. 
- Every AI capability (e.g., `ocr/`, `chunking/`, `embedding/`, `retrieval/`, `generation/`, `evaluation/`) is built as an independent, replaceable module. 
- Each module must define its own `interfaces.py`, `models.py`, `schemas.py`, `service.py`, and `exceptions.py`.

### RAG Prompt Management
Prompt templates (e.g., `retrieval_prompt.txt`, `system_prompt.txt`) exist exclusively under `backend/app/rag/prompts/`. They are strictly isolated from Python code, allowing them to be version-controlled, independently managed, and easily adjusted without redeploying logic.

### Pipeline Layer vs. Orchestration
- **Pipeline (`backend/app/rag/pipeline/`)**: The Pipeline coordinates the high-level execution flow of the Self-Correcting RAG process. The planned workflow invokes modules in this specific order:
  `User Query` -> `Retriever` -> `Context Evaluator` -> `Decision Engine` -> `Query Rewriter` (if required) -> `Clarification Generator` (if required) -> `Answer Generator` -> `Metrics Collection` -> `Final Response`
- **Orchestration (`backend/app/rag/orchestration/`)**: Contains the implementation details of the state machine (e.g., LangGraph). The Pipeline invokes orchestration but remains entirely agnostic to any specific workflow engine.

## Future Deployment & Evaluation Flow

- **Deployment**: `docker/` provides varying optimization strategies through `development/` and `production/` environments.
- **Evaluation**: The `evaluation/` directory structures the measurement of hallucination reduction. It separates baselines, self-corrected outputs, and metrics.
