"""Unit tests for TaskFormatter.

Tests cover:
- Format single task
- Format task list
- Format empty list
- Edge cases: long titles, many tags, special characters
- Requirements: 5.2

All tests will FAIL until implementation is complete (RED state).
"""

import pytest
from src.task_tracker.formatter import TaskFormatter
from src.task_tracker.models import Task


# ===== Fixture =====

@pytest.fixture
def formatter():
    """Create a TaskFormatter instance for testing."""
    return TaskFormatter()


@pytest.fixture
def sample_task() -> Task:
    """Create a sample task for testing."""
    return {
        "id": 1,
        "title": "Write documentation",
        "tags": ["docs", "urgent"],
        "status": "pending",
        "created_at": "2024-01-15T10:30:00.123456"
    }


@pytest.fixture
def completed_task() -> Task:
    """Create a completed task for testing."""
    return {
        "id": 2,
        "title": "Fix authentication bug",
        "tags": ["bug", "security"],
        "status": "complete",
        "created_at": "2024-01-15T09:00:00.000000"
    }


# ===== Format Single Task Tests (Requirement 5.2) =====

def test_format_task_returns_string(formatter, sample_task):
    """format_task returns a string."""
    result = formatter.format_task(sample_task)
    assert isinstance(result, str)


def test_format_task_includes_task_id(formatter, sample_task):
    """Formatted task includes task ID."""
    result = formatter.format_task(sample_task)
    assert "1" in result


def test_format_task_includes_title(formatter, sample_task):
    """Formatted task includes task title."""
    result = formatter.format_task(sample_task)
    assert "Write documentation" in result


def test_format_task_includes_status(formatter, sample_task):
    """Formatted task includes task status."""
    result = formatter.format_task(sample_task)
    assert "pending" in result


def test_format_task_includes_tags(formatter, sample_task):
    """Formatted task includes all tags."""
    result = formatter.format_task(sample_task)
    assert "docs" in result
    assert "urgent" in result


def test_format_task_includes_timestamp(formatter, sample_task):
    """Formatted task includes creation timestamp."""
    result = formatter.format_task(sample_task)
    assert "2024-01-15" in result


def test_format_task_with_no_tags(formatter):
    """format_task handles task with empty tags list."""
    task: Task = {
        "id": 3,
        "title": "Task without tags",
        "tags": [],
        "status": "pending",
        "created_at": "2024-01-15T10:30:00.123456"
    }
    
    result = formatter.format_task(task)
    assert isinstance(result, str)
    assert "Task without tags" in result


def test_format_task_with_completed_status(formatter, completed_task):
    """format_task handles completed tasks."""
    result = formatter.format_task(completed_task)
    assert "complete" in result
    assert "Fix authentication bug" in result


# ===== Format Task List Tests (Requirement 5.2) =====

def test_format_task_list_returns_string(formatter, sample_task, completed_task):
    """format_task_list returns a string."""
    tasks = [sample_task, completed_task]
    result = formatter.format_task_list(tasks)
    assert isinstance(result, str)


def test_format_task_list_includes_all_tasks(formatter, sample_task, completed_task):
    """format_task_list includes all tasks in the list."""
    tasks = [sample_task, completed_task]
    result = formatter.format_task_list(tasks)
    
    assert "Write documentation" in result
    assert "Fix authentication bug" in result


def test_format_task_list_with_single_task(formatter, sample_task):
    """format_task_list handles list with single task."""
    tasks = [sample_task]
    result = formatter.format_task_list(tasks)
    
    assert isinstance(result, str)
    assert "Write documentation" in result


def test_format_task_list_with_multiple_tasks(formatter):
    """format_task_list handles list with multiple tasks."""
    tasks = [
        {
            "id": 1,
            "title": "First task",
            "tags": ["tag1"],
            "status": "pending",
            "created_at": "2024-01-15T10:00:00.000000"
        },
        {
            "id": 2,
            "title": "Second task",
            "tags": ["tag2"],
            "status": "complete",
            "created_at": "2024-01-15T11:00:00.000000"
        },
        {
            "id": 3,
            "title": "Third task",
            "tags": ["tag3"],
            "status": "pending",
            "created_at": "2024-01-15T12:00:00.000000"
        }
    ]
    
    result = formatter.format_task_list(tasks)
    assert "First task" in result
    assert "Second task" in result
    assert "Third task" in result


