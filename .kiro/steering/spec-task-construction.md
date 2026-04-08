---
inclusion: fileMatch
fileMatchPattern: ["**/tasks.md"]
description: Guide for constructing spec tasks.md files following strict ATDD principles with RED-GREEN-REFACTOR workflow
---

# Spec Task Construction Guide

## Core Principle: Two-Phase ATDD

Every spec follows a **TWO-PHASE** approach:

**Phase 1: RED - Write ALL Tests**

1. Scaffold acceptance test infrastructure (all 4 layers)
2. Create module stubs (empty classes, functions with `pass` or `raise NotImplementedError`)
3. Write unit tests for every component
4. All tests FAIL - this is the complete RED state
5. Natural session break point

**Phase 2: GREEN - Implement Everything** 6. Implement components one by one 7. Run tests until GREEN 8. Refactor as needed (keep GREEN)

## Critical Rules

1. **ALL tests in Phase 1** - Complete RED state before any implementation
2. **ALL implementation in Phase 2** - Make tests GREEN one component at a time
3. **Tests are NEVER optional** - No `*` markers on test tasks
4. **Phase boundary is a session break** - User can start fresh for implementation
5. **Checkpoints verify test status** - Confirm RED/GREEN state at phase boundaries

---

## Task Structure Template

```markdown
# Implementation Plan: <Feature Name>

## Overview

[Brief description of feature and ATDD approach]

## Phase 1: RED - Write All Tests

- [ ] 1. Scaffold four-layer acceptance test infrastructure (RED)
  - Create tests/acceptance/test\_<story>.py (Layer 1: test cases using namespace pattern)
  - Create tests/acceptance/story_dsl.py (Layer 2: DSL with given/when/then namespaces)
  - Create tests/acceptance/system_driver.py (Layer 3: driver)
  - Use namespace pattern: `given.*`, `when.*`, `then.*` methods
  - State flows through tests via return values
  - Driver imports define application module structure
  - All tests will FAIL - that's the starting point
  - _Requirements: [all]_

- [ ] 2. Create module stubs for all components (RED)
  - Create src/<package>/<module_a>.py with empty classes/functions
  - Use `pass` or `raise NotImplementedError` for method bodies
  - Ensures imports resolve and tests can run
  - Establishes true RED state (tests run but fail)
  - _Requirements: [all]_

- [ ] 3. Write unit tests for <Component A> (RED)
  - Unit tests: [list specific cases and edge cases]
  - Tests will FAIL - no implementation yet
  - _Requirements: X.Y_

- [ ] 4. Write unit tests for <Component B> (RED)
  - Unit tests: [list specific cases and edge cases]
  - Tests will FAIL - no implementation yet
  - _Requirements: X.Y_

[Continue for all components]

- [ ] N. Checkpoint - Phase 1 Complete (RED state verified)
  - All acceptance tests exist and FAIL
  - All unit tests exist and FAIL
  - All modules exist as stubs (imports resolve)
  - Complete RED state achieved
  - **Session break point - user can start new session for Phase 2**

## Phase 2: GREEN - Implement All Components

- [ ] N+1. Implement <Component A> (GREEN)
  - Replace stub with real implementation
  - [Implementation details]
  - Run Component A unit tests until GREEN
  - Acceptance tests still RED (expected)
  - _Requirements: X.Y_

- [ ] N+2. Implement <Component B> (GREEN)
  - Replace stub with real implementation
  - [Implementation details]
  - Run Component B unit tests until GREEN
  - Acceptance tests may start passing
  - _Requirements: X.Y_

[Continue for all components]

- [ ] M. Final checkpoint - All tests GREEN
  - Run full test suite
  - Acceptance tests GREEN (story complete)
  - All unit tests GREEN
  - Feature is done
```

---

## Namespace Pattern Example

### Layer 1: Test Case (Namespace Pattern)

```python
def test_user_creates_task_with_title(given, when, then):
    """Scenario: User creates task with title
    Given the task tracker is ready
    When the user creates a task with title "Write documentation"
    Then a task exists with title "Write documentation"
    """
    tracker = given.task_tracker_is_ready()
    tracker = when.user_creates_task(tracker, "Write documentation")
    then.task_exists_with_title(tracker, "Write documentation")
```

### Layer 2: DSL (Namespace Implementation)

```python
class StoryDsl:
    def __init__(self):
        self.driver = SystemDriver()

    # given: set up world state
    def task_tracker_is_ready(self):
        self.driver.clear_all_tasks()
        return {"tasks": [], "next_id": 1}

    # when: perform actions (compose driver calls)
    def user_creates_task(self, tracker, title):
        task = self.driver.create_task(title)
        tracker["tasks"].append(task)
        tracker["next_id"] += 1
        return tracker

    # then: make assertions
    def task_exists_with_title(self, tracker, title):
        matching = [t for t in tracker["tasks"] if t["title"] == title]
        assert len(matching) == 1, f"Expected 1 task with title '{title}', found {len(matching)}"

# Create namespace aliases
dsl = StoryDsl()
given = when = then = dsl
```

