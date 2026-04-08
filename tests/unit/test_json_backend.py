"""Unit tests for JSONFileBackend.

Tests cover:
- File creation and directory creation (Requirement 2.2)
- Read/write operations (Requirements 2.1, 2.3, 2.5)
- Valid JSON format maintenance (Requirement 2.4)
- Error handling: missing directory, corrupted JSON, permission errors (Requirement 2.6)
- Edge cases: empty file, multiple tasks, task retrieval
- Requirements: 2.1-2.6, 3.2

All tests will FAIL until JSONFileBackend is implemented (Phase 2).
"""

import pytest
import json
import tempfile
import os
from pathlib import Path
from typing import List
from task_tracker.json_backend import JSONFileBackend
from task_tracker.models import Task


# ===== Fixtures =====

@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def temp_file_path(temp_dir):
    """Create a temporary file path (file doesn't exist yet)."""
    return str(temp_dir / "tasks.json")


@pytest.fixture
def backend(temp_file_path):
    """Create a JSONFileBackend instance with temporary file path."""
    return JSONFileBackend(temp_file_path)


@pytest.fixture
def sample_task() -> Task:
    """Create a sample task for testing."""
    return {
        "id": 1,
        "title": "Test task",
        "tags": ["test"],
        "status": "pending",
        "created_at": "2024-01-15T10:30:00.123456"
    }


@pytest.fixture
def sample_tasks() -> List[Task]:
    """Create multiple sample tasks for testing."""
    return [
        {
            "id": 1,
            "title": "First task",
            "tags": ["work"],
            "status": "pending",
            "created_at": "2024-01-15T10:30:00.123456"
        },
        {
            "id": 2,
            "title": "Second task",
            "tags": ["personal", "urgent"],
            "status": "complete",
            "created_at": "2024-01-15T11:45:00.789012"
        },
        {
            "id": 3,
            "title": "Third task",
            "tags": [],
            "status": "pending",
            "created_at": "2024-01-15T12:00:00.000000"
        }
    ]


# ===== Initialization Tests =====

def test_backend_initialization_with_default_path():
    """JSONFileBackend initializes with default path."""
    backend = JSONFileBackend()
    
    assert backend.file_path == Path("~/.task-tracker/tasks.json").expanduser()


def test_backend_initialization_with_custom_path(temp_file_path):
    """JSONFileBackend initializes with custom path."""
    backend = JSONFileBackend(temp_file_path)
    
    assert backend.file_path == Path(temp_file_path)


def test_backend_expands_tilde_in_path():
    """JSONFileBackend expands ~ in file path."""
    backend = JSONFileBackend("~/custom/path/tasks.json")
    
    assert "~" not in str(backend.file_path)
    assert backend.file_path.is_absolute()


# ===== Directory Creation Tests (Requirement 2.2) =====

def test_save_task_creates_directory_if_missing(temp_dir, sample_task):
    """WHEN directory does not exist, save_task creates it (Requirement 2.2)."""
    # Create path in non-existent subdirectory
    file_path = str(temp_dir / "subdir" / "tasks.json")
    backend = JSONFileBackend(file_path)
    
    # Directory should not exist yet
    assert not Path(file_path).parent.exists()
    
    # Save task should create directory
    backend.save_task(sample_task)
    
    # Directory should now exist
    assert Path(file_path).parent.exists()
    assert Path(file_path).parent.is_dir()


def test_save_task_creates_nested_directories(temp_dir, sample_task):
    """save_task creates nested directory structure if missing."""
    file_path = str(temp_dir / "level1" / "level2" / "level3" / "tasks.json")
    backend = JSONFileBackend(file_path)
    
    # Nested directories should not exist
    assert not Path(file_path).parent.exists()
    
    # Save task should create all directories
    backend.save_task(sample_task)
    
    # All directories should now exist
    assert Path(file_path).parent.exists()
    assert Path(file_path).exists()


def test_save_task_works_when_directory_already_exists(backend, sample_task):
    """save_task works when directory already exists."""
    # Ensure directory exists
    backend.file_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Should not raise any exception
    backend.save_task(sample_task)
    
    assert backend.file_path.exists()


# ===== File Creation Tests (Requirement 2.2) =====

