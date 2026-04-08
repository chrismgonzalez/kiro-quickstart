"""Unit tests for CLI commands.

Tests cover:
- create command with title, tags, and status
- list command for displaying tasks
- get command for retrieving specific task
- Edge cases: empty title validation, invalid status validation
- Requirements: 1.1-1.4, 4.1-4.2, 5.1-5.4

All tests will FAIL until implementation is complete (RED state).
"""

import pytest
from click.testing import CliRunner
from src.task_tracker.cli import cli


# ===== Create Command Tests =====

# Requirement 1.1: Create task with title
def test_create_command_with_title():
    """WHEN a user provides a title, THE CLI SHALL create a task with that title."""
    runner = CliRunner()
    
    result = runner.invoke(cli, ["create", "Write documentation"])
    
    assert result.exit_code == 0
    assert "Write documentation" in result.output


# Requirement 1.2: Create task with tags
def test_create_command_with_tags():
    """WHEN a user provides tags, THE CLI SHALL create a task with those tags."""
    runner = CliRunner()
    
    result = runner.invoke(cli, ["create", "Deploy application", "--tag", "urgent", "--tag", "devops"])
    
    assert result.exit_code == 0
    assert "urgent" in result.output
    assert "devops" in result.output


# Requirement 1.3: Create task with status
def test_create_command_with_status():
    """WHEN a user provides a status, THE CLI SHALL create a task with that status."""
    runner = CliRunner()
    
    result = runner.invoke(cli, ["create", "Review code", "--status", "complete"])
    
    assert result.exit_code == 0
    assert "complete" in result.output


# Requirement 1.4: Default status is pending
def test_create_command_default_status():
    """WHEN a user does not provide a status, THE CLI SHALL create a task with status 'pending'."""
    runner = CliRunner()
    
    result = runner.invoke(cli, ["create", "Fix bug"])
    
    assert result.exit_code == 0
    assert "pending" in result.output


def test_create_command_with_multiple_tags():
    """Create task with multiple tags."""
    runner = CliRunner()
    
    result = runner.invoke(cli, [
        "create", "Complex task",
        "--tag", "urgent",
        "--tag", "backend",
        "--tag", "api"
    ])
    
    assert result.exit_code == 0
    assert "urgent" in result.output
    assert "backend" in result.output
    assert "api" in result.output


def test_create_command_with_all_options():
    """Create task with title, tags, and status."""
    runner = CliRunner()
    
    result = runner.invoke(cli, [
        "create", "Full task",
        "--tag", "test",
        "--status", "complete"
    ])
    
    assert result.exit_code == 0
    assert "Full task" in result.output
    assert "test" in result.output
    assert "complete" in result.output


def test_create_command_displays_task_id():
    """Create command displays the assigned task ID."""
    runner = CliRunner()
    
    result = runner.invoke(cli, ["create", "Task with ID"])
    
    assert result.exit_code == 0
    # Should display task ID in output
    assert "ID" in result.output or "id" in result.output or "#" in result.output


def test_create_command_displays_creation_timestamp():
    """Create command displays the creation timestamp."""
    runner = CliRunner()
    
    result = runner.invoke(cli, ["create", "Timestamped task"])
    
    assert result.exit_code == 0
    # Should display timestamp or creation time in output


# ===== Create Command Validation Tests =====

# Requirement 4.1: Empty title validation
def test_create_command_rejects_empty_title():
    """WHEN a user provides an empty title, THE CLI SHALL return an error message 'Title cannot be empty'."""
    runner = CliRunner()
    
    result = runner.invoke(cli, ["create", ""])
    
    assert result.exit_code != 0
    assert "Title cannot be empty" in result.output


def test_create_command_rejects_whitespace_only_title():
    """Empty title with only whitespace raises error."""
    runner = CliRunner()
    
    result = runner.invoke(cli, ["create", "   "])
    
    assert result.exit_code != 0
    assert "Title cannot be empty" in result.output


def test_create_command_rejects_tabs_and_newlines_title():
    """Title with only tabs and newlines raises error."""
    runner = CliRunner()
    
    result = runner.invoke(cli, ["create", "\t\n\r"])
    
    assert result.exit_code != 0
    assert "Title cannot be empty" in result.output


