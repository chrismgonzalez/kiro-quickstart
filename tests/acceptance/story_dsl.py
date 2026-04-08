"""Layer 2: Domain-Specific Language - Composes driver operations into scenarios.

DSL methods use domain language and compose multiple driver calls.
State flows through tests via return values.
All assertions are in domain terms.
"""

from typing import List, Dict, Any
from datetime import datetime
from tests.acceptance.system_driver import SystemDriver


class StoryDsl:
    """Domain-specific language for task tracker acceptance tests."""

    def __init__(self):
        """Initialize DSL with a protocol driver."""
        self.driver = SystemDriver()

    # ===== GIVEN: Set up world state =====

    def task_tracker_is_ready(self) -> Dict[str, Any]:
        """Set up a fresh task tracker ready for use."""
        self.driver.initialize_storage()
        return {
            "tasks": [],
            "driver": self.driver
        }

    def task_tracker_storage_does_not_exist(self) -> Dict[str, Any]:
        """Set up task tracker with no existing storage."""
        self.driver.initialize_storage()
        # Storage is created but empty - simulates first use
        return {
            "tasks": [],
            "driver": self.driver
        }

    def task_tracker_storage_is_corrupted(self) -> Dict[str, Any]:
        """Set up task tracker with corrupted storage."""
        self.driver.initialize_storage()
        self.driver.corrupt_storage()
        return {
            "tasks": [],
            "driver": self.driver,
            "error": None
        }

    def user_has_created_task(self, state: Dict[str, Any], title: str, 
                             tags: List[str] = None) -> Dict[str, Any]:
        """Set up world state where user has already created a task."""
        task = self.driver.create_task(title, tags)
        state["tasks"].append(task)
        return state

    def no_tasks_have_been_created(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Ensure no tasks exist in the system."""
        # State already has empty task list
        return state

    def tasks_exist_with_ids(self, state: Dict[str, Any], ids: List[int]) -> Dict[str, Any]:
        """Set up world state with tasks having specific IDs."""
        for task_id in ids:
            task = self.driver.create_task(f"Task {task_id}")
            state["tasks"].append(task)
        return state

    # ===== WHEN: Perform actions =====

    def user_creates_task(self, state: Dict[str, Any], title: str) -> Dict[str, Any]:
        """User creates a task with just a title."""
        task = self.driver.create_task(title)
        state["tasks"].append(task)
        state["last_task"] = task
        return state

    def user_creates_task_with_tags(self, state: Dict[str, Any], title: str, 
                                   tags: List[str]) -> Dict[str, Any]:
        """User creates a task with title and tags."""
        task = self.driver.create_task(title, tags=tags)
        state["tasks"].append(task)
        state["last_task"] = task
        return state

    def user_creates_task_with_status(self, state: Dict[str, Any], title: str, 
                                     status: str) -> Dict[str, Any]:
        """User creates a task with title and status."""
        task = self.driver.create_task(title, status=status)
        state["tasks"].append(task)
        state["last_task"] = task
        return state

    def user_attempts_to_create_task_with_empty_title(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """User attempts to create a task with empty title."""
        try:
            task = self.driver.create_task("")
            state["last_task"] = task
            state["error"] = None
        except ValueError as e:
            state["error"] = str(e)
        return state

    def user_attempts_to_create_task_with_invalid_status(self, state: Dict[str, Any], 
                                                        title: str, status: str) -> Dict[str, Any]:
        """User attempts to create a task with invalid status."""
        try:
            task = self.driver.create_task(title, status=status)
            state["last_task"] = task
            state["error"] = None
        except ValueError as e:
            state["error"] = str(e)
        return state

    def user_retrieves_all_tasks(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """User retrieves all tasks from storage."""
        retrieved_tasks = self.driver.get_all_tasks()
        state["retrieved_tasks"] = retrieved_tasks
        return state

    def user_attempts_to_retrieve_all_tasks(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """User attempts to retrieve all tasks (may fail)."""
        try:
            retrieved_tasks = self.driver.get_all_tasks()
            state["retrieved_tasks"] = retrieved_tasks
            state["error"] = None
        except Exception as e:
            state["error"] = str(e)
        return state

    def user_retrieves_task_by_id(self, state: Dict[str, Any], task_id: int) -> Dict[str, Any]:
        """User retrieves a specific task by its ID."""
        task = self.driver.get_task_by_id(task_id)
        state["retrieved_task"] = task
        return state

    def user_attempts_to_retrieve_task_by_id(self, state: Dict[str, Any], 
                                            task_id: int) -> Dict[str, Any]:
        """User attempts to retrieve a task by ID (may not exist)."""
        task = self.driver.get_task_by_id(task_id)
        state["retrieved_task"] = task
        if task is None:
            state["error"] = f"Task with ID {task_id} not found"
        return state

    def user_lists_all_tasks(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """User lists all tasks in order."""
        retrieved_tasks = self.driver.get_all_tasks()
        state["task_list"] = retrieved_tasks
        return state

    def user_creates_multiple_tasks(self, state: Dict[str, Any], count: int) -> Dict[str, Any]:
        """User creates multiple tasks."""
        for i in range(count):
            task = self.driver.create_task(f"Task {i+1}")
            state["tasks"].append(task)
        return state

    # ===== THEN: Make assertions =====

    def task_exists_with_title(self, state: Dict[str, Any], title: str) -> None:
        """Assert that a task exists with the given title."""
        matching = [t for t in state["tasks"] if t["title"] == title]
        assert len(matching) == 1, f"Expected 1 task with title '{title}', found {len(matching)}"

    def task_exists_with_title_and_tags(self, state: Dict[str, Any], title: str, 
                                       tags: List[str]) -> None:
        """Assert that a task exists with the given title and tags."""
        matching = [t for t in state["tasks"] 
                   if t["title"] == title and t["tags"] == tags]
        assert len(matching) == 1, f"Expected 1 task with title '{title}' and tags {tags}"

    def task_exists_with_title_and_status(self, state: Dict[str, Any], title: str, 
                                         status: str) -> None:
        """Assert that a task exists with the given title and status."""
        matching = [t for t in state["tasks"] 
                   if t["title"] == title and t["status"] == status]
        assert len(matching) == 1, f"Expected 1 task with title '{title}' and status '{status}'"

    def task_has_status(self, state: Dict[str, Any], status: str) -> None:
        """Assert that the last created task has the given status."""
        assert "last_task" in state, "No task was created"
        assert state["last_task"]["status"] == status, \
            f"Expected status '{status}', got '{state['last_task']['status']}'"

    def each_task_has_different_identifier(self, state: Dict[str, Any]) -> None:
        """Assert that all tasks have unique IDs."""
        ids = [t["id"] for t in state["tasks"]]
        assert len(ids) == len(set(ids)), "Task IDs are not unique"

    def task_has_creation_timestamp(self, state: Dict[str, Any]) -> None:
        """Assert that the last task has a creation timestamp."""
        assert "last_task" in state, "No task was created"
        assert "created_at" in state["last_task"], "Task has no creation timestamp"
        assert state["last_task"]["created_at"], "Creation timestamp is empty"

    def task_is_successfully_created(self, state: Dict[str, Any]) -> None:
        """Assert that a task was successfully created."""
        assert "last_task" in state, "No task was created"
        assert state["last_task"] is not None, "Task creation failed"

    def n_tasks_exist(self, state: Dict[str, Any], count: int) -> None:
        """Assert that exactly N tasks exist."""
        retrieved = state.get("retrieved_tasks", state.get("tasks", []))
        assert len(retrieved) == count, f"Expected {count} tasks, found {len(retrieved)}"

    def error_message_indicates_storage_is_invalid(self, state: Dict[str, Any]) -> None:
        """Assert that an error message indicates invalid storage."""
        assert state.get("error") is not None, "Expected an error but none occurred"
        error = state["error"].lower()
        assert "json" in error or "invalid" in error or "corrupt" in error, \
            f"Error message doesn't indicate storage issue: {state['error']}"

    def task_is_not_created(self, state: Dict[str, Any]) -> None:
        """Assert that no task was created."""
        assert state.get("error") is not None, "Expected task creation to fail"

    def error_message_is(self, state: Dict[str, Any], message: str) -> None:
        """Assert that the error message matches expected text."""
        assert state.get("error") is not None, "Expected an error but none occurred"
        assert message in state["error"], \
            f"Expected error '{message}', got '{state['error']}'"

    def error_message_lists_valid_status_values(self, state: Dict[str, Any]) -> None:
        """Assert that error message lists valid status values."""
        assert state.get("error") is not None, "Expected an error but none occurred"
        error = state["error"].lower()
        assert "pending" in error or "complete" in error, \
            f"Error doesn't list valid status values: {state['error']}"

    def task_has_identifier_greater_than_zero(self, state: Dict[str, Any]) -> None:
        """Assert that the last task has a positive integer ID."""
        assert "last_task" in state, "No task was created"
        assert state["last_task"]["id"] > 0, \
            f"Expected ID > 0, got {state['last_task']['id']}"

    def task_has_valid_iso_format_timestamp(self, state: Dict[str, Any]) -> None:
        """Assert that the last task has a valid ISO format timestamp."""
        assert "last_task" in state, "No task was created"
        timestamp = state["last_task"]["created_at"]
        try:
            datetime.fromisoformat(timestamp)
        except ValueError:
            assert False, f"Invalid ISO timestamp: {timestamp}"

    def task_has_title(self, state: Dict[str, Any], title: str) -> None:
        """Assert that the retrieved task has the given title."""
        task = state.get("retrieved_task")
        assert task is not None, "No task was retrieved"
        assert task["title"] == title, f"Expected title '{title}', got '{task['title']}'"

    def error_indicates_task_not_found(self, state: Dict[str, Any]) -> None:
        """Assert that error indicates task was not found."""
        assert state.get("error") is not None or state.get("retrieved_task") is None, \
            "Expected task not found error"

    def tasks_appear_in_order(self, state: Dict[str, Any], titles: List[str]) -> None:
        """Assert that tasks appear in the specified order."""
        task_list = state.get("task_list", [])
        actual_titles = [t["title"] for t in task_list]
        assert actual_titles == titles, \
            f"Expected order {titles}, got {actual_titles}"

    def task_has_identifier(self, state: Dict[str, Any], task_id: int) -> None:
        """Assert that the last task has the specified ID."""
        assert "last_task" in state, "No task was created"
        assert state["last_task"]["id"] == task_id, \
            f"Expected ID {task_id}, got {state['last_task']['id']}"

    def tasks_have_identifiers(self, state: Dict[str, Any], ids: List[int]) -> None:
        """Assert that tasks have the specified IDs in order."""
        actual_ids = [t["id"] for t in state["tasks"]]
        assert actual_ids == ids, f"Expected IDs {ids}, got {actual_ids}"

    def all_tasks_have_different_identifiers(self, state: Dict[str, Any]) -> None:
        """Assert that all tasks have unique IDs."""
        ids = [t["id"] for t in state["tasks"]]
        assert len(ids) == len(set(ids)), "Task IDs are not unique"


# Create namespace aliases for given/when/then pattern
dsl = StoryDsl()
given = dsl
when = dsl
then = dsl