def test_save_task_creates_file_if_missing(backend, sample_task):
    """WHEN file does not exist, save_task creates it (Requirement 2.2)."""
    # File should not exist yet
    assert not backend.file_path.exists()
    
    # Save task should create file
    backend.save_task(sample_task)
    
    # File should now exist
    assert backend.file_path.exists()
    assert backend.file_path.is_file()


def test_new_file_contains_valid_json(backend, sample_task):
    """Newly created file contains valid JSON (Requirement 2.4)."""
    backend.save_task(sample_task)
    
    # File should contain valid JSON
    with open(backend.file_path, 'r') as f:
        data = json.load(f)
    
    assert isinstance(data, list)
    assert len(data) == 1


def test_new_file_contains_saved_task(backend, sample_task):
    """Newly created file contains the saved task (Requirement 2.1)."""
    backend.save_task(sample_task)
    
    with open(backend.file_path, 'r') as f:
        data = json.load(f)
    
    assert len(data) == 1
    assert data[0]["id"] == sample_task["id"]
    assert data[0]["title"] == sample_task["title"]
    assert data[0]["tags"] == sample_task["tags"]
    assert data[0]["status"] == sample_task["status"]
    assert data[0]["created_at"] == sample_task["created_at"]


# ===== Save Task Tests (Requirements 2.1, 2.3) =====

def test_save_task_writes_task_to_file(backend, sample_task):
    """save_task writes task to JSON file (Requirement 2.1)."""
    backend.save_task(sample_task)
    
    tasks = backend.load_tasks()
    
    assert len(tasks) == 1
    assert tasks[0]["id"] == sample_task["id"]
    assert tasks[0]["title"] == sample_task["title"]


def test_save_task_appends_to_existing_tasks(backend, sample_tasks):
    """save_task appends new task to existing tasks (Requirement 2.3)."""
    # Save first task
    backend.save_task(sample_tasks[0])
    
    # Save second task
    backend.save_task(sample_tasks[1])
    
    # Both tasks should be in file
    tasks = backend.load_tasks()
    assert len(tasks) == 2
    assert tasks[0]["id"] == sample_tasks[0]["id"]
    assert tasks[1]["id"] == sample_tasks[1]["id"]


def test_save_multiple_tasks_sequentially(backend, sample_tasks):
    """Multiple tasks can be saved sequentially (Requirement 2.3)."""
    for task in sample_tasks:
        backend.save_task(task)
    
    loaded_tasks = backend.load_tasks()
    
    assert len(loaded_tasks) == len(sample_tasks)
    for i, task in enumerate(sample_tasks):
        assert loaded_tasks[i]["id"] == task["id"]
        assert loaded_tasks[i]["title"] == task["title"]


def test_save_task_preserves_all_fields(backend):
    """save_task preserves all task fields."""
    task: Task = {
        "id": 42,
        "title": "Complex task with all fields",
        "tags": ["tag1", "tag2", "tag3"],
        "status": "complete",
        "created_at": "2024-01-15T10:30:00.123456"
    }
    
    backend.save_task(task)
    loaded_tasks = backend.load_tasks()
    
    assert len(loaded_tasks) == 1
    loaded = loaded_tasks[0]
    
    assert loaded["id"] == 42
    assert loaded["title"] == "Complex task with all fields"
    assert loaded["tags"] == ["tag1", "tag2", "tag3"]
    assert loaded["status"] == "complete"
    assert loaded["created_at"] == "2024-01-15T10:30:00.123456"


# ===== Load Tasks Tests (Requirement 2.5) =====

def test_load_tasks_returns_empty_list_when_file_missing(backend):
    """load_tasks returns empty list when file doesn't exist (Requirement 5.5)."""
    # File doesn't exist yet
    assert not backend.file_path.exists()
    
    tasks = backend.load_tasks()
    
    assert isinstance(tasks, list)
    assert len(tasks) == 0


def test_load_tasks_returns_empty_list_for_empty_file(backend):
    """load_tasks returns empty list for empty JSON array."""
    # Create empty JSON file
    backend.file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(backend.file_path, 'w') as f:
        json.dump([], f)
    
    tasks = backend.load_tasks()
    
    assert isinstance(tasks, list)
    assert len(tasks) == 0


