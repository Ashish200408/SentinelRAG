import os
from pathlib import Path

BASE_DIR = Path("c:/SentinelRAG")

directories = {
    # Backend
    "backend/app/api": "FastAPI routers and endpoint definitions.",
    "backend/app/common/exceptions": "Shared application exceptions.",
    "backend/app/common/responses": "Standard API response models.",
    "backend/app/common/types": "Shared Python type definitions and aliases.",
    "backend/app/common/utils": "Reusable helper functions.",
    "backend/app/common/validators": "Common validation logic used across multiple modules.",
    "backend/app/core": "App-wide core logic (exceptions, lifespan).",
    "backend/app/config": "Config files (settings.py, constants.py, thresholds.py, logging.py).",
    "backend/app/dependencies": "Dependency Injection (FastAPI Depends).",
    "backend/app/middleware": "Custom middlewares (CORS, timing, auth).",
    "backend/app/monitoring": "Health Checks, Readiness, Liveness, Latency, Metrics.",
    "backend/app/observability": "OpenTelemetry, Prometheus, Tracing, Structured Logging.",
    "backend/app/providers": "External integrations (gemini, qdrant, postgres, redis, ocr, storage).",
    "backend/app/repositories": "Data access layer (Database interactions).",
    "backend/app/services": "Business logic layer.",
    "backend/app/database": "DB connection management and migrations (Alembic).",
    "backend/app/workers": "Background tasks (e.g., Celery/RQ).",
    "backend/app/models": "ORM models (SQLAlchemy).",
    "backend/app/schemas": "Pydantic validation schemas.",
    "backend/app/rag/interfaces": "Abstract interfaces and contracts (EmbeddingProvider, etc.).",
    "backend/app/rag/pipeline": "High-level RAG execution workflow coordinating the entire execution.",
    "backend/app/rag/prompts": "AI prompt templates isolated from Python logic.",
    "backend/app/rag/orchestration": "LangGraph State Machine logic.",
    "backend/app/rag/ingestion": "Document processing module.",
    "backend/app/rag/ocr": "Optical Character Recognition module.",
    "backend/app/rag/chunking": "Semantic chunking module.",
    "backend/app/rag/embedding": "Vector generation module.",
    "backend/app/rag/retrieval": "Vector Search & Reranking module.",
    "backend/app/rag/evaluation": "Context Evaluation module.",
    "backend/app/rag/rewriter": "Query Rewriting module.",
    "backend/app/rag/clarification": "Clarification Generation module.",
    "backend/app/rag/generation": "Final Answer Generation module.",
    "backend/app/rag/metrics": "Telemetry and Dashboard stats module.",
    "backend/tests/unit": "Unit testing.",
    "backend/tests/api": "API integration testing.",
    "backend/tests/rag": "RAG specific testing.",
    "backend/tests/integration": "End-to-end integration testing.",
    "backend/tests/evaluation": "Evaluation harnesses.",
    "backend/tests/fixtures": "Test fixtures.",
    "backend/tests/performance": "Performance testing.",
    # Frontend
    "frontend/src/api": "API client layer (React Query).",
    "frontend/src/assets": "Static assets.",
    "frontend/src/components": "Reusable UI components.",
    "frontend/src/features": "Future AI features logic and UI.",
    "frontend/src/hooks": "Custom React hooks.",
    "frontend/src/layouts": "Page layouts.",
    "frontend/src/pages": "Route components.",
    "frontend/src/providers": "Context providers.",
    "frontend/src/routes": "Route configurations.",
    "frontend/src/services": "Frontend business logic.",
    "frontend/src/store": "Global state (Zustand).",
    "frontend/src/styles": "Global styles.",
    "frontend/src/types": "TypeScript type definitions.",
    "frontend/src/utils": "Helper functions.",
    # Docker
    "docker/backend": "Backend specific Docker configurations.",
    "docker/frontend": "Frontend specific Docker configurations.",
    "docker/compose": "docker-compose override files (dev, prod).",
    "docker/development": "Development Dockerfiles.",
    "docker/production": "Optimized production containers.",
    "docker/nginx": "Reverse proxy configurations.",
    "docker/monitoring": "Prometheus/Grafana configs.",
    # Root Level
    "docs/architecture": "Architecture documentation.",
    "docs/api": "API documentation.",
    "docs/diagrams": "Architecture diagrams.",
    "docs/images": "Images and screenshots.",
    "docs/presentation": "Presentation materials.",
    "datasets/raw": "Raw source datasets.",
    "datasets/processed": "Processed datasets.",
    "datasets/ocr": "OCR outputs and samples.",
    "datasets/evaluation": "Datasets meant for evaluation.",
    "datasets/sample_documents": "Sample PDFs and documents.",
    "evaluation/baseline": "Baseline evaluations.",
    "evaluation/self_corrected": "Self-corrected response evaluations.",
    "evaluation/questions": "Test query sets.",
    "evaluation/metrics": "Calculated metrics over time.",
    "evaluation/results": "Hallucination comparison results.",
    "evaluation/reports": "Generated reports.",
    "infra": "Terraform, Kubernetes manifests, IaC.",
    "scripts": "Utility scripts (start.sh, dev.sh, etc).",
    ".github/workflows": "CI/CD pipelines.",
}

# RAG Modules that need specific python files
rag_modules = [
    "ingestion", "ocr", "chunking", "embedding", "retrieval", 
    "evaluation", "rewriter", "clarification", "generation", "metrics", "orchestration"
]

def create_scaffold():
    for dir_path, readme_text in directories.items():
        p = BASE_DIR / dir_path
        p.mkdir(parents=True, exist_ok=True)
        readme = p / "README.md"
        if not readme.exists():
            readme.write_text(f"# {p.name}\n\n{readme_text}\n")
    
    # Create empty RAG module files
    for mod in rag_modules:
        mod_dir = BASE_DIR / f"backend/app/rag/{mod}"
        for f in ["__init__.py", "interfaces.py", "models.py", "schemas.py", "service.py", "exceptions.py"]:
            (mod_dir / f).touch(exist_ok=True)

    # Empty env files
    (BASE_DIR / ".env.example").touch(exist_ok=True)
    (BASE_DIR / ".env.backend.example").touch(exist_ok=True)
    (BASE_DIR / ".env.frontend.example").touch(exist_ok=True)
    
    # Empty scripts
    scripts = ["start.sh", "dev.sh", "docker.sh", "seed.sh", "reset.sh", "healthcheck.sh"]
    for s in scripts:
        (BASE_DIR / "scripts" / s).touch(exist_ok=True)
        
    print("Scaffolding complete.")

if __name__ == "__main__":
    create_scaffold()
