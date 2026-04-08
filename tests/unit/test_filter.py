"""Unit tests for TaskFilter."""

import pytest
from task_tracker.filter import TaskFilter
from task_tracker.models import Task


@pytest.fixture
def task_filter():
    """Create a TaskFilter instance."""
    return TaskFilter()


@pytest.fixture
def sample_tasks():
    """Create sample tasks for testing."""
    return [
        Task(
            id=1,
            title="Write documentation",
            tags=["docs", "urgent"],
            status="pending",
            created_at="2024-01-15T10:00:00"
        ),
        Task(
            id=2,
            title="Fix bug",
            tags=["bug", "urgent"],
            status="complete",
            created_at="2024-01-15T11:00:00"
        ),
        Task(
            id=3,
            title="Review code",
            tags=["review"],
            status="pending",
            created_at="2024-01-15T12:00:00"
        ),
        Task(
            id=4,
            title="Deploy application",
            tags=["devops", "urgent"],
            status="complete",
            created_at="2024-01-15T13:00:00"
        ),
        Task(
            id=5,
            title="Update dependencies",
            tags=["maintenance"],
            status="pending",
            created_at="2024-01-15T14:00:00"
        ),
    ]


# Filter by status tests

def test_filter_by_status_pending(task_filter, sample_tasks):
    """Test filtering tasks by pending status."""
    result = task_filter.filter_by_status(sample_tasks, "pending")
    assert len(result) == 3
    assert all(task["status"] == "pending" for task in result)
    assert result[0]["id"] == 1
    assert result[1]["id"] == 3
    assert result[2]["id"] == 5


def test_filter_by_status_complete(task_filter, sample_tasks):
    """Test filtering tasks by complete status."""
    result = task_filter.filter_by_status(sample_tasks, "complete")
    assert len(result) == 2
    assert all(task["status"] == "complete" for task in result)
    assert result[0]["id"] == 2
    assert result[1]["id"] == 4


def test_filter_by_status_no_matches(task_filter, sample_tasks):
    """Test filtering by status with no matches."""
    result = task_filter.filter_by_status(sample_tasks, "archived")
    assert len(result) == 0
    assert result == []


def test_filter_by_status_empty_list(task_filter):
    """Test filtering empty task list by status."""
    result = task_filter.filter_by_status([], "pending")
    assert len(result) == 0
    assert result == []


# Filter by tags tests

def test_filter_by_tags_single_tag(task_filter, sample_tasks):
    """Test filtering tasks by a single tag."""
    result = task_filter.filter_by_tags(sample_tasks, ["urgent"])
    assert len(result) == 3
    assert all("urgent" in task["tags"] for task in result)
    assert result[0]["id"] == 1
    assert result[1]["id"] == 2
    assert result[2]["id"] == 4


def test_filter_by_tags_multiple_tags(task_filter, sample_tasks):
    """Test filtering tasks by multiple tags (tasks must have all tags)."""
    result = task_filter.filter_by_tags(sample_tasks, ["docs", "urgent"])
    assert len(result) == 1
    assert result[0]["id"] == 1
    assert "docs" in result[0]["tags"]
    assert "urgent" in result[0]["tags"]


def test_filter_by_tags_no_matches(task_filter, sample_tasks):
    """Test filtering by tags with no matches."""
    result = task_filter.filter_by_tags(sample_tasks, ["nonexistent"])
    assert len(result) == 0
    assert result == []


def test_filter_by_tags_empty_list(task_filter):
    """Test filtering empty task list by tags."""
    result = task_filter.filter_by_tags([], ["urgent"])
    assert len(result) == 0
    assert result == []


def test_filter_by_tags_empty_tag_list(task_filter, sample_tasks):
    """Test filtering with empty tag list."""
    result = task_filter.filter_by_tags(sample_tasks, [])
    # Empty tag list should return all tasks (no filter applied)
    assert len(result) == 5


# Filter by ID tests

def test_filter_by_id_found(task_filter, sample_tasks):
    """Test filtering task by ID when task exists."""
    result = task_filter.filter_by_id(sample_tasks, 3)
    assert result is not None
    assert result["id"] == 3
    assert result["title"] == "Review code"


def test_filter_by_id_not_found(task_filter, sample_tasks):
    """Test filtering task by ID when task does not exist."""
    result = task_filter.filter_by_id(sample_tasks, 999)
    assert result is None


def test_filter_by_id_empty_list(task_filter):
    """Test filtering by ID in empty task list."""
    result = task_filter.filter_by_id([], 1)
    assert result is None


def test_filter_by_id_first_task(task_filter, sample_tasks):
    """Test filtering by ID for first task."""
    result = task_filter.filter_by_id(sample_tasks, 1)
    assert result is not None
    assert result["id"] == 1


def test_filter_by_id_last_task(task_filter, sample_tasks):
    """Test filtering by ID for last task."""
    result = task_filter.filter_by_id(sample_tasks, 5)
    assert result is not None
    assert result["id"] == 5