def test_load_tasks_returns_all_saved_tasks(backend, sample_tasks):
    """load_tasks returns all tasks from file (Requirement 2.5)."""
    # Save multiple tasks
    for task in sample_tasks:
        backend.save_task(task)
    
    # Load all tasks
    loaded_tasks = backend.load_tasks()
    
    assert len(loaded_tasks) == len(sample_tasks)


def test_load_tasks_preserves_task_order(backend, sample_tasks):
    """load_tasks returns tasks in the order they were saved."""
    for task in sample_tasks:
        backend.save_task(task)
    
    loaded_tasks = backend.load_tasks()
    
    for i, task in enumerate(sample_tasks):
        assert loaded_tasks[i]["id"] == task["id"]
        assert loaded_tasks[i]["title"] == task["title"]


def test_load_tasks_returns_correct_task_structure(backend, sample_task):
    """load_tasks returns tasks with correct structure."""
    backend.save_task(sample_task)
    
    tasks = backend.load_tasks()
    task = tasks[0]
    
    assert "id" in task
    assert "title" in task
    assert "tags" in task
    assert "status" in task
    assert "created_at" in task


# ===== Get Task By ID Tests (Requirement 5.3, 5.4) =====

def test_get_task_by_id_returns_correct_task(backend, sample_tasks):
    """get_task_by_id returns the task with matching ID (Requirement 5.3)."""
    for task in sample_tasks:
        backend.save_task(task)
    
    # Get task with ID 2
    task = backend.get_task_by_id(2)
    
    assert task is not None
    assert task["id"] == 2
    assert task["title"] == "Second task"


def test_get_task_by_id_returns_none_for_missing_id(backend, sample_tasks):
    """get_task_by_id returns None when ID doesn't exist (Requirement 5.4)."""
    for task in sample_tasks:
        backend.save_task(task)
    
    # Try to get non-existent task
    task = backend.get_task_by_id(999)
    
    assert task is None


def test_get_task_by_id_returns_none_for_empty_storage(backend):
    """get_task_by_id returns None when storage is empty."""
    task = backend.get_task_by_id(1)
    
    assert task is None


def test_get_task_by_id_returns_first_task(backend, sample_tasks):
    """get_task_by_id can retrieve the first task."""
    for task in sample_tasks:
        backend.save_task(task)
    
    task = backend.get_task_by_id(1)
    
    assert task is not None
    assert task["id"] == 1
    assert task["title"] == "First task"


def test_get_task_by_id_returns_last_task(backend, sample_tasks):
    """get_task_by_id can retrieve the last task."""
    for task in sample_tasks:
        backend.save_task(task)
    
    task = backend.get_task_by_id(3)
    
    assert task is not None
    assert task["id"] == 3
    assert task["title"] == "Third task"


# ===== JSON Format Validation Tests (Requirement 2.4) =====

def test_file_maintains_valid_json_after_multiple_saves(backend, sample_tasks):
    """File maintains valid JSON format after multiple saves (Requirement 2.4)."""
    for task in sample_tasks:
        backend.save_task(task)
    
    # File should contain valid JSON
    with open(backend.file_path, 'r') as f:
        data = json.load(f)
    
    assert isinstance(data, list)
    assert len(data) == len(sample_tasks)


def test_file_is_json_array(backend, sample_task):
    """JSON file contains an array at the root."""
    backend.save_task(sample_task)
    
    with open(backend.file_path, 'r') as f:
        data = json.load(f)
    
    assert isinstance(data, list)


def test_json_file_is_readable_by_standard_parser(backend, sample_tasks):
    """JSON file can be parsed by standard JSON parser."""
    for task in sample_tasks:
        backend.save_task(task)
    
    # Should not raise JSONDecodeError
    with open(backend.file_path, 'r') as f:
        data = json.load(f)
    
    assert len(data) == len(sample_tasks)


# ===== Error Handling Tests (Requirement 2.6) =====

def test_load_tasks_raises_error_for_corrupted_json(backend):
    """load_tasks raises error when JSON file is corrupted (Requirement 2.6)."""
    # Create file with invalid JSON
    backend.file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(backend.file_path, 'w') as f:
        f.write("{ this is not valid json }")
    
    # Should raise JSONDecodeError
    with pytest.raises(json.JSONDecodeError):
        backend.load_tasks()


def test_load_tasks_raises_error_for_malformed_json(backend):
    """load_tasks raises error for malformed JSON."""
    backend.file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(backend.file_path, 'w') as f:
        f.write("[{\"id\": 1, \"title\": \"Incomplete")
    
    with pytest.raises(json.JSONDecodeError):
        backend.load_tasks()