def test_format_task_list_preserves_order(formatter):
    """format_task_list preserves task order."""
    tasks = [
        {
            "id": 5,
            "title": "Task A",
            "tags": [],
            "status": "pending",
            "created_at": "2024-01-15T10:00:00.000000"
        },
        {
            "id": 3,
            "title": "Task B",
            "tags": [],
            "status": "pending",
            "created_at": "2024-01-15T11:00:00.000000"
        },
        {
            "id": 7,
            "title": "Task C",
            "tags": [],
            "status": "pending",
            "created_at": "2024-01-15T12:00:00.000000"
        }
    ]
    
    result = formatter.format_task_list(tasks)
    
    # Check that tasks appear in the order they were provided
    pos_a = result.find("Task A")
    pos_b = result.find("Task B")
    pos_c = result.find("Task C")
    
    assert pos_a < pos_b < pos_c


def test_format_task_list_with_ten_tasks(formatter):
    """format_task_list handles list with 10 tasks."""
    tasks = [
        {
            "id": i,
            "title": f"Task {i}",
            "tags": [f"tag{i}"],
            "status": "pending",
            "created_at": f"2024-01-15T{10+i:02d}:00:00.000000"
        }
        for i in range(1, 11)
    ]
    
    result = formatter.format_task_list(tasks)
    
    # Verify all tasks are included
    for i in range(1, 11):
        assert f"Task {i}" in result


# ===== Format Empty List Tests (Requirement 5.2) =====

def test_format_empty_list_returns_string(formatter):
    """format_empty_list returns a string."""
    result = formatter.format_empty_list()
    assert isinstance(result, str)


def test_format_empty_list_returns_non_empty_message(formatter):
    """format_empty_list returns a non-empty message."""
    result = formatter.format_empty_list()
    assert len(result) > 0


def test_format_empty_list_indicates_no_tasks(formatter):
    """format_empty_list message indicates no tasks exist."""
    result = formatter.format_empty_list()
    # Message should indicate emptiness (common phrases)
    assert any(phrase in result.lower() for phrase in [
        "no tasks",
        "empty",
        "0 tasks",
        "nothing",
        "none"
    ])


# ===== Edge Cases: Long Titles =====

def test_format_task_with_very_long_title(formatter):
    """format_task handles task with very long title (1000+ characters)."""
    long_title = "A" * 1000
    task: Task = {
        "id": 1,
        "title": long_title,
        "tags": ["test"],
        "status": "pending",
        "created_at": "2024-01-15T10:30:00.123456"
    }
    
    result = formatter.format_task(task)
    assert isinstance(result, str)
    # Title should be present (may be truncated, but that's implementation detail)
    assert "A" in result


def test_format_task_list_with_long_titles(formatter):
    """format_task_list handles tasks with very long titles."""
    tasks = [
        {
            "id": 1,
            "title": "A" * 500,
            "tags": [],
            "status": "pending",
            "created_at": "2024-01-15T10:00:00.000000"
        },
        {
            "id": 2,
            "title": "B" * 500,
            "tags": [],
            "status": "pending",
            "created_at": "2024-01-15T11:00:00.000000"
        }
    ]
    
    result = formatter.format_task_list(tasks)
    assert isinstance(result, str)


# ===== Edge Cases: Many Tags =====

def test_format_task_with_many_tags(formatter):
    """format_task handles task with many tags (100+)."""
    many_tags = [f"tag{i}" for i in range(100)]
    task: Task = {
        "id": 1,
        "title": "Task with many tags",
        "tags": many_tags,
        "status": "pending",
        "created_at": "2024-01-15T10:30:00.123456"
    }
    
    result = formatter.format_task(task)
    assert isinstance(result, str)
    # At least some tags should be present
    assert "tag0" in result or "tag" in result


def test_format_task_list_with_many_tags_per_task(formatter):
    """format_task_list handles tasks with many tags each."""
    tasks = [
        {
            "id": 1,
            "title": "Task 1",
            "tags": [f"tag1_{i}" for i in range(50)],
            "status": "pending",
            "created_at": "2024-01-15T10:00:00.000000"
        },
        {
            "id": 2,
            "title": "Task 2",
            "tags": [f"tag2_{i}" for i in range(50)],
            "status": "pending",
            "created_at": "2024-01-15T11:00:00.000000"
        }
    ]
    
    result = formatter.format_task_list(tasks)
    assert isinstance(result, str)


# ===== Edge Cases: Special Characters =====

def test_format_task_with_unicode_title(formatter):
    """format_task handles task with unicode characters in title."""
    task: Task = {
        "id": 1,
        "title": "Tâche importante 📝 任务 Задача",
        "tags": ["unicode"],
        "status": "pending",
        "created_at": "2024-01-15T10:30:00.123456"
    }
    
    result = formatter.format_task(task)
    assert isinstance(result, str)
    assert "Tâche" in result or "任务" in result or "Задача" in result


