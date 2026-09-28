"""MasteryFlow FastAPI Backend Server Launcher (Root Shortcut).
Delegates to backend/run_api.py.
"""

import sys
from pathlib import Path

# Ensure root is in sys.path
ROOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR))

if __name__ == "__main__":
    from backend.run_api import main
    main()
