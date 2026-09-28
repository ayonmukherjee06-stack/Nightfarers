"""MasteryFlow FastAPI Backend Server Launcher.
Single-command bootstrap script for the REST API layer.
"""

import sys
from pathlib import Path

# Add project root and backend to sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))
sys.path.insert(0, str(Path(__file__).resolve().parent))

# Ensure UTF-8 output encoding on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import uvicorn


def main():
    print("=" * 80)
    print(" [*] Launching MasteryFlow FastAPI REST Backend")
    print(" [*] Interactive Swagger API Docs: http://127.0.0.1:8000/docs")
    print(" [*] OpenAPI JSON Schema:          http://127.0.0.1:8000/openapi.json")
    print("=" * 80)

    # Use backend.api.server:app with fallback to masteryflow.api.server:app
    try:
        import backend.api.server
        app_target = "backend.api.server:app"
    except ImportError:
        app_target = "masteryflow.api.server:app"

    uvicorn.run(
        app_target,
        host="127.0.0.1",
        port=8000,
        reload=False,
        log_level="info"
    )


if __name__ == "__main__":
    main()
