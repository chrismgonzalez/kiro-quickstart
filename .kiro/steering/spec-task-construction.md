---
inclusion: manual
description: Guide for constructing spec tasks.md files following strict ATDD principles with RED-GREEN-REFACTOR workflow
---

# Spec Task Construction Guide

## Core Principle: Tests First, Always

Every task follows **RED-GREEN-REFACTOR**:

1. Write the test (RED - it fails)
2. Write minimal implementation (GREEN - it passes)
3. Refactor if needed (keep it GREEN)

## Critical Rules

1. **Acceptance tests FIRST** - They define what "done" means
2. **Test subtask before implementation subtask** - Always RED then GREEN
3. **Tests are NEVER optional** - No `*` markers on test tasks
4. **Checkpoints verify test status** - Not just "run tests"

---

## Task Structure Template

```markdown
# Implementation Plan: <Feature Name>

## Overview

[Brief description of feature and ATDD approach]

## Tasks

- [ ] 1. Scaffold four-layer acceptance test infrastructure (RED)
  - Create tests/acceptance/test\_<story>.py (Layer 1: test cases)
  - Create tests/acceptance/story_dsl.py (Layer 2: DSL)
  - Create tests/acceptance/system_driver.py (Layer 3: driver)
  - Driver imports define application module structure
  - All tests will FAIL - that's the starting point
  - _Requirements: [all]_

- [ ] 2. Implement <Component A> (RED-GREEN)
  - [ ] 2.1 Write tests for <Component A> (RED)
    - Unit tests: [list specific cases and edge cases]
    - Tests will FAIL
    - _Requirements: X.Y_
  - [ ] 2.2 Implement <Component A> (GREEN)
    - [Implementation details]
    - Run tests until GREEN
    - _Requirements: X.Y_

- [ ] 3. Checkpoint - Verify progress
  - Acceptance tests still RED (expected)
  - Component A unit tests GREEN
  - Ask user if questions arise

- [ ] 4. Implement <Component B> (RED-GREEN)
  - [ ] 4.1 Write tests for <Component B> (RED)
    - [Test details]
  - [ ] 4.2 Implement <Component B> (GREEN)
    - [Implementation details]

[Continue pattern for all components]

- [ ] N. Final checkpoint - All tests GREEN
  - Run full test suite
  - Acceptance tests GREEN (story complete)
  - All unit tests GREEN
  - Feature is done
```

---

## Anti-Patterns

### ❌ Wrong: Implementation before tests

```markdown
- [ ] 1. Create data models
- [ ] 2. Write tests for data models
```

### ✅ Correct: Tests before implementation

```markdown
- [ ] 1. Write tests for data models (RED)
  - Unit tests will fail - no implementation yet
- [ ] 2. Implement data models (GREEN)
  - Run tests until they pass
```

### ❌ Wrong: Mixed test/implementation in same task

```markdown
- [ ] 2. Implement JSONFileBackend
  - [ ] 2.1 Implement class with file I/O
  - [ ]\* 2.2 Write tests (optional)
```

### ✅ Correct: Test subtask, then implementation subtask

```markdown
- [ ] 2. Implement JSONFileBackend (RED-GREEN)
  - [ ] 2.1 Write tests for JSONFileBackend (RED)
    - Unit tests: persistence, validation, edge cases
    - Tests will FAIL
  - [ ] 2.2 Implement JSONFileBackend (GREEN)
    - Implement file I/O operations
    - Run tests until GREEN
```

### ❌ Wrong: Acceptance tests at the end

```markdown
- [ ] 1-6. Implement all components
- [ ] 7. Write acceptance tests
```

### ✅ Correct: Acceptance tests first

```markdown
- [ ] 1. Scaffold acceptance tests (RED)
  - Tests define what "done" means
- [ ] 2-7. Implement components to make tests pass
- [ ] 8. Final checkpoint - acceptance tests GREEN
```

---

## Key Reminders

1. **Acceptance tests first** - Scaffold all four layers before any implementation
2. **RED → GREEN → REFACTOR** - Each component follows this cycle
3. **Driver imports define architecture** - Layer 3 imports show what modules to build
4. **Checkpoints verify state** - Confirm which tests are RED/GREEN
5. **Reference requirements** - Each task notes which requirements it satisfies

---

## Integration

**Flow:** Design (Gherkin) → Tasks (RED-GREEN sequence) → Implementation (ATDD)

**Works with:**

- `spec-design-construction.md` - Defines WHAT to build
- `atdd` skill - Provides four-layer architecture details
- `development-guide.md` - Provides workflow context
