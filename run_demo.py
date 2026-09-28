"""MasteryFlow Unified Full-Stack Launch Script.

Authored by: Ayon Mukherjee (Team Lead & Orchestrator)
Role: One-command launcher that boots both the FastAPI backend (port 8000)
and the Streamlit frontend portal (port 8501) seamlessly.
"""

import subprocess
import sys
import socket
import time

# Ensure UTF-8 output encoding on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


def is_port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) == 0


def main():
    print("=" * 80)
    print(" [*] MASTERYFLOW FULL-STACK ADAPTIVE ENGINE BOOTSTRAP")
    print("=" * 80)

    # 1. Boot FastAPI backend on port 8000 if not already running
    api_proc = None
    if not is_port_in_use(8000):
        print(" [+] Starting FastAPI REST Backend on http://127.0.0.1:8000...")
        api_proc = subprocess.Popen(
            [sys.executable, "run_api.py"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        time.sleep(1.5)
        print(" [+] FastAPI REST Backend online (Interactive Docs: http://127.0.0.1:8000/docs)")
    else:
        print(" [*] FastAPI REST Backend already running on http://127.0.0.1:8000")

    # 2. Determine available Streamlit port
    port = 8501
    while is_port_in_use(port):
        port += 1

    print(f" [+] Launching MasteryFlow Unified Portal on http://localhost:{port}")
    print("=" * 80)

    app_path = "frontend/app.py"
    cmd = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        app_path,
        "--server.port",
        str(port),
    ]

    try:
        subprocess.run(cmd)
    finally:
        if api_proc is not None:
            api_proc.terminate()


if __name__ == "__main__":
    main()
