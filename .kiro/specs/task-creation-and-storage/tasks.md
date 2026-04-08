# Implementation Plan: Task Creation and Storage

## Overview

This implementation follows strict ATDD principles with RED-GREEN-REFACTOR workflow. We start by scaffolding the four-layer acceptance test infrastructure (RED), then build each component by writing tests first (RED) and implementing to make them pass (GREEN). Tests are never optional - they define what "done" means.

## Tasks

- [ ] 1. Scaffold four-layer acceptance test infrastructure (RED)
  - Create tests/acceptance/test_task_creation.py (Layer 1: test cases in domain language)
  - Create tests/acceptance/story_dsl.py (Layer 2: DSL that composes driver operations)
  - Create tests/acceptance/system_driver.py (Layer 3: elementary calls to modules)
  - Translate all Gherkin scenarios from design.md into executable test cases
  - Driver imports define application structure: TaskStore, JSONFileBackend, Task model
  - All acceptance tests will FAIL - this is the starting RED state
  - _Requirements: 1.1-1.6, 2.1-2.6, 4.1-4.5, 5.1-5.5, 6.1-6.5_

- [ ] 2. Implement Task data model and validation (RED-GREEN)
  - [ ] 2.1 Write tests for Task model (RED)
    - Unit tests: Task structure validation, field types, default values
    - Edge cases: empty title, invalid status, special characters, unicode
    - Tests will FAIL - no implementation yet
    - _Requirements: 4.1-4.5_
  - [ ] 2.2 Implement Task TypedDict and validation (GREEN)
    - Create src/task_tracker/models.py with Task TypedDict
    - Implement validation functions for title, status, tags, ID, timestamp
    - Run tests until GREEN
    - _Requirements: 4.1-4.5_

- [ ] 3. Checkpoint - Verify Task model progress
  - Acceptance tests still RED (expected - no storage yet)
  - Task model unit tests GREEN
  - Confirm Task structure matches design.md specification
  - Ask user if questions arise

- [ ] 4. Implement StorageBackend protocol (RED-GREEN)
  - [ ] 4.1 Write tests for StorageBackend protocol (RED)
    - Unit tests: protocol definition, method signatures
    - Tests will FAIL - no implementation yet
    - _Requirements: 3.1-3.2_
  - [ ] 4.2 Implement StorageBackend protocol (GREEN)
    - Create src/task_tracker/storage.py with StorageBackend Protocol
    - Define save_task, load_tasks, get_task_by_id methods
    - Run tests until GREEN
    - _Requirements: 3.1-3.2_

- [ ] 5. Implement JSONFileBackend (RED-GREEN)
  - [ ] 5.1 Write tests for JSONFileBackend (RED)
    - Unit tests: file creation, directory creation, read/write operations
    - Edge cases: missing directory, corrupted JSON, permission errors, empty file
    - Tests will FAIL - no implementation yet
    - _Requirements: 2.1-2.6, 3.2_
  - [ ] 5.2 Implement JSONFileBackend class (GREEN)
    - Create JSONFileBackend implementing StorageBackend protocol
    - Implement file I/O, directory creation, JSON parsing
    - Handle errors: invalid JSON, permissions, missing files
    - Run tests until GREEN
    - _Requirements: 2.1-2.6, 3.2_

- [ ] 6. Checkpoint - Verify storage layer progress
  - Acceptance tests still RED (expected - no TaskStore yet)
  - JSONFileBackend unit tests GREEN
  - StorageBackend protocol tests GREEN
  - Confirm storage can persist and retrieve data
  - Ask user if questions arise

- [ ] 7. Implement TaskStore (RED-GREEN)
  - [ ] 7.1 Write tests for TaskStore (RED)
    - Unit tests: create_task, get_all_tasks, get_task, ID generation
    - Edge cases: empty storage, non-existent IDs, sequential IDs, max ID + 1
    - Tests will FAIL - no implementation yet
    - _Requirements: 1.1-1.6, 5.1-5.5, 6.1-6.5_
  - [ ] 7.2 Implement TaskStore class (GREEN)
    - Create src/task_tracker/store.py with TaskStore class
    - Implement create_task with ID generation and timestamp
    - Implement get_all_tasks and get_task methods
    - Implement \_generate_next_id (max existing ID + 1)
    - Run tests until GREEN
    - _Requirements: 1.1-1.6, 5.1-5.5, 6.1-6.5_

- [ ] 8. Checkpoint - Verify TaskStore progress
  - Some acceptance tests may be GREEN (basic create/retrieve)
  - TaskStore unit tests GREEN
  - Confirm ID generation follows specification (max + 1)
  - Confirm timestamps are ISO format
  - Ask user if questions arise

- [ ] 9. Implement CLI layer (RED-GREEN)
  - [ ] 9.1 Write tests for CLI commands (RED)
    - Unit tests: create command, list command, get command
    - Edge cases: empty title validation, invalid status validation
    - Tests will FAIL - no implementation yet
    - _Requirements: 1.1-1.4, 4.1-4.2, 5.1-5.4_
  - [ ] 9.2 Implement CLI commands (GREEN)
    - Update src/task_tracker/cli.py with Click commands
    - Implement create command with validation
    - Implement list command
    - Implement get command
    - Wire CLI to TaskStore and JSONFileBackend
    - Run tests until GREEN
    - _Requirements: 1.1-1.4, 4.1-4.2, 5.1-5.4_

- [ ] 10. Implement TaskFormatter (RED-GREEN)
  - [ ] 10.1 Write tests for TaskFormatter (RED)
    - Unit tests: format single task, format task list, format empty list
    - Edge cases: long titles, many tags, special characters
    - Tests will FAIL - no implementation yet
    - _Requirements: 5.2_
  - [ ] 10.2 Implement TaskFormatter class (GREEN)
    - Create src/task_tracker/formatter.py
    - Implement format methods for tasks
    - Run tests until GREEN
    - _Requirements: 5.2_

- [ ] 11. Implement TaskFilter (RED-GREEN)
  - [ ] 11.1 Write tests for TaskFilter (RED)
    - Unit tests: filter by status, filter by tags, filter by ID
    - Edge cases: no matches, multiple filters, empty task list
    - Tests will FAIL - no implementation yet
    - _Requirements: 3.4, 5.1-5.4_
  - [ ] 11.2 Implement TaskFilter class (GREEN)
    - Create src/task_tracker/filter.py
    - Implement filtering methods
    - Run tests until GREEN
    - _Requirements: 3.4, 5.1-5.4_

- [ ] 12. Final checkpoint - All tests GREEN
  - Run full test suite: pytest
  - Acceptance tests GREEN (all Gherkin scenarios pass)
  - All unit tests GREEN (all components working)
  - Verify all requirements covered
  - Feature is complete

## Notes

- Tests are NEVER optional - they define what "done" means
- Each component follows RED-GREEN-REFACTOR cycle
- Acceptance tests are scaffolded FIRST to define success criteria
- Checkpoints verify which tests are RED/GREEN at each stage
- Driver imports in Layer 3 define the application architecture
- All tests use real implementations (no mocking internal modules)
