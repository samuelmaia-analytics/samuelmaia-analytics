from __future__ import annotations

import subprocess
import time
import urllib.request
from pathlib import Path


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    process = subprocess.Popen(
        [
            str(root / ".venv" / "Scripts" / "streamlit.exe"),
            "run",
            "app/streamlit_app.py",
            "--server.headless",
            "true",
            "--server.port",
            "8511",
        ],
        cwd=root,
    )
    try:
        deadline = time.time() + 45
        while time.time() < deadline:
            try:
                with urllib.request.urlopen("http://127.0.0.1:8511", timeout=2) as response:
                    if response.status == 200:
                        break
            except Exception:
                time.sleep(1)
        else:
            raise SystemExit("Streamlit smoke failed: app did not become ready.")
    finally:
        process.terminate()
        process.wait(timeout=10)


if __name__ == "__main__":
    main()

