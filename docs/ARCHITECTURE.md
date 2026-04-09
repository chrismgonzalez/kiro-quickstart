# Architecture

## Overview

Task Tracker CLI demonstrates ATDD (Acceptance Test-Driven Development) using a four-layer test architecture. This document explains the architectural patterns and design decisions.

## Four-Layer Test Architecture

The test architecture separates concerns into four distinct layers, each with a specific responsibility:

### Layer 1: Test Cases

**Purpose**: Express user stories in plain domain language

**Characteristics**:

- No technical details (no HTTP, JSON, file paths)
- Reads like a specification
- Uses Given-When-Then structure
- Focuses on behavior, not implementation

**Example**:

```python
def test_user_adds_task_with_tags():
    user = given.a_user_with_empty_task_list()
    when.user_adds_task(user, "Write tests", tags=["testing"])
    then.task_appears_in_list(user, "Write tests")
```

### Layer 2: Domain-Specific Language (DSL)

**Purpose**: Compose driver operations into meaningful scenarios

**Characteristics**:

- Translates domain concepts into driver calls
- Composes multiple driver operations
- No single-line proxies to driver
- Maintains domain vocabulary

**Example**:

```python
def user_adds_task(self, user, title, tags=None):
    task = self.driver.create_task(title, tags)
    self.driver.save_task(user, task)
    return user
```

### Layer 3: Protocol Driver

**Purpose**: Elementary calls to application modules

**Characteristics**:

- One module call per method
- No business logic
- Direct interface to system under test
- Handles technical details (file I/O, API calls)

**Example**:

```python
def create_task(self, title, tags=None):
    from task_tracker.store import TaskStore
    store = TaskStore()
    return store.create(title=title, tags=tags or [])
```

### Layer 4: System Under Test

**Purpose**: Application modules that implement features

**Characteristics**:

- Production code
- No test-specific logic
- Focused, single-responsibility modules
- Testable through driver interface

**Example**:

```python
# task_tracker/store.py
class TaskStore:
    def create(self, title, tags):
        # Implementation
```

## Benefits of This Architecture

### Tests Drive Design

Module boundaries emerge naturally from what the driver needs to call. If the driver needs `TaskStore.create()`, that tells you exactly what interface to implement.

### Tests Are Documentation

Layer 1 test cases read like specifications. Anyone can understand what the system does by reading the tests.

### Tests Are Maintainable

Implementation changes don't break tests. You can refactor Layer 4 freely as long as the driver interface remains stable.

### Tests Are Fast

No mocking of code under your control. Real implementations run fast and catch integration issues.

## Module Design Principles

### Single Responsibility

Each module has one clear purpose:

- `models.py` - Task data model and validation
- `storage.py` - Storage backend protocol (interface)
- `json_backend.py` - JSON file storage implementation
- `store.py` - Task business logic and ID generation
- `filter.py` - Task filtering logic
- `formatter.py` - Output formatting
- `cli.py` - CLI command interface

### Minimal Interfaces

Modules expose only what the driver needs. No speculative features.

### No Premature Abstraction

Started with the simplest implementation. Abstraction added only when justified by actual need (e.g., StorageBackend protocol for testability).

## Data Flow

```
User Input (CLI)
    ↓
CLI Command Handler (cli.py)
    ↓
TaskStore (store.py) - Business logic
    ↓
StorageBackend (storage.py) - Protocol
    ↓
JSONFileBackend (json_backend.py) - Implementation
    ↓
JSON File (~/.task-tracker/tasks.json)

Filtering & Formatting:
TaskStore → TaskFilter → TaskFormatter → CLI Output
```

## Testing Strategy

### Acceptance Tests (30+ scenarios)

- Test complete user workflows end-to-end
- Use real implementations (TaskStore, JSONFileBackend, TaskFilter, TaskFormatter)
- No mocking (all code is under our control)
- Written before implementation (RED)
- All passing (GREEN)
- Cover all 6 requirements from spec

### Unit Tests (complete coverage)

- Test individual module behavior
- Fast and focused
- Written before implementing each module (RED)
- All passing (GREEN)
- Cover edge cases and validation logic

## Development Workflow

This project followed the ATDD workflow:

1. **Wrote acceptance tests first (RED)** - 30+ scenarios in domain language
2. **Identified modules needed** - From driver imports (models, storage, store, etc.)
3. **Wrote unit tests for each module (RED)** - Comprehensive coverage
4. **Implemented minimal code (GREEN)** - All tests passing
5. **Refactored** - Kept tests green throughout
6. **Updated code-index.md** - Documented all modules and functions

## Implementation Complete

The Task Tracker CLI demonstrates a complete ATDD cycle:

- All acceptance tests passing (GREEN)
- All unit tests passing (GREEN)
- Full feature implementation
- Clean four-layer architecture
- Comprehensive documentation

## Future Considerations

As the application grows, consider:

- **Additional features** - Task completion, deletion, editing
- **Advanced filtering** - Date ranges, complex queries
- **Export formats** - CSV, Markdown, HTML
- **Configuration** - Custom storage locations, output formats
- **Performance optimization** - Caching, indexing for large task lists

But don't add these until you need them. Start simple.