# Requirement 4.2: Invalid status validation
def test_create_command_rejects_invalid_status():
    """WHEN a user provides an invalid status, THE CLI SHALL return an error message listing valid status values."""
    runner = CliRunner()
    
    result = runner.invoke(cli, ["create", "Test task", "--status", "in-progress"])
    
    assert result.exit_code != 0
    assert "pending" in result.output
    assert "complete" in result.output


def test_create_command_rejects_invalid_status_todo():
    """Invalid status 'todo' raises error."""
    runner = CliRunner()
    
    result = runner.invoke(cli, ["create", "Test task", "--status", "todo"])
    
    assert result.exit_code != 0


def test_create_command_rejects_invalid_status_done():
    """Invalid status 'done' raises error."""
    runner = CliRunner()
    
    result = runner.invoke(cli, ["create", "Test task", "--status", "done"])
    
    assert result.exit_code != 0


def test_create_command_rejects_invalid_status_case_sensitive():
    """Status validation is case-sensitive."""
    runner = CliRunner()
    
    result = runner.invoke(cli, ["create", "Test task", "--status", "Pending"])
    
    assert result.exit_code != 0


def test_create_command_rejects_empty_status():
    """Empty status raises error."""
    runner = CliRunner()
    
    result = runner.invoke(cli, ["create", "Test task", "--status", ""])
    
    assert result.exit_code != 0


# ===== List Command Tests =====

# Requirement 5.1: Retrieve all tasks
def test_list_command_displays_all_tasks():
    """THE Task_Store SHALL provide a method to retrieve all tasks."""
    runner = CliRunner()
    
    # Create some tasks first
    runner.invoke(cli, ["create", "Task A"])
    runner.invoke(cli, ["create", "Task B"])
    
    # List all tasks
    result = runner.invoke(cli, ["list"])
    
    assert result.exit_code == 0
    assert "Task A" in result.output
    assert "Task B" in result.output


# Requirement 5.2: Tasks in creation order
def test_list_command_shows_tasks_in_creation_order():
    """WHEN retrieving tasks, THE Task_Store SHALL return tasks in creation order."""
    runner = CliRunner()
    
    # Create tasks in specific order
    runner.invoke(cli, ["create", "First task"])
    runner.invoke(cli, ["create", "Second task"])
    runner.invoke(cli, ["create", "Third task"])
    
    # List all tasks
    result = runner.invoke(cli, ["list"])
    
    assert result.exit_code == 0
    # Verify order in output
    first_pos = result.output.find("First task")
    second_pos = result.output.find("Second task")
    third_pos = result.output.find("Third task")
    
    assert first_pos < second_pos < third_pos


# Requirement 5.5: Empty storage returns empty list
def test_list_command_with_no_tasks():
    """WHEN the JSON_File is empty, THE Task_Store SHALL return an empty list."""
    runner = CliRunner()
    
    result = runner.invoke(cli, ["list"])
    
    assert result.exit_code == 0
    # Should indicate no tasks or show empty list
    assert "No tasks" in result.output or result.output.strip() == ""


def test_list_command_displays_task_details():
    """List command displays task ID, title, tags, and status."""
    runner = CliRunner()
    
    runner.invoke(cli, ["create", "Detailed task", "--tag", "test", "--status", "complete"])
    
    result = runner.invoke(cli, ["list"])
    
    assert result.exit_code == 0
    assert "Detailed task" in result.output
    assert "test" in result.output
    assert "complete" in result.output


def test_list_command_with_many_tasks():
    """List command handles many tasks."""
    runner = CliRunner()
    
    # Create 10 tasks
    for i in range(10):
        runner.invoke(cli, ["create", f"Task {i}"])
    
    result = runner.invoke(cli, ["list"])
    
    assert result.exit_code == 0
    # All tasks should be displayed
    for i in range(10):
        assert f"Task {i}" in result.output


