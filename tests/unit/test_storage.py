"""Unit tests for TaskStore module."""

import pytest
from datetime import datetime
from typing import List, Optional
from task_tracker.models import Task
from task_tracker.storage import StorageBackend
from task_tracker.store import TaskStore


class FakeBackend:
    """Fake storage backend for testing TaskStore in isolation."""
    
    def __init__(self):
        self.tasks: List[Task] = []
    
    def save_task(self, task: Task) -> None:
        """Save a task to in-memory storage."""
        self.tasks.append(task)
    
    def load_tasks(self) -> List[Task]:
        """Load all tasks from in-memory storage."""
        return self.tasks.copy()
    
    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Get a task by ID from in-memory storage."""
        for task in self.tasks:
            if task["id"] == task_id:
                return task
        return None


# Requirement 1.1: Create task with title
def test_create_task_with_title():
    """WHEN a user provides a title, THE CLI SHALL create a task with that title."""
    backend = FakeBackend()
    store = TaskStore(backend)
    
    task = store.create_task("Write documentation")
    
    assert task["title"] == "Write documentation"


# Requirement 1.2: Create task with tags
def test_create_task_with_tags():
    """WHEN a user provides tags, THE CLI SHALL create a task with those tags."""
    backend = FakeBackend()
    store = TaskStore(backend)
    
    task = store.create_task("Deploy application", tags=["urgent", "devops"])
    
    assert task["tags"] == ["urgent", "devops"]


# Requirement 1.3: Create task with status
def test_create_task_with_status():
    """WHEN a user provides a status, THE CLI SHALL create a task with that status."""
    backend = FakeBackend()
    store = TaskStore(backend)
    
    task = store.create_task("Review code", status="complete")
    
    assert task["status"] == "complete"


# Requirement 1.4: Default status is pending
def test_create_task_default_status():
    """WHEN a user does not provide a status, THE CLI SHALL create a task with status 'pending'."""
    backend = FakeBackend()
    store = TaskStore(backend)
    
    task = store.create_task("Fix bug")
    
    assert task["status"] == "pending"


# Requirement 1.5: Assign unique task ID
def test_create_task_assigns_unique_id():
    """WHEN a task is created, THE Task_Store SHALL assign a unique Task_ID."""
    backend = FakeBackend()
    store = TaskStore(backend)
    
    task1 = store.create_task("First task")
    task2 = store.create_task("Second task")
    task3 = store.create_task("Third task")
    
    assert task1["id"] != task2["id"]
    assert task2["id"] != task3["id"]
    assert task1["id"] != task3["id"]


# Requirement 1.6: Record creation timestamp
def test_create_task_records_timestamp():
    """WHEN a task is created, THE Task_Store SHALL record the creation timestamp in ISO format."""
    backend = FakeBackend()
    store = TaskStore(backend)
    
    task = store.create_task("Time-sensitive task")
    
    assert "created_at" in task
    # Verify it's a valid ISO timestamp by parsing it
    datetime.fromisoformat(task["created_at"])


# Requirement 5.1: Retrieve all tasks
def test_get_all_tasks():
    """THE Task_Store SHALL provide a method to retrieve all tasks."""
    backend = FakeBackend()
    store = TaskStore(backend)
    
    store.create_task("Task A")
    store.create_task("Task B")
    
    tasks = store.get_all_tasks()
    
    assert len(tasks) == 2
    assert any(t["title"] == "Task A" for t in tasks)
    assert any(t["title"] == "Task B" for t in tasks)


# Requirement 5.2: Tasks returned in creation order
def test_get_all_tasks_returns_in_creation_order():
    """WHEN retrieving tasks, THE Task_Store SHALL return tasks in creation order."""
    backend = FakeBackend()
    store = TaskStore(backend)
    
    task1 = store.create_task("First task")
    task2 = store.create_task("Second task")
    task3 = store.create_task("Third task")
    
    tasks = store.get_all_tasks()
    
    assert tasks[0]["title"] == "First task"
    assert tasks[1]["title"] == "Second task"
    assert tasks[2]["title"] == "Third task"


# Requirement 5.3: Retrieve task by ID
def test_get_task_by_id():
    """THE Task_Store SHALL provide a method to retrieve a task by Task_ID."""
    backend = FakeBackend()
    store = TaskStore(backend)
    
    created_task = store.create_task("Specific task")
    task_id = created_task["id"]
    
    retrieved_task = store.get_task(task_id)
    
    assert retrieved_task is not None
    assert retrieved_task["title"] == "Specific task"
    assert retrieved_task["id"] == task_id


# Requirement 5.4: Non-existent ID returns None
def test_get_task_nonexistent_id_returns_none():
    """WHEN a Task_ID does not exist, THE Task_Store SHALL return an error indicating the task was not found."""
    backend = FakeBackend()
    store = TaskStore(backend)
    
    result = store.get_task(999)
    
    assert result is None


# Requirement 5.5: Empty storage returns empty list
def test_get_all_tasks_empty_storage():
    """WHEN the JSON_File is empty, THE Task_Store SHALL return an empty list."""
    backend = FakeBackend()
    store = TaskStore(backend)
    
    tasks = store.get_all_tasks()
    
    assert tasks == []


# Requirement 6.1: First task gets ID 1
def test_first_task_gets_id_1():
    """WHEN the first task is created, THE Task_Store SHALL assign Task_ID 1."""
    backend = FakeBackend()
    store = TaskStore(backend)
    
    task = store.create_task("Very first task")
    
    assert task["id"] == 1


# Requirement 6.2: Sequential IDs
def test_sequential_task_ids():
    """WHEN subsequent tasks are created, THE Task_Store SHALL assign the next sequential Task_ID."""
    backend = FakeBackend()
    store = TaskStore(backend)
    
    task1 = store.create_task("Task 1")
    task2 = store.create_task("Task 2")
    task3 = store.create_task("Task 3")
    
    assert task1["id"] == 1
    assert task2["id"] == 2
    assert task3["id"] == 3


# Requirement 6.3: Next ID is max existing ID + 1
def test_next_id_is_max_plus_one():
    """THE Task_Store SHALL determine the next Task_ID by finding the maximum existing Task_ID and adding 1."""
    backend = FakeBackend()
    store = TaskStore(backend)
    
    # Create tasks with IDs 1, 2, 5 (simulating gaps)
    task1 = store.create_task("Task 1")
    task2 = store.create_task("Task 2")
    # Manually insert a task with ID 5 to simulate non-sequential IDs
    backend.tasks.append({
        "id": 5,
        "title": "Task 5",
        "tags": [],
        "status": "pending",
        "created_at": datetime.now().isoformat()
    })
    
    # Next task should get ID 6 (max 5 + 1)
    task_new = store.create_task("New task")
    
    assert task_new["id"] == 6


# Requirement 6.4: Empty storage starts at ID 1
def test_empty_storage_starts_at_id_1():
    """WHEN no tasks exist, THE Task_Store SHALL start Task_ID at 1."""
    backend = FakeBackend()
    store = TaskStore(backend)
    
    task = store.create_task("Initial task")
    
    assert task["id"] == 1


# Requirement 6.5: Task IDs are unique
def test_task_ids_are_unique():
    """THE Task_Store SHALL ensure Task_ID uniqueness across all tasks."""
    backend = FakeBackend()
    store = TaskStore(backend)
    
    tasks = [store.create_task(f"Task {i}") for i in range(10)]
    task_ids = [task["id"] for task in tasks]
    
    # All IDs should be unique
    assert len(task_ids) == len(set(task_ids))


# Edge case: Empty title handling (validation should happen at CLI layer, but test store behavior)
def test_create_task_with_empty_title():
    """Edge case: Store should handle empty title (validation at CLI layer)."""
    backend = FakeBackend()
    store = TaskStore(backend)
    
    # Store itself doesn't validate - it creates what it's given
    # This tests that store doesn't crash with empty title
    task = store.create_task("")
    
    assert task["title"] == ""


# Edge case: None tags defaults to empty list
def test_create_task_none_tags_defaults_to_empty_list():
    """Edge case: When tags is None, should default to empty list."""
    backend = FakeBackend()
    store = TaskStore(backend)
    
    task = store.create_task("Task without tags")
    
    assert task["tags"] == []


# Edge case: Empty tags list
def test_create_task_with_empty_tags_list():
    """Edge case: Explicitly passing empty tags list."""
    backend = FakeBackend()
    store = TaskStore(backend)
    
    task = store.create_task("Task with empty tags", tags=[])
    
    assert task["tags"] == []


# Edge case: Many tags
def test_create_task_with_many_tags():
    """Edge case: Task with many tags."""
    backend = FakeBackend()
    store = TaskStore(backend)
    
    many_tags = [f"tag{i}" for i in range(100)]
    task = store.create_task("Task with many tags", tags=many_tags)
    
    assert len(task["tags"]) == 100
    assert task["tags"] == many_tags


# Edge case: Special characters in title
def test_create_task_with_special_characters():
    """Edge case: Title with special characters."""
    backend = FakeBackend()
    store = TaskStore(backend)
    
    task = store.create_task("Task with special chars: !@#$%^&*()")
    
    assert task["title"] == "Task with special chars: !@#$%^&*()"


# Edge case: Unicode in title
def test_create_task_with_unicode():
    """Edge case: Title with unicode characters."""
    backend = FakeBackend()
    store = TaskStore(backend)
    
    task = store.create_task("Task with emoji 🚀 and unicode 你好")
    
    assert task["title"] == "Task with emoji 🚀 and unicode 你好"


# Edge case: Very long title
def test_create_task_with_very_long_title():
    """Edge case: Task with very long title."""
    backend = FakeBackend()
    store = TaskStore(backend)
    
    long_title = "A" * 1000
    task = store.create_task(long_title)
    
    assert task["title"] == long_title
    assert len(task["title"]) == 1000


# Edge case: Retrieve from empty storage
def test_get_task_from_empty_storage():
    """Edge case: Attempting to retrieve task when storage is empty."""
    backend = FakeBackend()
    store = TaskStore(backend)
    
    result = store.get_task(1)
    
    assert result is None


# Edge case: Retrieve with negative ID
def test_get_task_with_negative_id():
    """Edge case: Attempting to retrieve task with negative ID."""
    backend = FakeBackend()
    store = TaskStore(backend)
    
    store.create_task("Task 1")
    result = store.get_task(-1)
    
    assert result is None


# Edge case: Retrieve with zero ID
def test_get_task_with_zero_id():
    """Edge case: Attempting to retrieve task with zero ID."""
    backend = FakeBackend()
    store = TaskStore(backend)
    
    store.create_task("Task 1")
    result = store.get_task(0)
    
    assert result is None


# Edge case: Multiple tasks with same title (should be allowed)
def test_create_multiple_tasks_with_same_title():
    """Edge case: Creating multiple tasks with identical titles."""
    backend = FakeBackend()
    store = TaskStore(backend)
    
    task1 = store.create_task("Duplicate title")
    task2 = store.create_task("Duplicate title")
    
    assert task1["title"] == task2["title"]
    assert task1["id"] != task2["id"]  # But IDs must be different


# Edge case: Task persistence through backend
def test_task_persisted_to_backend():
    """Edge case: Verify task is actually saved to backend."""
    backend = FakeBackend()
    store = TaskStore(backend)
    
    task = store.create_task("Persisted task")
    
    # Verify backend has the task
    assert len(backend.tasks) == 1
    assert backend.tasks[0]["title"] == "Persisted task"


# Edge case: Get all tasks returns copy, not reference
def test_get_all_tasks_returns_independent_list():
    """Edge case: Modifying returned list shouldn't affect storage."""
    backend = FakeBackend()
    store = TaskStore(backend)
    
    store.create_task("Task 1")
    tasks1 = store.get_all_tasks()
    tasks1.append({"id": 999, "title": "Fake", "tags": [], "status": "pending", "created_at": ""})
    
    tasks2 = store.get_all_tasks()
    
    # Original storage should only have 1 task
    assert len(tasks2) == 1
