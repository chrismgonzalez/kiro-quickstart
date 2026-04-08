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
2. Write unit tests for every component
3. All tests FAIL - this is the complete RED state
4. Natural session break point

**Phase 2: GREEN - Implement Everything** 5. Implement components one by one 6. Run tests until GREEN 7. Refactor as needed (keep GREEN)

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
  - Create tests/acceptance/test\_<story>.py (Layer 1: test cases)
  - Create tests/acceptance/story_dsl.py (Layer 2: DSL)
  - Create tests/acceptance/system_driver.py (Layer 3: driver)
  - Driver imports define application module structure
  - All tests will FAIL - that's the starting point
  - _Requirements: [all]_

- [ ] 2. Write unit tests for <Component A> (RED)
  - Unit tests: [list specific cases and edge cases]
  - Tests will FAIL - no implementation yet
  - _Requirements: X.Y_

- [ ] 3. Write unit tests for <Component B> (RED)
  - Unit tests: [list specific cases and edge cases]
  - Tests will FAIL - no implementation yet
  - _Requirements: X.Y_

[Continue for all components]

- [ ] N. Checkpoint - Phase 1 Complete (RED state verified)
  - All acceptance tests exist and FAIL
  - All unit tests exist and FAIL
  - Complete RED state achieved
  - **Session break point - user can start new session for Phase 2**

## Phase 2: GREEN - Implement All Components

- [ ] N+1. Implement <Component A> (GREEN)
  - [Implementation details]
  - Run Component A unit tests until GREEN
  - Acceptance tests still RED (expected)
  - _Requirements: X.Y_

- [ ] N+2. Implement <Component B> (GREEN)
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

## Anti-Patterns

### ❌ Wrong: Implementation before tests

```markdown
- [ ] 1. Create data models
- [ ] 2. Write tests for data models
```

### ✅ Correct: All tests in Phase 1, implementation in Phase 2

```markdown
## Phase 1: RED

- [ ] 1. Write tests for data models (RED)

## Phase 2: GREEN

- [ ] 2. Implement data models (GREEN)
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

- [ ] 1. Write tests for Component A (RED)
- [ ] 2. Write tests for Component B (RED)
- [ ] 3. Checkpoint - Phase 1 complete (session break)

## Phase 2: GREEN

- [ ] 4. Implement Component A (GREEN)
- [ ] 5. Implement Component B (GREEN)
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

- [ ] 2. Write tests for JSONFileBackend (RED)
  - Unit tests: persistence, validation, edge cases

## Phase 2: GREEN

- [ ] 5. Implement JSONFileBackend (GREEN)
  - Implement file I/O operations
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
- [ ] 2-4. Write all unit tests (RED)
- [ ] 5. Checkpoint - Phase 1 complete

## Phase 2: GREEN

- [ ] 6-10. Implement components to make tests pass
- [ ] 11. Final checkpoint - all tests GREEN
```

---

## Key Reminders

1. **Two-phase approach** - Phase 1 writes ALL tests (RED), Phase 2 implements ALL components (GREEN)
2. **Session break at phase boundary** - Complete Phase 1, then user can start fresh session for Phase 2
3. **Acceptance tests first** - Scaffold all four layers at start of Phase 1
4. **Driver imports define architecture** - Layer 3 imports show what modules to build
5. **Checkpoints verify state** - Confirm RED state at end of Phase 1, GREEN state at end of Phase 2
6. **Reference requirements** - Each task notes which requirements it satisfies
7. **No interleaving** - Never mix test writing and implementation within a phase

---

## Integration

**Flow:** Design (Gherkin) → Tasks (RED-GREEN sequence) → Implementation (ATDD)

**Works with:**

- `spec-design-construction.md` - Defines WHAT to build
- `atdd` skill - Provides four-layer architecture details
- `development-guide.md` - Provides workflow context
