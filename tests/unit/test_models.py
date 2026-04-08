"""Unit tests for Task model and validation functions.

Tests cover:
- Task structure validation
- Field type validation
- Default values
- Edge cases: empty title, invalid status, special characters, unicode
- Requirements: 4.1-4.5

All tests will FAIL until implementation is complete (RED state).
"""

import pytest
from datetime import datetime
from src.task_tracker.models import (
    Task,
    validate_title,
    validate_status,
    validate_task_id,
    validate_timestamp,
)


# ===== Task Structure Tests =====

def test_task_has_required_fields():
    """Task structure includes all required fields."""
    task: Task = {
        "id": 1,
        "title": "Test task",
        "tags": ["test"],
        "status": "pending",
        "created_at": "2024-01-15T10:30:00.123456"
    }
    
    assert "id" in task
    assert "title" in task
    assert "tags" in task
    assert "status" in task
    assert "created_at" in task


def test_task_field_types():
    """Task fields have correct types."""
    task: Task = {
        "id": 1,
        "title": "Test task",
        "tags": ["test", "example"],
        "status": "pending",
        "created_at": "2024-01-15T10:30:00.123456"
    }
    
    assert isinstance(task["id"], int)
    assert isinstance(task["title"], str)
    assert isinstance(task["tags"], list)
    assert all(isinstance(tag, str) for tag in task["tags"])
    assert isinstance(task["status"], str)
    assert isinstance(task["created_at"], str)


# ===== Title Validation Tests (Requirement 4.1) =====

def test_validate_title_accepts_valid_title():
    """Valid title passes validation."""
    validate_title("Write documentation")
    validate_title("Fix bug #123")
    validate_title("Deploy to production")


def test_validate_title_rejects_empty_string():
    """Empty title raises ValueError with specific message."""
    with pytest.raises(ValueError) as exc_info:
        validate_title("")
    
    assert "Title cannot be empty" in str(exc_info.value)


def test_validate_title_rejects_whitespace_only():
    """Whitespace-only title raises ValueError."""
    with pytest.raises(ValueError) as exc_info:
        validate_title("   ")
    
    assert "Title cannot be empty" in str(exc_info.value)


def test_validate_title_rejects_tabs_and_newlines():
    """Title with only tabs and newlines raises ValueError."""
    with pytest.raises(ValueError):
        validate_title("\t\n\r")


def test_validate_title_accepts_unicode_characters():
    """Title with unicode characters passes validation."""
    validate_title("Tâche importante 📝")
    validate_title("任务管理")
    validate_title("Задача")


def test_validate_title_accepts_special_characters():
    """Title with special characters passes validation."""
    validate_title("Fix bug: API returns 500 error!")
    validate_title("Update README.md (v2.0)")
    validate_title("Task #42 - @mention & review")


def test_validate_title_accepts_very_long_title():
    """Very long title (1000+ characters) passes validation."""
    long_title = "A" * 1000
    validate_title(long_title)


def test_validate_title_accepts_title_with_leading_trailing_spaces():
    """Title with leading/trailing spaces passes validation (will be trimmed by caller)."""
    validate_title("  Task with spaces  ")


# ===== Status Validation Tests (Requirement 4.2) =====

def test_validate_status_accepts_pending():
    """Status 'pending' passes validation."""
    validate_status("pending")


def test_validate_status_accepts_complete():
    """Status 'complete' passes validation."""
    validate_status("complete")


def test_validate_status_rejects_invalid_status():
    """Invalid status raises ValueError with list of valid values."""
    with pytest.raises(ValueError) as exc_info:
        validate_status("in-progress")
    
    error_message = str(exc_info.value)
    assert "pending" in error_message
    assert "complete" in error_message


def test_validate_status_rejects_empty_string():
    """Empty status raises ValueError."""
    with pytest.raises(ValueError):
        validate_status("")


def test_validate_status_rejects_none():
    """None status raises ValueError."""
    with pytest.raises((ValueError, TypeError)):
        validate_status(None)


def test_validate_status_is_case_sensitive():
    """Status validation is case-sensitive."""
    with pytest.raises(ValueError):
        validate_status("Pending")
    
    with pytest.raises(ValueError):
        validate_status("COMPLETE")


def test_validate_status_rejects_common_invalid_values():
    """Common invalid status values raise ValueError."""
    invalid_statuses = [
        "in-progress",
        "todo",
        "done",
        "started",
        "blocked",
        "cancelled"
    ]
    
    for status in invalid_statuses:
        with pytest.raises(ValueError):
            validate_status(status)


# ===== Task ID Validation Tests (Requirement 4.4) =====

def test_validate_task_id_accepts_positive_integers():
    """Positive integer IDs pass validation."""
    validate_task_id(1)
    validate_task_id(42)
    validate_task_id(999999)


def test_validate_task_id_rejects_zero():
    """Task ID of 0 raises ValueError."""
    with pytest.raises(ValueError) as exc_info:
        validate_task_id(0)
    
    assert "positive integer" in str(exc_info.value).lower()


def test_validate_task_id_rejects_negative_integers():
    """Negative task IDs raise ValueError."""
    with pytest.raises(ValueError) as exc_info:
        validate_task_id(-1)
    
    assert "positive integer" in str(exc_info.value).lower()


