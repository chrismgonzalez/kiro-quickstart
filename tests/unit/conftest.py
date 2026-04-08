"""Pytest configuration for unit tests."""

import pytest
import os
import tempfile
from pathlib import Path


@pytest.fixture(autouse=True)
def isolated_task_storage(monkeypatch, tmp_path):
    """Automatically isolate task storage for each test.
    
    This fixture:
    - Creates a temporary directory for each test
    - Sets TEST_TASK_FILE env var to use temp directory
    - Ensures tests don't share state
    """
    task_file = tmp_path / "tasks.json"
    monkeypatch.setenv('TEST_TASK_FILE', str(task_file))
    return task_file