# Multiple filters (combining filters)

def test_multiple_filters_status_then_tags(task_filter, sample_tasks):
    """Test applying multiple filters in sequence."""
    # First filter by status
    pending_tasks = task_filter.filter_by_status(sample_tasks, "pending")
    # Then filter by tags
    result = task_filter.filter_by_tags(pending_tasks, ["urgent"])
    assert len(result) == 1
    assert result[0]["id"] == 1
    assert result[0]["status"] == "pending"
    assert "urgent" in result[0]["tags"]


def test_multiple_filters_tags_then_status(task_filter, sample_tasks):
    """Test applying filters in different order."""
    # First filter by tags
    urgent_tasks = task_filter.filter_by_tags(sample_tasks, ["urgent"])
    # Then filter by status
    result = task_filter.filter_by_status(urgent_tasks, "complete")
    assert len(result) == 2
    assert result[0]["id"] == 2
    assert result[1]["id"] == 4


def test_multiple_filters_no_results(task_filter, sample_tasks):
    """Test multiple filters that result in no matches."""
    # Filter by status
    complete_tasks = task_filter.filter_by_status(sample_tasks, "complete")
    # Filter by tag that doesn't exist in complete tasks
    result = task_filter.filter_by_tags(complete_tasks, ["docs"])
    assert len(result) == 0


# Edge cases

def test_filter_preserves_task_order(task_filter, sample_tasks):
    """Test that filtering preserves original task order."""
    result = task_filter.filter_by_status(sample_tasks, "pending")
    # IDs should be in ascending order (original order)
    assert result[0]["id"] < result[1]["id"] < result[2]["id"]


def test_filter_does_not_modify_original_list(task_filter, sample_tasks):
    """Test that filtering does not modify the original task list."""
    original_length = len(sample_tasks)
    original_first_id = sample_tasks[0]["id"]
    
    task_filter.filter_by_status(sample_tasks, "pending")
    
    assert len(sample_tasks) == original_length
    assert sample_tasks[0]["id"] == original_first_id


def test_filter_by_status_case_sensitive(task_filter, sample_tasks):
    """Test that status filtering is case-sensitive."""
    result = task_filter.filter_by_status(sample_tasks, "Pending")
    # Should not match "pending" (case mismatch)
    assert len(result) == 0


def test_filter_by_tags_case_sensitive(task_filter, sample_tasks):
    """Test that tag filtering is case-sensitive."""
    result = task_filter.filter_by_tags(sample_tasks, ["Urgent"])
    # Should not match "urgent" (case mismatch)
    assert len(result) == 0


def test_filter_with_special_characters_in_tags(task_filter):
    """Test filtering tasks with special characters in tags."""
    tasks_with_special_chars = [
        Task(
            id=1,
            title="Task 1",
            tags=["tag-with-dash", "tag_with_underscore"],
            status="pending",
            created_at="2024-01-15T10:00:00"
        ),
        Task(
            id=2,
            title="Task 2",
            tags=["tag.with.dots"],
            status="pending",
            created_at="2024-01-15T11:00:00"
        ),
    ]
    
    result = task_filter.filter_by_tags(tasks_with_special_chars, ["tag-with-dash"])
    assert len(result) == 1
    assert result[0]["id"] == 1


def test_filter_with_unicode_in_tags(task_filter):
    """Test filtering tasks with unicode characters in tags."""
    tasks_with_unicode = [
        Task(
            id=1,
            title="Task 1",
            tags=["🚀", "emoji"],
            status="pending",
            created_at="2024-01-15T10:00:00"
        ),
        Task(
            id=2,
            title="Task 2",
            tags=["日本語", "unicode"],
            status="pending",
            created_at="2024-01-15T11:00:00"
        ),
    ]
    
    result = task_filter.filter_by_tags(tasks_with_unicode, ["🚀"])
    assert len(result) == 1
    assert result[0]["id"] == 1


def test_filter_by_tags_with_many_tags(task_filter):
    """Test filtering task with many tags."""
    task_with_many_tags = [
        Task(
            id=1,
            title="Task with many tags",
            tags=[f"tag{i}" for i in range(100)],
            status="pending",
            created_at="2024-01-15T10:00:00"
        ),
    ]
    
    result = task_filter.filter_by_tags(task_with_many_tags, ["tag50"])
    assert len(result) == 1
    assert "tag50" in result[0]["tags"]


def test_filter_by_id_with_zero(task_filter, sample_tasks):
    """Test filtering by ID with zero (invalid ID)."""
    result = task_filter.filter_by_id(sample_tasks, 0)
    assert result is None


def test_filter_by_id_with_negative(task_filter, sample_tasks):
    """Test filtering by ID with negative number."""
    result = task_filter.filter_by_id(sample_tasks, -1)
    assert result is None