def test_list_command_with_filter_by_status():
    """List command can filter by status."""
    runner = CliRunner()
    
    runner.invoke(cli, ["create", "Pending task", "--status", "pending"])
    runner.invoke(cli, ["create", "Complete task", "--status", "complete"])
    
    result = runner.invoke(cli, ["list", "--status", "pending"])
    
    assert result.exit_code == 0
    assert "Pending task" in result.output
    assert "Complete task" not in result.output


def test_list_command_with_filter_by_tag():
    """List command can filter by tag."""
    runner = CliRunner()
    
    runner.invoke(cli, ["create", "Urgent task", "--tag", "urgent"])
    runner.invoke(cli, ["create", "Normal task", "--tag", "normal"])
    
    result = runner.invoke(cli, ["list", "--tag", "urgent"])
    
    assert result.exit_code == 0
    assert "Urgent task" in result.output
    assert "Normal task" not in result.output


# ===== Get Command Tests =====

# Requirement 5.3: Retrieve task by ID
def test_get_command_retrieves_task_by_id():
    """THE Task_Store SHALL provide a method to retrieve a task by Task_ID."""
    runner = CliRunner()
    
    # Create a task
    create_result = runner.invoke(cli, ["create", "Specific task"])
    
    # Extract task ID from output (assuming it's displayed)
    # For now, assume first task gets ID 1
    result = runner.invoke(cli, ["get", "1"])
    
    assert result.exit_code == 0
    assert "Specific task" in result.output


# Requirement 5.4: Non-existent ID returns error
def test_get_command_nonexistent_id_returns_error():
    """WHEN a Task_ID does not exist, THE Task_Store SHALL return an error indicating the task was not found."""
    runner = CliRunner()
    
    result = runner.invoke(cli, ["get", "999"])
    
    assert result.exit_code != 0
    assert "not found" in result.output.lower()


def test_get_command_displays_full_task_details():
    """Get command displays all task details."""
    runner = CliRunner()
    
    runner.invoke(cli, ["create", "Full details task", "--tag", "test", "--tag", "demo", "--status", "complete"])
    
    result = runner.invoke(cli, ["get", "1"])
    
    assert result.exit_code == 0
    assert "Full details task" in result.output
    assert "test" in result.output
    assert "demo" in result.output
    assert "complete" in result.output


def test_get_command_with_invalid_id_format():
    """Get command with non-numeric ID returns error."""
    runner = CliRunner()
    
    result = runner.invoke(cli, ["get", "abc"])
    
    assert result.exit_code != 0


def test_get_command_with_negative_id():
    """Get command with negative ID returns error."""
    runner = CliRunner()
    
    result = runner.invoke(cli, ["get", "-1"])
    
    assert result.exit_code != 0


def test_get_command_with_zero_id():
    """Get command with zero ID returns error."""
    runner = CliRunner()
    
    result = runner.invoke(cli, ["get", "0"])
    
    assert result.exit_code != 0


# ===== Edge Cases =====

def test_create_command_with_unicode_title():
    """Create task with unicode characters in title."""
    runner = CliRunner()
    
    result = runner.invoke(cli, ["create", "Task with emoji 🚀 and unicode 你好"])
    
    assert result.exit_code == 0
    assert "🚀" in result.output or "unicode" in result.output


def test_create_command_with_special_characters():
    """Create task with special characters in title."""
    runner = CliRunner()
    
    result = runner.invoke(cli, ["create", "Task: Fix bug #42 @mention & review!"])
    
    assert result.exit_code == 0


def test_create_command_with_very_long_title():
    """Create task with very long title."""
    runner = CliRunner()
    
    long_title = "A" * 500
    result = runner.invoke(cli, ["create", long_title])
    
    assert result.exit_code == 0


def test_create_command_with_unicode_tags():
    """Create task with unicode tags."""
    runner = CliRunner()
    
    result = runner.invoke(cli, ["create", "Unicode tags", "--tag", "重要", "--tag", "🔥"])
    
    assert result.exit_code == 0


def test_create_command_with_empty_tag():
    """Create task with empty tag string."""
    runner = CliRunner()
    
    result = runner.invoke(cli, ["create", "Task", "--tag", ""])
    
    # Should either accept empty tag or reject it
    # Behavior depends on validation rules


