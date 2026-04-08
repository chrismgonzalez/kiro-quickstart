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

_This section will be populated as modules are implemented._

### Planned Structure

```
src/task_tracker/
  cli.py           # CLI interface (Click)
  store.py         # Task persistence
  filter.py        # Task filtering logic
  formatter.py     # Output formatting

tests/acceptance/
  test_*.py        # Layer 1: Test cases
  story_dsl.py     # Layer 2: Domain-specific language
  system_driver.py # Layer 3: Protocol driver

tests/unit/
  test_*.py        # Unit tests for individual modules
```

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
