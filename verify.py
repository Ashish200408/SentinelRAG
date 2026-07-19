import os
from pathlib import Path

BASE_DIR = Path("c:/SentinelRAG")

def ensure_dir(path, readme_text):
    p = BASE_DIR / path
    p.mkdir(parents=True, exist_ok=True)
    
    readme = p / "README.md"
    if not readme.exists() or readme.read_text().strip() == f"# {p.name}":
        readme.write_text(f"# {p.name}\n\n**Purpose:** {readme_text}\n\n**Responsibilities:** TBD in future phases.\n\n**Future Usage:** TBD.\n")
    
    return p

# 1. RAG Structure
rag_folders = ["interfaces", "pipeline", "prompts", "ingestion", "ocr", "chunking", "embedding", "retrieval", "evaluation", "rewriter", "clarification", "generation", "orchestration", "metrics"]
for folder in rag_folders:
    p = ensure_dir(f"backend/app/rag/{folder}", f"RAG {folder} module.")
    (p / "__init__.py").touch(exist_ok=True)

# 2. Providers
provider_folders = ["gemini", "qdrant", "postgres", "redis", "ocr", "storage"]
for folder in provider_folders:
    p = ensure_dir(f"backend/app/providers/{folder}", "Provider integration. Providers are the ONLY layer allowed to communicate with external SDKs and services.")
    (p / "__init__.py").touch(exist_ok=True)

# 3. Configuration
config_dir = BASE_DIR / "backend/app/config"
config_dir.mkdir(parents=True, exist_ok=True)
for f in ["settings.py", "constants.py", "logging.py", "thresholds.py"]:
    (config_dir / f).touch(exist_ok=True)

# 5. Common Package
common_folders = ["exceptions", "responses", "types", "utils", "validators"]
for folder in common_folders:
    p = ensure_dir(f"backend/app/common/{folder}", f"Shared {folder} utilities.")
    (p / "__init__.py").touch(exist_ok=True)

# 8. Gitignore
gitignore_path = BASE_DIR / ".gitignore"
if gitignore_path.exists():
    content = gitignore_path.read_text()
    for item in [".venv/", "__pycache__/", ".pytest_cache/", ".mypy_cache/", ".ruff_cache/", ".env", ".env.*", "node_modules/", "dist/", "build/"]:
        if item not in content:
            content += f"\n{item}"
    if "!.env.example" not in content:
        content += "\n!.env.example\n!.env.backend.example\n!.env.frontend.example"
    gitignore_path.write_text(content)

print("Verification complete.")
