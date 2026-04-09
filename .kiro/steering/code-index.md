---
description: Maps every component, function, and module to its exact file location. Keep updated when adding new code.
---

# Code Index

## Project Overview

**Task Tracker CLI** - A proof-of-concept demonstrating ATDD with the four-layer test architecture & spec driven development.

**Tech Stack:**

- Language: Python 3.11+
- CLI: Click
- Testing: pytest
- Storage: JSON file

---

## Source Map

### Application Modules

**src/task_tracker/**

- `__init__.py` - Package initialization with version
- `models.py` - Task data model and validation
  - `Task` - TypedDict defining task structure (id, title, tags, status, created_at)
  - `validate_title()` - Ensures title is non-empty
  - `validate_status()` - Ensures status is "pending" or "complete"
  - `validate_task_id()` - Ensures ID is positive integer
  - `validate_timestamp()` - Ensures timestamp is valid ISO format
- `storage.py` - Storage backend protocol
  - `StorageBackend` - Abstract protocol for storage implementations
  - `save_task()` - Save a task to storage
  - `load_tasks()` - Load all tasks from storage
  - `get_task_by_id()` - Retrieve specific task by ID
- `json_backend.py` - JSON file storage implementation
  - `JSONFileBackend` - Implements StorageBackend using JSON file
  - `__init__()` - Initialize with file path (default: ~/.task-tracker/tasks.json)
  - `save_task()` - Append task to JSON file
  - `load_tasks()` - Read all tasks from JSON file
  - `get_task_by_id()` - Find task by ID in JSON file
- `store.py` - Task business logic
  - `TaskStore` - Core task management with ID generation
  - `__init__()` - Initialize with storage backend
  - `create_task()` - Create task with auto-incrementing ID and timestamp
  - `get_all_tasks()` - Retrieve all tasks
  - `get_task()` - Retrieve specific task by ID
- `filter.py` - Task filtering logic
  - `TaskFilter` - Filter tasks by various criteria
  - `filter_by_status()` - Filter tasks by status (pending/complete)
  - `filter_by_tags()` - Filter tasks by tags (AND logic)
  - `filter_by_id()` - Find single task by ID
- `formatter.py` - Output formatting
  - `TaskFormatter` - Format tasks for display
  - `format_task()` - Format single task with ID, title, status, tags, timestamp
  - `format_task_list()` - Format multiple tasks with header
  - `format_empty_list()` - Format message for empty task list
- `cli.py` - Click CLI interface
  - `get_backend()` - Factory function for storage backend
  - `cli()` - Main CLI group
  - `create()` - Create new task (--tag, --status options)
  - `list()` - List tasks (--status, --tag filters)
  - `get()` - Get specific task by ID

### Test Suite

**tests/**

- `__init__.py` - Test package initialization
- `test_smoke.py` - Infrastructure smoke tests
  - `test_infrastructure()` - Verify pytest works
  - `test_imports()` - Verify CLI module imports

**tests/acceptance/** - Layer 1 & 2 (30+ scenarios)

- `__init__.py` - Acceptance test package
- `test_task_creation.py` - Layer 1: Test cases in domain language
  - 30+ test scenarios covering all requirements
  - Tests for task creation, persistence, retrieval, validation, ID generation
- `story_dsl.py` - Layer 2: Domain-specific language
  - `StoryDsl` - Composes driver operations into scenarios
  - `given.*` methods - Set up world state
  - `when.*` methods - Perform user actions
  - `then.*` methods - Make assertions in domain terms
- `system_driver.py` - Layer 3: Protocol driver
  - `SystemDriver` - Elementary calls to application modules
  - `initialize_storage()` - Set up temporary test storage
  - `create_task()` - Call TaskStore.create_task()
  - `get_all_tasks()` - Call TaskStore.get_all_tasks()
  - `get_task_by_id()` - Call TaskStore.get_task()
  - `corrupt_storage()` - Simulate storage errors

**tests/unit/** - Component-level tests

- `__init__.py` - Unit test package
- `conftest.py` - Shared test fixtures
- `test_models.py` - Task model and validation tests
- `test_storage.py` - StorageBackend protocol tests
- `test_json_backend.py` - JSON file backend tests
- `test_store.py` - TaskStore business logic tests
- `test_filter.py` - TaskFilter tests
- `test_formatter.py` - TaskFormatter tests
- `test_cli.py` - CLI command tests

**Configuration:**

- `pyproject.toml` - Project configuration, dependencies, pytest settings
- `Makefile` - Development commands (install, test, run, lint, clean)

---

## Key Patterns & Architecture

### Four-Layer Test Architecture

1. **Test Cases** (Layer 1): Plain domain language, no technical details
2. **DSL** (Layer 2): Composes driver operations into scenarios
3. **Protocol Driver** (Layer 3): Elementary calls to application modules
4. **System Under Test** (Layer 4): Application modules themselves

### Data Model

```python
Task = {
    "id": int,           # Auto-incrementing ID
    "title": str,        # Task title
    "tags": List[str],   # List of tags
    "status": str,       # "pending" or "complete"
    "created_at": str    # ISO timestamp
}
```

### Storage

- JSON file at `~/.task-tracker/tasks.json`
- Simple list of task dictionaries
- Auto-incrementing IDs

---

## Testing Strategy

### Acceptance Tests

- Test complete user workflows end-to-end
- Use real TaskStore, TaskFilter, TaskFormatter
- No mocking (all code is under our control)
- Written before implementation (RED)
- Pass when story is complete (GREEN)

### Unit Tests

- Test individual module behavior
- Use real implementations
- Fast and focused
- Written before implementing each module (RED)
- Pass when module is complete (GREEN)

---

## Maintenance Notes

**Keep this file updated when:**

- Adding new CLI commands
- Adding new modules (store, filter, formatter, etc.)
- Adding new test files
- Changing module dependencies
- Adding new functions to existing modules
