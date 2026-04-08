"""Layer 1: Test Cases - Executable specifications in plain domain language.

All Gherkin scenarios from design.md translated into executable test cases.
Uses namespace pattern: given.*, when.*, then.* methods.
State flows through tests via return values.
No technical details - pure domain language.
"""

import pytest
from tests.acceptance.story_dsl import given, when, then


# ===== Requirement 1: Create Tasks =====

def test_user_creates_task_with_title():
    """Scenario: User creates task with title
    Given the task tracker is ready
    When the user creates a task with title "Write documentation"
    Then a task exists with title "Write documentation"
    """
    state = given.task_tracker_is_ready()
    state = when.user_creates_task(state, "Write documentation")
    then.task_exists_with_title(state, "Write documentation")


def test_user_creates_task_with_tags():
    """Scenario: User creates task with tags
    Given the task tracker is ready
    When the user creates a task with title "Deploy application" and tags "urgent" and "devops"
    Then a task exists with title "Deploy application" and tags "urgent" and "devops"
    """
    state = given.task_tracker_is_ready()
    state = when.user_creates_task_with_tags(state, "Deploy application", ["urgent", "devops"])
    then.task_exists_with_title_and_tags(state, "Deploy application", ["urgent", "devops"])


def test_user_creates_task_with_status():
    """Scenario: User creates task with status
    Given the task tracker is ready
    When the user creates a task with title "Review code" and status "complete"
    Then a task exists with title "Review code" and status "complete"
    """
    state = given.task_tracker_is_ready()
    state = when.user_creates_task_with_status(state, "Review code", "complete")
    then.task_exists_with_title_and_status(state, "Review code", "complete")


def test_user_creates_task_without_specifying_status():
    """Scenario: User creates task without specifying status
    Given the task tracker is ready
    When the user creates a task with title "Fix bug"
    Then a task exists with title "Fix bug" and status "pending"
    """
    state = given.task_tracker_is_ready()
    state = when.user_creates_task(state, "Fix bug")
    then.task_exists_with_title_and_status(state, "Fix bug", "pending")


def test_each_task_receives_unique_identifier():
    """Scenario: Each task receives a unique identifier
    Given the task tracker is ready
    When the user creates a task with title "First task"
    And the user creates a task with title "Second task"
    And the user creates a task with title "Third task"
    Then each task has a different identifier
    """
    state = given.task_tracker_is_ready()
    state = when.user_creates_task(state, "First task")
    state = when.user_creates_task(state, "Second task")
    state = when.user_creates_task(state, "Third task")
    then.each_task_has_different_identifier(state)


def test_task_records_creation_timestamp():
    """Scenario: Task records when it was created
    Given the task tracker is ready
    When the user creates a task with title "Time-sensitive task"
    Then the task has a creation timestamp
    """
    state = given.task_tracker_is_ready()
    state = when.user_creates_task(state, "Time-sensitive task")
    then.task_has_creation_timestamp(state)


# ===== Requirement 2: Persist Tasks to JSON File =====

def test_created_task_is_persisted():
    """Scenario: Created task is persisted
    Given the task tracker is ready
    When the user creates a task with title "Persistent task"
    And the user retrieves all tasks
    Then a task exists with title "Persistent task"
    """
    state = given.task_tracker_is_ready()
    state = when.user_creates_task(state, "Persistent task")
    state = when.user_retrieves_all_tasks(state)
    then.task_exists_with_title(state, "Persistent task")


def test_task_tracker_initializes_storage_on_first_use():
    """Scenario: Task tracker initializes storage on first use
    Given the task tracker storage does not exist
    When the user creates a task with title "First ever task"
    Then the task is successfully created
    And a task exists with title "First ever task"
    """
    state = given.task_tracker_storage_does_not_exist()
    state = when.user_creates_task(state, "First ever task")
    then.task_is_successfully_created(state)
    then.task_exists_with_title(state, "First ever task")


def test_multiple_tasks_are_stored_together():
    """Scenario: Multiple tasks are stored together
    Given the task tracker is ready
    When the user creates a task with title "Task one"
    And the user creates a task with title "Task two"
    And the user retrieves all tasks
    Then 2 tasks exist
    And a task exists with title "Task one"
    And a task exists with title "Task two"
    """
    state = given.task_tracker_is_ready()
    state = when.user_creates_task(state, "Task one")
    state = when.user_creates_task(state, "Task two")
    state = when.user_retrieves_all_tasks(state)
    then.n_tasks_exist(state, 2)
    then.task_exists_with_title(state, "Task one")
    then.task_exists_with_title(state, "Task two")


