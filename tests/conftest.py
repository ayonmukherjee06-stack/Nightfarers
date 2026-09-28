import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = ROOT_DIR / "backend"
FRONTEND_DIR = ROOT_DIR / "frontend"

for p in [ROOT_DIR, BACKEND_DIR, FRONTEND_DIR]:
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))
