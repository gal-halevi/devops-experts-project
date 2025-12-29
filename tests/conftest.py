import sys
from pathlib import Path

import pytest


@pytest.fixture()
def app_module(tmp_path: Path, monkeypatch):
    """
    Set COUNTER_PATH then (re)load src.app so its module-level COUNTER_PATH
    points to a temp file for the test.
    """
    counter_file = tmp_path / "counter.txt"
    monkeypatch.setenv("COUNTER_PATH", str(counter_file))

    # Force a fresh import so module-level COUNTER_PATH is re-evaluated.
    # (Python caches imported modules in sys.modules.)
    sys.modules.pop("src.app", None)
    import src.app
    return src.app


@pytest.fixture()
def client(app_module):
    return app_module.app.test_client()