def test_storage_remains_valid_after_multiple_operations():
    """Scenario: Storage remains valid after multiple operations
    Given the task tracker is ready
    When the user creates a task with title "Alpha"
    And the user creates a task with title "Beta"
    And the user creates a task with title "Gamma"
    And the user retrieves all tasks
    Then 3 tasks exist
    """
    state = given.task_tracker_is_ready()
    state = when.user_creates_task(state, "Alpha")
    state = when.user_creates_task(state, "Beta")
    state = when.user_creates_task(state, "Gamma")
    state = when.user_retrieves_all_tasks(state)
    then.n_tasks_exist(state, 3)


def test_user_retrieves_previously_created_tasks():
    """Scenario: User retrieves previously created tasks
    Given the task tracker is ready
    And the user has created a task with title "Stored task" and tags "important"
    When the user retrieves all tasks
    Then a task exists with title "Stored task" and tags "important"
    """
    state = given.task_tracker_is_ready()
    state = given.user_has_created_task(state, "Stored task", ["important"])
    state = when.user_retrieves_all_tasks(state)
    then.task_exists_with_title_and_tags(state, "Stored task", ["important"])


def test_corrupted_storage_produces_error_message():
    """Scenario: Corrupted storage produces error message
    Given the task tracker storage is corrupted
    When the user attempts to retrieve all tasks
    Then an error message indicates the storage is invalid
    """
    state = given.task_tracker_storage_is_corrupted()
    state = when.user_attempts_to_retrieve_all_tasks(state)
    then.error_message_indicates_storage_is_invalid(state)


# ===== Requirement 4: Task Data Validation =====

def test_user_attempts_to_create_task_with_empty_title():
    """Scenario: User attempts to create task with empty title
    Given the task tracker is ready
    When the user attempts to create a task with an empty title
    Then the task is not created
    And an error message "Title cannot be empty" is displayed
    """
    state = given.task_tracker_is_ready()
    state = when.user_attempts_to_create_task_with_empty_title(state)
    then.task_is_not_created(state)
    then.error_message_is(state, "Title cannot be empty")


def test_user_attempts_to_create_task_with_invalid_status():
    """Scenario: User attempts to create task with invalid status
    Given the task tracker is ready
    When the user attempts to create a task with title "Test" and status "in-progress"
    Then the task is not created
    And an error message lists valid status values
    """
    state = given.task_tracker_is_ready()
    state = when.user_attempts_to_create_task_with_invalid_status(state, "Test", "in-progress")
    then.task_is_not_created(state)
    then.error_message_lists_valid_status_values(state)


def test_user_creates_task_with_multiple_tags():
    """Scenario: User creates task with multiple tags
    Given the task tracker is ready
    When the user creates a task with title "Tagged task" and tags "work", "urgent", and "backend"
    Then a task exists with title "Tagged task" and tags "work", "urgent", and "backend"
    """
    state = given.task_tracker_is_ready()
    state = when.user_creates_task_with_tags(state, "Tagged task", ["work", "urgent", "backend"])
    then.task_exists_with_title_and_tags(state, "Tagged task", ["work", "urgent", "backend"])


def test_task_identifiers_are_positive_integers():
    """Scenario: Task identifiers are positive integers
    Given the task tracker is ready
    When the user creates a task with title "ID test"
    Then the task has an identifier greater than zero
    """
    state = given.task_tracker_is_ready()
    state = when.user_creates_task(state, "ID test")
    then.task_has_identifier_greater_than_zero(state)


def test_task_timestamp_follows_iso_format():
    """Scenario: Task timestamp follows ISO format
    Given the task tracker is ready
    When the user creates a task with title "Timestamp test"
    Then the task has a valid ISO format timestamp
    """
    state = given.task_tracker_is_ready()
    state = when.user_creates_task(state, "Timestamp test")
    then.task_has_valid_iso_format_timestamp(state)


# ===== Requirement 5: Task Retrieval =====

def test_user_retrieves_all_tasks():
    """Scenario: User retrieves all tasks
    Given the task tracker is ready
    And the user has created a task with title "Task A"
    And the user has created a task with title "Task B"
    When the user retrieves all tasks
    Then 2 tasks exist
    """
    state = given.task_tracker_is_ready()
    state = given.user_has_created_task(state, "Task A")
    state = given.user_has_created_task(state, "Task B")
    state = when.user_retrieves_all_tasks(state)
    then.n_tasks_exist(state, 2)