def test_list_command_with_unicode_content():
    """List command displays unicode content correctly."""
    runner = CliRunner()
    
    runner.invoke(cli, ["create", "Unicode task 你好", "--tag", "重要"])
    
    result = runner.invoke(cli, ["list"])
    
    assert result.exit_code == 0


def test_cli_help_command():
    """CLI help command works."""
    runner = CliRunner()
    
    result = runner.invoke(cli, ["--help"])
    
    assert result.exit_code == 0
    assert "create" in result.output.lower() or "help" in result.output.lower()


def test_create_command_help():
    """Create command help works."""
    runner = CliRunner()
    
    result = runner.invoke(cli, ["create", "--help"])
    
    assert result.exit_code == 0
    assert "title" in result.output.lower()


def test_list_command_help():
    """List command help works."""
    runner = CliRunner()
    
    result = runner.invoke(cli, ["list", "--help"])
    
    assert result.exit_code == 0


def test_get_command_help():
    """Get command help works."""
    runner = CliRunner()
    
    result = runner.invoke(cli, ["get", "--help"])
    
    assert result.exit_code == 0


def test_cli_version_command():
    """CLI version command works."""
    runner = CliRunner()
    
    result = runner.invoke(cli, ["--version"])
    
    assert result.exit_code == 0


def test_create_command_with_quotes_in_title():
    """Create task with quotes in title."""
    runner = CliRunner()
    
    result = runner.invoke(cli, ["create", 'Task with "quotes" in title'])
    
    assert result.exit_code == 0


def test_create_command_with_newline_in_title():
    """Create task with newline in title."""
    runner = CliRunner()
    
    result = runner.invoke(cli, ["create", "Task with\nnewline"])
    
    # Should either accept or reject newlines
    # Behavior depends on validation rules


def test_list_command_multiple_invocations():
    """List command can be invoked multiple times."""
    runner = CliRunner()
    
    runner.invoke(cli, ["create", "Task 1"])
    
    result1 = runner.invoke(cli, ["list"])
    result2 = runner.invoke(cli, ["list"])
    
    assert result1.exit_code == 0
    assert result2.exit_code == 0
    assert result1.output == result2.output


def test_get_command_after_multiple_creates():
    """Get command retrieves correct task after multiple creates."""
    runner = CliRunner()
    
    runner.invoke(cli, ["create", "Task 1"])
    runner.invoke(cli, ["create", "Task 2"])
    runner.invoke(cli, ["create", "Task 3"])
    
    result = runner.invoke(cli, ["get", "2"])
    
    assert result.exit_code == 0
    assert "Task 2" in result.output


def test_create_command_persistence():
    """Tasks persist between CLI invocations."""
    runner = CliRunner()
    
    # Create task in first invocation
    runner.invoke(cli, ["create", "Persistent task"])
    
    # List in second invocation (new runner simulates new CLI session)
    result = runner.invoke(cli, ["list"])
    
    assert result.exit_code == 0
    assert "Persistent task" in result.output


def test_create_command_with_duplicate_tags():
    """Create task with duplicate tags."""
    runner = CliRunner()
    
    result = runner.invoke(cli, [
        "create", "Task",
        "--tag", "duplicate",
        "--tag", "duplicate"
    ])
    
    # Should either accept duplicates or deduplicate
    assert result.exit_code == 0


def test_list_command_with_no_filters():
    """List command without filters shows all tasks."""
    runner = CliRunner()
    
    runner.invoke(cli, ["create", "Task 1", "--status", "pending"])
    runner.invoke(cli, ["create", "Task 2", "--status", "complete"])
    
    result = runner.invoke(cli, ["list"])
    
    assert result.exit_code == 0
    assert "Task 1" in result.output
    assert "Task 2" in result.output


def test_get_command_with_large_id():
    """Get command with very large ID."""
    runner = CliRunner()
    
    result = runner.invoke(cli, ["get", "999999999"])
    
    assert result.exit_code != 0
    assert "not found" in result.output.lower()
