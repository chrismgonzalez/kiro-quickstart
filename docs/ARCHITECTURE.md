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

- `store.py` - Task persistence
- `filter.py` - Task filtering logic
- `formatter.py` - Output formatting

### Minimal Interfaces

Modules expose only what the driver needs. No speculative features.

### No Premature Abstraction

Start with the simplest implementation. Add abstraction only when justified by actual need.

## Data Flow

```
User Input (CLI)
    ↓
CLI Command Handler
    ↓
Application Modules (Store, Filter, Formatter)
    ↓
Storage (JSON file)
```

## Testing Strategy

### Acceptance Tests

- Test complete user workflows end-to-end
- Use real implementations (no mocking)
- Written before implementation (RED)
- Pass when story is complete (GREEN)

### Unit Tests

- Test individual module behavior
- Fast and focused
- Written before implementing each module (RED)
- Pass when module is complete (GREEN)

## Development Workflow

1. **Write acceptance test** (Layer 1) - Fails (RED)
2. **Identify modules needed** - Look at driver imports
3. **Write unit tests** for each module - Fails (RED)
4. **Implement minimal code** - Tests pass (GREEN)
5. **Refactor** - Keep tests green
6. **Update code-index.md** - Document new modules

## Future Considerations

As the application grows, consider:

- **Dependency injection** - When modules need configuration
- **Interface segregation** - When modules have multiple clients
- **Event-driven architecture** - When modules need to react to changes
- **Caching layer** - When performance becomes critical

But don't add these until you need them. Start simple.