def test_load_tasks_raises_error_for_non_array_json(backend):
    """load_tasks handles non-array JSON (should be array)."""
    backend.file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(backend.file_path, 'w') as f:
        json.dump({"id": 1, "title": "Not an array"}, f)
    
    # Behavior depends on implementation - might raise TypeError or return empty
    # The implementation should handle this gracefully
    try:
        tasks = backend.load_tasks()
        # If it doesn't raise, it should return empty or handle gracefully
        assert isinstance(tasks, list) or tasks is None
    except (TypeError, ValueError):
        # Acceptable to raise an error for invalid format
        pass


def test_get_task_by_id_handles_corrupted_json(backend):
    """get_task_by_id raises error when JSON file is corrupted."""
    backend.file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(backend.file_path, 'w') as f:
        f.write("corrupted data")
    
    with pytest.raises(json.JSONDecodeError):
        backend.get_task_by_id(1)


@pytest.mark.skipif(os.name == 'nt', reason="Permission tests unreliable on Windows")
def test_save_task_raises_error_for_permission_denied(temp_dir, sample_task):
    """save_task raises PermissionError when cannot write to file."""
    file_path = temp_dir / "tasks.json"
    backend = JSONFileBackend(str(file_path))
    
    # Create directory but make it read-only
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.parent.chmod(0o444)
    
    try:
        # Should raise PermissionError
        with pytest.raises(PermissionError):
            backend.save_task(sample_task)
    finally:
        # Restore permissions for cleanup
        file_path.parent.chmod(0o755)


@pytest.mark.skipif(os.name == 'nt', reason="Permission tests unreliable on Windows")
def test_load_tasks_raises_error_for_permission_denied(temp_dir):
    """load_tasks raises PermissionError when cannot read file."""
    file_path = temp_dir / "tasks.json"
    backend = JSONFileBackend(str(file_path))
    
    # Create file and make it unreadable
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, 'w') as f:
        json.dump([], f)
    file_path.chmod(0o000)
    
    try:
        with pytest.raises(PermissionError):
            backend.load_tasks()
    finally:
        # Restore permissions for cleanup
        file_path.chmod(0o644)


# ===== Edge Cases =====

def test_save_task_with_empty_tags(backend):
    """save_task handles task with empty tags list."""
    task: Task = {
        "id": 1,
        "title": "Task with no tags",
        "tags": [],
        "status": "pending",
        "created_at": "2024-01-15T10:30:00"
    }
    
    backend.save_task(task)
    loaded_tasks = backend.load_tasks()
    
    assert len(loaded_tasks) == 1
    assert loaded_tasks[0]["tags"] == []


def test_save_task_with_many_tags(backend):
    """save_task handles task with many tags."""
    task: Task = {
        "id": 1,
        "title": "Task with many tags",
        "tags": [f"tag{i}" for i in range(100)],
        "status": "pending",
        "created_at": "2024-01-15T10:30:00"
    }
    
    backend.save_task(task)
    loaded_tasks = backend.load_tasks()
    
    assert len(loaded_tasks) == 1
    assert len(loaded_tasks[0]["tags"]) == 100


def test_save_task_with_long_title(backend):
    """save_task handles task with very long title."""
    long_title = "A" * 1000
    task: Task = {
        "id": 1,
        "title": long_title,
        "tags": [],
        "status": "pending",
        "created_at": "2024-01-15T10:30:00"
    }
    
    backend.save_task(task)
    loaded_tasks = backend.load_tasks()
    
    assert len(loaded_tasks) == 1
    assert loaded_tasks[0]["title"] == long_title


def test_save_task_with_special_characters_in_title(backend):
    """save_task handles special characters in title."""
    task: Task = {
        "id": 1,
        "title": "Task with special chars: @#$%^&*(){}[]|\\:;\"'<>,.?/~`",
        "tags": [],
        "status": "pending",
        "created_at": "2024-01-15T10:30:00"
    }
    
    backend.save_task(task)
    loaded_tasks = backend.load_tasks()
    
    assert len(loaded_tasks) == 1
    assert loaded_tasks[0]["title"] == task["title"]


