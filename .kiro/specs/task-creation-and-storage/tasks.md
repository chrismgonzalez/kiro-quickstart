# Implementation Plan: Task Creation and Storage

## Overview

This implementation follows strict ATDD principles with a two-phase approach. Phase 1 writes ALL tests (complete RED state), then Phase 2 implements ALL components (GREEN state). The phase boundary is a natural session break point.

## Phase 1: RED - Write All Tests

- [x] 1. Scaffold four-layer acceptance test infrastructure (RED)
  - Create tests/acceptance/test_task_creation.py (Layer 1: test cases using namespace pattern)
  - Create tests/acceptance/story_dsl.py (Layer 2: DSL with given/when/then namespaces)
  - Create tests/acceptance/system_driver.py (Layer 3: elementary calls to modules)
  - Use namespace pattern: `given.*`, `when.*`, `then.*` methods
  - State flows through tests via return values
  - Translate all Gherkin scenarios from design.md into executable test cases
  - Driver imports define application structure: TaskStore, JSONFileBackend, Task model
  - All acceptance tests will FAIL - this is the starting RED state
  - _Requirements: 1.1-1.6, 2.1-2.6, 4.1-4.5, 5.1-5.5, 6.1-6.5_

- [x] 2. Create module stubs for all components (RED)
  - Create src/task_tracker/models.py with Task TypedDict and validation function stubs
  - Create src/task_tracker/storage.py with StorageBackend Protocol definition
  - Create src/task_tracker/store.py with TaskStore class (methods raise NotImplementedError)
  - Create src/task_tracker/json_backend.py with JSONFileBackend class (methods raise NotImplementedError)
  - Create src/task_tracker/formatter.py with TaskFormatter class (methods raise NotImplementedError)
  - Create src/task_tracker/filter.py with TaskFilter class (methods raise NotImplementedError)
  - Ensures imports resolve and tests can run
  - Establishes true RED state (tests run but fail)
  - _Requirements: 1.1-1.6, 2.1-2.6, 3.1-3.5, 4.1-4.5, 5.1-5.5, 6.1-6.5_

- [x] 3. Write unit tests for Task model (RED)
  - Unit tests: Task structure validation, field types, default values
  - Edge cases: empty title, invalid status, special characters, unicode
  - Tests will FAIL - no implementation yet
  - _Requirements: 4.1-4.5_

- [x] 4. Write unit tests for StorageBackend protocol (RED)
  - Unit tests: protocol definition, method signatures
  - Tests will FAIL - no implementation yet
  - _Requirements: 3.1-3.2_

- [x] 5. Write unit tests for JSONFileBackend (RED)
  - Unit tests: file creation, directory creation, read/write operations
  - Edge cases: missing directory, corrupted JSON, permission errors, empty file
  - Tests will FAIL - no implementation yet
  - _Requirements: 2.1-2.6, 3.2_

- [x] 6. Write unit tests for TaskStore (RED)
  - Unit tests: create_task, get_all_tasks, get_task, ID generation
  - Edge cases: empty storage, non-existent IDs, sequential IDs, max ID + 1
  - Tests will FAIL - no implementation yet
  - _Requirements: 1.1-1.6, 5.1-5.5, 6.1-6.5_

- [x] 7. Write unit tests for CLI commands (RED)
  - Unit tests: create command, list command, get command
  - Edge cases: empty title validation, invalid status validation
  - Tests will FAIL - no implementation yet
  - _Requirements: 1.1-1.4, 4.1-4.2, 5.1-5.4_

- [x] 8. Write unit tests for TaskFormatter (RED)
  - Unit tests: format single task, format task list, format empty list
  - Edge cases: long titles, many tags, special characters
  - Tests will FAIL - no implementation yet
  - _Requirements: 5.2_

- [x] 9. Write unit tests for TaskFilter (RED)
  - Unit tests: filter by status, filter by tags, filter by ID
  - Edge cases: no matches, multiple filters, empty task list
  - Tests will FAIL - no implementation yet
  - _Requirements: 3.4, 5.1-5.4_

- [x] 10. Checkpoint - Phase 1 Complete (RED state verified)
  - All acceptance tests exist and FAIL
  - All unit tests exist and FAIL
  - All modules exist as stubs (imports resolve)
  - Complete RED state achieved
  - **Session break point - user can start new session for Phase 2**

## Phase 2: GREEN - Implement All Components

- [x] 11. Implement Task data model and validation (GREEN)
  - Replace stubs in src/task_tracker/models.py with real implementations
  - Implement validation functions for title, status, tags, ID, timestamp
  - Run Task model unit tests until GREEN
  - Acceptance tests still RED (expected)
  - _Requirements: 4.1-4.5_

- [x] 12. Implement StorageBackend protocol (GREEN)
  - Verify src/task_tracker/storage.py StorageBackend Protocol is complete
  - Protocol definition should already be complete from Phase 1
  - Run StorageBackend unit tests until GREEN
  - Acceptance tests still RED (expected)
  - _Requirements: 3.1-3.2_

- [x] 13. Implement JSONFileBackend (GREEN)
  - Replace NotImplementedError stubs in JSONFileBackend with real implementation
  - Implement file I/O, directory creation, JSON parsing
  - Handle errors: invalid JSON, permissions, missing files
  - Run JSONFileBackend unit tests until GREEN
  - Acceptance tests still RED (expected)
  - _Requirements: 2.1-2.6, 3.2_

- [x] 14. Implement TaskStore (GREEN)
  - Replace NotImplementedError stubs in TaskStore with real implementation
  - Implement create_task with ID generation and timestamp
  - Implement get_all_tasks and get_task methods
  - Implement \_generate_next_id (max existing ID + 1)
  - Run TaskStore unit tests until GREEN
  - Some acceptance tests may start passing
  - _Requirements: 1.1-1.6, 5.1-5.5, 6.1-6.5_

- [x] 15. Implement CLI layer (GREEN)
  - Update src/task_tracker/cli.py with Click commands
  - Implement create command with validation
  - Implement list command
  - Implement get command
  - Wire CLI to TaskStore and JSONFileBackend
  - Run CLI unit tests until GREEN
  - More acceptance tests may pass
  - _Requirements: 1.1-1.4, 4.1-4.2, 5.1-5.4_

- [x] 16. Implement TaskFormatter (GREEN)
  - Replace NotImplementedError stubs in TaskFormatter with real implementation
  - Implement format methods for tasks
  - Run TaskFormatter unit tests until GREEN
  - Acceptance tests may pass
  - _Requirements: 5.2_

- [x] 17. Implement TaskFilter (GREEN)
  - Replace NotImplementedError stubs in TaskFilter with real implementation
  - Implement filtering methods
  - Run TaskFilter unit tests until GREEN
  - Acceptance tests may pass
  - _Requirements: 3.4, 5.1-5.4_

- [x] 18. Final checkpoint - All tests GREEN
  - Run full test suite: pytest
  - Acceptance tests GREEN (all Gherkin scenarios pass)
  - All unit tests GREEN (all components working)
  - Verify all requirements covered
  - Feature is complete

## Notes

- Phase 1 writes ALL tests (complete RED state)
- Module stubs created in Phase 1 ensure imports resolve and tests can run
- Phase 2 implements ALL components (GREEN state)
- Session break at phase boundary (after task 10)
- Tests are NEVER optional - they define what "done" means
- Acceptance tests are scaffolded FIRST to define success criteria
- Driver imports in Layer 3 define the application architecture
- All tests use real implementations (no mocking internal modules)