def test_format_task_with_special_characters_in_title(formatter):
    """format_task handles task with special characters in title."""
    task: Task = {
        "id": 1,
        "title": "Fix bug: API returns 500 error! @urgent #critical",
        "tags": ["bug"],
        "status": "pending",
        "created_at": "2024-01-15T10:30:00.123456"
    }
    
    result = formatter.format_task(task)
    assert isinstance(result, str)
    assert "Fix bug" in result


def test_format_task_with_unicode_tags(formatter):
    """format_task handles task with unicode tags."""
    task: Task = {
        "id": 1,
        "title": "Unicode task",
        "tags": ["重要", "срочно", "🔥"],
        "status": "pending",
        "created_at": "2024-01-15T10:30:00.123456"
    }
    
    result = formatter.format_task(task)
    assert isinstance(result, str)


def test_format_task_with_special_characters_in_tags(formatter):
    """format_task handles task with special characters in tags."""
    task: Task = {
        "id": 1,
        "title": "Special tags task",
        "tags": ["@urgent", "#bug", "v2.0", "API-500"],
        "status": "pending",
        "created_at": "2024-01-15T10:30:00.123456"
    }
    
    result = formatter.format_task(task)
    assert isinstance(result, str)


def test_format_task_with_newline_in_title(formatter):
    """format_task handles task with newline in title."""
    task: Task = {
        "id": 1,
        "title": "First line\nSecond line",
        "tags": ["multiline"],
        "status": "pending",
        "created_at": "2024-01-15T10:30:00.123456"
    }
    
    result = formatter.format_task(task)
    assert isinstance(result, str)


def test_format_task_with_quotes_in_title(formatter):
    """format_task handles task with quotes in title."""
    task: Task = {
        "id": 1,
        "title": 'Update "config.json" file',
        "tags": ["config"],
        "status": "pending",
        "created_at": "2024-01-15T10:30:00.123456"
    }
    
    result = formatter.format_task(task)
    assert isinstance(result, str)
    assert "config" in result.lower()


def test_format_task_list_with_mixed_special_characters(formatter):
    """format_task_list handles tasks with various special characters."""
    tasks = [
        {
            "id": 1,
            "title": "Task with emoji 🎉",
            "tags": ["🔥"],
            "status": "pending",
            "created_at": "2024-01-15T10:00:00.000000"
        },
        {
            "id": 2,
            "title": "Task with symbols: @#$%",
            "tags": ["@urgent"],
            "status": "complete",
            "created_at": "2024-01-15T11:00:00.000000"
        },
        {
            "id": 3,
            "title": "Task with unicode: 你好",
            "tags": ["中文"],
            "status": "pending",
            "created_at": "2024-01-15T12:00:00.000000"
        }
    ]
    
    result = formatter.format_task_list(tasks)
    assert isinstance(result, str)


# ===== Edge Cases: Boundary Conditions =====

def test_format_task_with_id_zero(formatter):
    """format_task handles task with ID 0 (edge case, may be invalid)."""
    task: Task = {
        "id": 0,
        "title": "Task with zero ID",
        "tags": [],
        "status": "pending",
        "created_at": "2024-01-15T10:30:00.123456"
    }
    
    result = formatter.format_task(task)
    assert isinstance(result, str)


def test_format_task_with_large_id(formatter):
    """format_task handles task with very large ID."""
    task: Task = {
        "id": 999999999,
        "title": "Task with large ID",
        "tags": [],
        "status": "pending",
        "created_at": "2024-01-15T10:30:00.123456"
    }
    
    result = formatter.format_task(task)
    assert isinstance(result, str)
    assert "999999999" in result


def test_format_task_with_minimal_timestamp(formatter):
    """format_task handles task with minimal ISO timestamp."""
    task: Task = {
        "id": 1,
        "title": "Minimal timestamp",
        "tags": [],
        "status": "pending",
        "created_at": "2024-01-01T00:00:00"
    }
    
    result = formatter.format_task(task)
    assert isinstance(result, str)


def test_format_task_with_timezone_in_timestamp(formatter):
    """format_task handles task with timezone in timestamp."""
    task: Task = {
        "id": 1,
        "title": "Timezone task",
        "tags": [],
        "status": "pending",
        "created_at": "2024-01-15T10:30:00.123456+00:00"
    }
    
    result = formatter.format_task(task)
    assert isinstance(result, str)


def test_format_task_list_with_hundred_tasks(formatter):
    """format_task_list handles list with 100 tasks."""
    tasks = [
        {
            "id": i,
            "title": f"Task {i}",
            "tags": [],
            "status": "pending",
            "created_at": "2024-01-15T10:00:00.000000"
        }
        for i in range(1, 101)
    ]
    
    result = formatter.format_task_list(tasks)
    assert isinstance(result, str)
    # Verify first and last tasks are included
    assert "Task 1" in result
    assert "Task 100" in result