def test_tasks_are_listed_in_creation_order():
    """Scenario: Tasks are listed in creation order
    Given the task tracker is ready
    When the user creates a task with title "First task"
    And the user creates a task with title "Second task"
    And the user creates a task with title "Third task"
    And the user lists all tasks
    Then the tasks appear in order: "First task", "Second task", "Third task"
    """
    state = given.task_tracker_is_ready()
    state = when.user_creates_task(state, "First task")
    state = when.user_creates_task(state, "Second task")
    state = when.user_creates_task(state, "Third task")
    state = when.user_lists_all_tasks(state)
    then.tasks_appear_in_order(state, ["First task", "Second task", "Third task"])


def test_user_retrieves_specific_task_by_identifier():
    """Scenario: User retrieves specific task by identifier
    Given the task tracker is ready
    And the user has created a task with title "Specific task"
    When the user retrieves the task by its identifier
    Then the task has title "Specific task"
    """
    state = given.task_tracker_is_ready()
    state = given.user_has_created_task(state, "Specific task")
    task_id = state["tasks"][0]["id"]
    state = when.user_retrieves_task_by_id(state, task_id)
    then.task_has_title(state, "Specific task")


def test_user_attempts_to_retrieve_non_existent_task():
    """Scenario: User attempts to retrieve non-existent task
    Given the task tracker is ready
    When the user attempts to retrieve a task with identifier 999
    Then an error message indicates the task was not found
    """
    state = given.task_tracker_is_ready()
    state = when.user_attempts_to_retrieve_task_by_id(state, 999)
    then.error_indicates_task_not_found(state)


def test_user_retrieves_tasks_when_none_exist():
    """Scenario: User retrieves tasks when none exist
    Given the task tracker is ready
    And no tasks have been created
    When the user retrieves all tasks
    Then 0 tasks exist
    """
    state = given.task_tracker_is_ready()
    state = given.no_tasks_have_been_created(state)
    state = when.user_retrieves_all_tasks(state)
    then.n_tasks_exist(state, 0)


# ===== Requirement 6: Task ID Generation =====

def test_first_task_receives_identifier_1():
    """Scenario: First task receives identifier 1
    Given the task tracker is ready
    And no tasks have been created
    When the user creates a task with title "Very first task"
    Then the task has identifier 1
    """
    state = given.task_tracker_is_ready()
    state = given.no_tasks_have_been_created(state)
    state = when.user_creates_task(state, "Very first task")
    then.task_has_identifier(state, 1)


def test_tasks_receive_sequential_identifiers():
    """Scenario: Tasks receive sequential identifiers
    Given the task tracker is ready
    When the user creates a task with title "Task 1"
    And the user creates a task with title "Task 2"
    And the user creates a task with title "Task 3"
    Then the tasks have identifiers 1, 2, and 3
    """
    state = given.task_tracker_is_ready()
    state = when.user_creates_task(state, "Task 1")
    state = when.user_creates_task(state, "Task 2")
    state = when.user_creates_task(state, "Task 3")
    then.tasks_have_identifiers(state, [1, 2, 3])


def test_new_task_identifier_follows_maximum_existing_identifier():
    """Scenario: New task identifier follows maximum existing identifier
    Given the task tracker is ready
    And tasks exist with identifiers 1, 2, and 5
    When the user creates a task with title "New task"
    Then the task has identifier 6
    """
    state = given.task_tracker_is_ready()
    state = given.tasks_exist_with_ids(state, [1, 2, 5])
    state = when.user_creates_task(state, "New task")
    then.task_has_identifier(state, 6)


def test_first_task_in_empty_storage_gets_identifier_1():
    """Scenario: First task in empty storage gets identifier 1
    Given the task tracker is ready
    And no tasks have been created
    When the user creates a task with title "Initial task"
    Then the task has identifier 1
    """
    state = given.task_tracker_is_ready()
    state = given.no_tasks_have_been_created(state)
    state = when.user_creates_task(state, "Initial task")
    then.task_has_identifier(state, 1)


def test_no_two_tasks_share_same_identifier():
    """Scenario: No two tasks share the same identifier
    Given the task tracker is ready
    When the user creates 10 tasks
    Then all 10 tasks have different identifiers
    """
    state = given.task_tracker_is_ready()
    state = when.user_creates_multiple_tasks(state, 10)
    then.all_tasks_have_different_identifiers(state)


# Cleanup fixture
@pytest.fixture(autouse=True)
def cleanup():
    """Clean up test storage after each test."""
    yield
    # Cleanup happens in the DSL driver
    if hasattr(given, 'driver'):
        given.driver.cleanup_storage()
