from __future__ import annotations

import json
import subprocess
import time
import urllib.request
from pathlib import Path


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    process = subprocess.Popen(
        [
            str(root / ".venv" / "Scripts" / "python.exe"),
            "-m",
            "uvicorn",
            "services.api.main:app",
            "--host",
            "127.0.0.1",
            "--port",
            "8010",
        ],
        cwd=root,
    )
    try:
        deadline = time.time() + 30
        while time.time() < deadline:
            try:
                with urllib.request.urlopen("http://127.0.0.1:8010/health", timeout=2) as response:
                    payload = json.loads(response.read().decode("utf-8"))
                if payload.get("status") == "ok":
                    break
            except Exception:
                time.sleep(1)
        else:
            raise SystemExit("API smoke failed: health endpoint did not become ready.")
    finally:
        process.terminate()
        process.wait(timeout=10)


if __name__ == "__main__":
    main()

