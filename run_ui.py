"""MasteryFlow Interactive UI Portal Launcher (Root Shortcut).
Delegates to frontend/run_ui.py.
"""

import sys
from pathlib import Path

# Ensure root is in sys.path
ROOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR))

if __name__ == "__main__":
    from frontend.run_ui import main
    main()