def test_validate_task_id_rejects_negative_large_number():
    """Large negative task ID raises ValueError."""
    with pytest.raises(ValueError):
        validate_task_id(-999)


def test_validate_task_id_rejects_none():
    """None task ID raises ValueError or TypeError."""
    with pytest.raises((ValueError, TypeError)):
        validate_task_id(None)


# ===== Timestamp Validation Tests (Requirement 4.5) =====

def test_validate_timestamp_accepts_valid_iso_format():
    """Valid ISO format timestamps pass validation."""
    validate_timestamp("2024-01-15T10:30:00.123456")
    validate_timestamp("2024-12-31T23:59:59.999999")
    validate_timestamp("2024-01-01T00:00:00.000000")


def test_validate_timestamp_accepts_iso_format_with_timezone():
    """ISO format with timezone passes validation."""
    validate_timestamp("2024-01-15T10:30:00.123456+00:00")
    validate_timestamp("2024-01-15T10:30:00.123456Z")
    validate_timestamp("2024-01-15T10:30:00.123456-05:00")


def test_validate_timestamp_accepts_iso_format_without_microseconds():
    """ISO format without microseconds passes validation."""
    validate_timestamp("2024-01-15T10:30:00")


def test_validate_timestamp_rejects_invalid_format():
    """Invalid timestamp format raises ValueError."""
    with pytest.raises(ValueError):
        validate_timestamp("2024-01-15 10:30:00")  # Space instead of T


def test_validate_timestamp_rejects_date_only():
    """Date-only string raises ValueError."""
    with pytest.raises(ValueError):
        validate_timestamp("2024-01-15")


def test_validate_timestamp_rejects_time_only():
    """Time-only string raises ValueError."""
    with pytest.raises(ValueError):
        validate_timestamp("10:30:00")


def test_validate_timestamp_rejects_empty_string():
    """Empty timestamp raises ValueError."""
    with pytest.raises(ValueError):
        validate_timestamp("")


def test_validate_timestamp_rejects_none():
    """None timestamp raises ValueError or TypeError."""
    with pytest.raises((ValueError, TypeError)):
        validate_timestamp(None)


def test_validate_timestamp_rejects_invalid_date():
    """Invalid date in timestamp raises ValueError."""
    with pytest.raises(ValueError):
        validate_timestamp("2024-13-01T10:30:00")  # Month 13


def test_validate_timestamp_rejects_invalid_time():
    """Invalid time in timestamp raises ValueError."""
    with pytest.raises(ValueError):
        validate_timestamp("2024-01-15T25:00:00")  # Hour 25


# ===== Edge Cases =====

def test_task_with_empty_tags_list():
    """Task with empty tags list is valid."""
    task: Task = {
        "id": 1,
        "title": "Task without tags",
        "tags": [],
        "status": "pending",
        "created_at": "2024-01-15T10:30:00.123456"
    }
    
    assert task["tags"] == []


def test_task_with_many_tags():
    """Task with many tags (100+) is valid."""
    many_tags = [f"tag{i}" for i in range(100)]
    task: Task = {
        "id": 1,
        "title": "Task with many tags",
        "tags": many_tags,
        "status": "pending",
        "created_at": "2024-01-15T10:30:00.123456"
    }
    
    assert len(task["tags"]) == 100


def test_task_with_unicode_tags():
    """Task with unicode tags is valid."""
    task: Task = {
        "id": 1,
        "title": "Unicode task",
        "tags": ["重要", "срочно", "🔥"],
        "status": "pending",
        "created_at": "2024-01-15T10:30:00.123456"
    }
    
    assert "重要" in task["tags"]
    assert "срочно" in task["tags"]
    assert "🔥" in task["tags"]


def test_task_with_special_characters_in_tags():
    """Task with special characters in tags is valid."""
    task: Task = {
        "id": 1,
        "title": "Special tags",
        "tags": ["@urgent", "#bug", "v2.0", "API-500"],
        "status": "pending",
        "created_at": "2024-01-15T10:30:00.123456"
    }
    
    assert "@urgent" in task["tags"]
    assert "#bug" in task["tags"]


def test_task_with_large_id():
    """Task with very large ID is valid."""
    task: Task = {
        "id": 999999999,
        "title": "Large ID task",
        "tags": [],
        "status": "pending",
        "created_at": "2024-01-15T10:30:00.123456"
    }
    
    assert task["id"] == 999999999


def test_validate_title_with_newline_in_middle():
    """Title with newline in middle passes validation (caller decides handling)."""
    validate_title("First line\nSecond line")


def test_validate_title_with_emoji():
    """Title with emoji passes validation."""
    validate_title("Fix bug 🐛 in authentication 🔐")


def test_validate_status_with_whitespace():
    """Status with whitespace raises ValueError."""
    with pytest.raises(ValueError):
        validate_status(" pending ")
    
    with pytest.raises(ValueError):
        validate_status("pending ")


def test_validate_timestamp_current_time():
    """Current timestamp in ISO format passes validation."""
    current_time = datetime.now().isoformat()
    validate_timestamp(current_time)
