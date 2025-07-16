#!/usr/bin/env python3
"""
Utility script to launch both the backend (FastAPI / Uvicorn) and the frontend (Vite / React)
in a single command: `python run.py`.

The script will:
1. Spawn the backend with hot-reload enabled.
2. Spawn the frontend dev server.
3. Keep running until you press Ctrl-C, after which it will shut down both processes.
"""
from __future__ import annotations

import os
import signal
import subprocess
import sys
import time
from pathlib import Path
from typing import List

ROOT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = ROOT_DIR / "backend"
FRONTEND_DIR = ROOT_DIR / "frontend"

# Commands to launch each service. Feel free to adjust ports or flags here.
BACKEND_CMD: List[str] = [
    sys.executable,
    "-m",
    "uvicorn",
    "main:app",
    "--reload",
    "--host",
    "0.0.0.0",
    "--port",
    "8000",
]
FRONTEND_CMD: List[str] = ["npm", "run", "dev"]


def launch_process(cmd: List[str], cwd: Path) -> subprocess.Popen:
    """Launch a subprocess and return the Popen object."""
    print(f"Starting {' '.join(cmd)} in {cwd}")
    return subprocess.Popen(cmd, cwd=str(cwd))


def main() -> None:
    """Entry-point: start both servers and keep them alive until interrupted."""
    processes: List[subprocess.Popen] = []

    try:
        processes.append(launch_process(BACKEND_CMD, BACKEND_DIR))
        processes.append(launch_process(FRONTEND_CMD, FRONTEND_DIR))

        # Monitor processes. If any exits, terminate all.
        while True:
            time.sleep(1)
            for proc in processes:
                if proc.poll() is not None:  # Process has finished
                    raise RuntimeError(
                        f"Process {' '.join(proc.args)} exited with code {proc.returncode}"
                    )
    except KeyboardInterrupt:
        print("\nReceived Ctrl-C — shutting down.")
    except RuntimeError as exc:
        print(str(exc))
    finally:
        # Gracefully terminate child processes
        for proc in processes:
            if proc.poll() is None:
                proc.terminate()
        # Give them a moment to exit gracefully
        time.sleep(2)
        # Force kill if still running
        for proc in processes:
            if proc.poll() is None:
                proc.kill()
        print("All child processes stopped. Bye!")


if __name__ == "__main__":
    # Ensure script is run from project root for predictable paths
    os.chdir(ROOT_DIR)
    main()