### Layer 3: Protocol Driver

```python
from task_tracker.store import TaskStore

class SystemDriver:
    def __init__(self):
        self.store = TaskStore()

    def clear_all_tasks(self):
        self.store.clear()

    def create_task(self, title: str) -> dict:
        return self.store.create(title=title)
```

---

## Anti-Patterns

### ❌ Wrong: Method prefix pattern (verbose, less reusable)

```python
def test_create_task_with_title_only(story: TaskStory):
    story.given_a_fresh_task_tracker()
    story.when_i_create_a_task_with_title("Buy groceries")
    story.then_the_task_should_be_stored_with_status("pending")
```

### ✅ Correct: Namespace pattern (clean, composable)

```python
def test_user_creates_task_with_title(given, when, then):
    """Scenario: User creates task with title
    Given the task tracker is ready
    When the user creates a task with title "Buy groceries"
    Then the task should be stored with status "pending"
    """
    tracker = given.task_tracker_is_ready()
    tracker = when.user_creates_task(tracker, "Buy groceries")
    then.task_has_status(tracker, "pending")
```

### ❌ Wrong: Implementation before tests

```markdown
- [ ] 1. Create data models
- [ ] 2. Write tests for data models
```

### ✅ Correct: All tests in Phase 1, implementation in Phase 2

```markdown
## Phase 1: RED

- [ ] 1. Create module stubs (RED)
- [ ] 2. Write tests for data models (RED)

## Phase 2: GREEN

- [ ] 3. Implement data models (GREEN)
```

### ❌ Wrong: Interleaving tests and implementation

```markdown
- [ ] 1. Write tests for Component A (RED)
- [ ] 2. Implement Component A (GREEN)
- [ ] 3. Write tests for Component B (RED)
- [ ] 4. Implement Component B (GREEN)
```

### ✅ Correct: Complete Phase 1, then Phase 2

```markdown
## Phase 1: RED

- [ ] 1. Create module stubs (RED)
- [ ] 2. Write tests for Component A (RED)
- [ ] 3. Write tests for Component B (RED)
- [ ] 4. Checkpoint - Phase 1 complete (session break)

## Phase 2: GREEN

- [ ] 5. Implement Component A (GREEN)
- [ ] 6. Implement Component B (GREEN)
```

### ❌ Wrong: Mixed test/implementation in same task

```markdown
- [ ] 2. Implement JSONFileBackend
  - [ ] 2.1 Implement class with file I/O
  - [ ]\* 2.2 Write tests (optional)
```

### ✅ Correct: Test in Phase 1, implementation in Phase 2

```markdown
## Phase 1: RED

- [ ] 2. Create JSONFileBackend stub (RED)
  - Empty class with method signatures
  - Methods raise NotImplementedError

- [ ] 3. Write tests for JSONFileBackend (RED)
  - Unit tests: persistence, validation, edge cases

## Phase 2: GREEN

- [ ] 5. Implement JSONFileBackend (GREEN)
  - Replace NotImplementedError with real file I/O
  - Run tests until GREEN
```

### ❌ Wrong: Acceptance tests at the end

```markdown
- [ ] 1-6. Implement all components
- [ ] 7. Write acceptance tests
```

### ✅ Correct: Acceptance tests first in Phase 1

```markdown
## Phase 1: RED

- [ ] 1. Scaffold acceptance tests (RED)
- [ ] 2. Create all module stubs (RED)
- [ ] 3-6. Write all unit tests (RED)
- [ ] 7. Checkpoint - Phase 1 complete

## Phase 2: GREEN

- [ ] 8-12. Implement components to make tests pass
- [ ] 13. Final checkpoint - all tests GREEN
```

---

## Key Reminders

1. **Two-phase approach** - Phase 1 writes ALL tests (RED), Phase 2 implements ALL components (GREEN)
2. **Module stubs enable true RED** - Create empty classes/functions with `pass` or `raise NotImplementedError` so imports resolve and tests can run
3. **Session break at phase boundary** - Complete Phase 1, then user can start fresh session for Phase 2
4. **Acceptance tests first** - Scaffold all four layers at start of Phase 1
5. **Driver imports define architecture** - Layer 3 imports show what modules to build
6. **Checkpoints verify state** - Confirm RED state at end of Phase 1, GREEN state at end of Phase 2
7. **Reference requirements** - Each task notes which requirements it satisfies
8. **No interleaving** - Never mix test writing and implementation within a phase

---

## Integration

**Flow:** Design (Gherkin) → Tasks (RED-GREEN sequence) → Implementation (ATDD)

**Works with:**

- `spec-design-construction.md` - Defines WHAT to build
- `atdd` skill - Provides four-layer architecture details
- `development-guide.md` - Provides workflow context