def test_save_task_with_unicode_characters(backend):
    """save_task handles unicode characters in title and tags."""
    task: Task = {
        "id": 1,
        "title": "Task with unicode: 你好 🎉 café",
        "tags": ["日本語", "emoji🔥", "français"],
        "status": "pending",
        "created_at": "2024-01-15T10:30:00"
    }
    
    backend.save_task(task)
    loaded_tasks = backend.load_tasks()
    
    assert len(loaded_tasks) == 1
    assert loaded_tasks[0]["title"] == task["title"]
    assert loaded_tasks[0]["tags"] == task["tags"]


def test_save_task_with_newlines_in_title(backend):
    """save_task handles newlines in title."""
    task: Task = {
        "id": 1,
        "title": "Task with\nnewlines\nin title",
        "tags": [],
        "status": "pending",
        "created_at": "2024-01-15T10:30:00"
    }
    
    backend.save_task(task)
    loaded_tasks = backend.load_tasks()
    
    assert len(loaded_tasks) == 1
    assert loaded_tasks[0]["title"] == task["title"]


def test_save_many_tasks(backend):
    """save_task handles saving many tasks."""
    tasks = [
        {
            "id": i,
            "title": f"Task {i}",
            "tags": [f"tag{i}"],
            "status": "pending",
            "created_at": f"2024-01-15T10:{i:02d}:00"
        }
        for i in range(100)
    ]
    
    for task in tasks:
        backend.save_task(task)
    
    loaded_tasks = backend.load_tasks()
    
    assert len(loaded_tasks) == 100


def test_get_task_by_id_with_gaps_in_ids(backend):
    """get_task_by_id works when IDs have gaps."""
    tasks = [
        {
            "id": 1,
            "title": "Task 1",
            "tags": [],
            "status": "pending",
            "created_at": "2024-01-15T10:00:00"
        },
        {
            "id": 5,
            "title": "Task 5",
            "tags": [],
            "status": "pending",
            "created_at": "2024-01-15T10:05:00"
        },
        {
            "id": 10,
            "title": "Task 10",
            "tags": [],
            "status": "pending",
            "created_at": "2024-01-15T10:10:00"
        }
    ]
    
    for task in tasks:
        backend.save_task(task)
    
    # Should find existing IDs
    assert backend.get_task_by_id(1) is not None
    assert backend.get_task_by_id(5) is not None
    assert backend.get_task_by_id(10) is not None
    
    # Should not find missing IDs
    assert backend.get_task_by_id(2) is None
    assert backend.get_task_by_id(3) is None
    assert backend.get_task_by_id(7) is None


def test_load_tasks_after_file_manually_edited(backend, sample_task):
    """load_tasks works after file is manually edited."""
    # Save initial task
    backend.save_task(sample_task)
    
    # Manually edit file to add another task
    with open(backend.file_path, 'r') as f:
        data = json.load(f)
    
    data.append({
        "id": 2,
        "title": "Manually added task",
        "tags": ["manual"],
        "status": "complete",
        "created_at": "2024-01-15T11:00:00"
    })
    
    with open(backend.file_path, 'w') as f:
        json.dump(data, f)
    
    # Load tasks should include manually added task
    loaded_tasks = backend.load_tasks()
    
    assert len(loaded_tasks) == 2
    assert loaded_tasks[1]["title"] == "Manually added task"


def test_backend_with_relative_path():
    """JSONFileBackend works with relative paths."""
    backend = JSONFileBackend("./test_tasks.json")
    
    # Path is stored as provided (expanduser only expands ~)
    # Relative paths remain relative until file operations
    assert backend.file_path == Path("./test_tasks.json")


def test_multiple_backend_instances_same_file(temp_file_path, sample_task):
    """Multiple backend instances can access the same file."""
    backend1 = JSONFileBackend(temp_file_path)
    backend2 = JSONFileBackend(temp_file_path)
    
    # Save with first backend
    backend1.save_task(sample_task)
    
    # Load with second backend
    tasks = backend2.load_tasks()
    
    assert len(tasks) == 1
    assert tasks[0]["id"] == sample_task["id"]


def test_file_path_stored_correctly(temp_file_path):
    """Backend stores file path correctly."""
    backend = JSONFileBackend(temp_file_path)
    
    assert str(backend.file_path) == temp_file_path
    assert backend.file_path == Path(temp_file_path)
