"""MasteryFlow Interactive Student UI & Glass-Box Portal Launcher.
Supports automatic port detection and seamless presentation launch.
"""

import subprocess
import sys
import socket
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

def is_port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("localhost", port)) == 0

def main():
    port = 8501
    while is_port_in_use(port):
        port += 1

    print("=" * 80)
    print(" 🚀 Launching MasteryFlow Interactive Student UI & Glass-Box Portal")
    print(f" 🌐 Target URL: http://localhost:{port}")
    print("=" * 80)

    # Determine app path
    app_path = ROOT_DIR / "frontend" / "app.py"
    if not app_path.exists():
        app_path = Path(__file__).resolve().parent / "app.py"
    if not app_path.exists():
        app_path = ROOT_DIR / "masteryflow" / "ui" / "app.py"

    cmd = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        str(app_path),
        "--server.port",
        str(port),
    ]
    subprocess.run(cmd)

if __name__ == "__main__":
    main()
