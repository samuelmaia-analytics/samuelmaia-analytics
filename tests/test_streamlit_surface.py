from __future__ import annotations

import importlib.util
from pathlib import Path


def test_streamlit_entrypoints_import_cleanly() -> None:
    root = Path(__file__).resolve().parents[1]
    entrypoints = [root / "streamlit_app.py", *sorted((root / "pages").glob("*.py"))]

    for path in entrypoints:
        spec = importlib.util.spec_from_file_location(path.stem, path)
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(module)
