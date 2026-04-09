---
description: Core development workflow, coding standards, ATDD principles, and common commands for the Task Tracker CLI project
---

# Development Guide

## Codebase Index

When searching the code during research, debugging, or implementation, read `code-index.md` (steering) — it maps every component, function, and utility to its exact file and location.

## Spec Construction

When creating or reviewing specs:

- **design.md**: Read `spec-design-construction.md` (steering) — translate EARS requirements into Gherkin behaviors, then add technical design details.
- **tasks.md**: Read `spec-task-construction.md` (steering) — follow strict ATDD ordering: acceptance tests first, then RED-GREEN-REFACTOR for each component

## Development Guidelines

1. All production code must have a test. Prefer acceptance tests that describe behavior in Gherkin format. Unit tests are for isolated logic too granular for acceptance tests.

2. Tests first. Write or update the test before writing implementation code. If a behavior changes, update the test first, then make it pass. Follow the red-green-refactor cycle.

3. All tests must follow the four-layer architecture from the atdd skill:
   - **Layer 1 (Test Cases)**: Written in pure domain language. No HTTP, JSON, database, or technical details. Could be read by a non-technical stakeholder.
   - **Layer 2 (DSL)**: Composes driver operations into scenarios. DSL methods must compose multiple driver calls, not proxy single calls. Holds all assertions in domain terms.
   - **Layer 3 (Protocol Driver)**: Elementary operations on application modules. Each method calls exactly one module. Driver imports define the application's module structure.
   - **Layer 4 (System Under Test)**: Real application modules. Use real implementations, mock only external third parties you don't control.

4. Author the simplest implementation that works. Do not over-engineer. Start with the simplest code that is correct, readable, and easy to extend. Avoid abstractions not justified by a current need.

5. Do not rewrite complete files — only fix what needs to be fixed.

6. No need for abundant comments or summary documentation unless asked.

## Technology Stack

- Language: Python 3.11+
- Package manager: uv
- CLI framework: Click
- Testing: pytest
- Storage: JSON file

## Coding Standards

### Python

- Type hints for function signatures
- Docstrings for public functions and classes
- PEP 8 style (use `black` if available)
- Explicit is better than implicit

### Testing

All tests must follow the four-layer architecture from the `atdd` skill:

- **Layer 1 (Test Cases)**: Executable specifications in plain domain language
  - Use the namespace pattern: `given.*`, `when.*`, `then.*` methods
  - State flows through tests via return values (e.g., `user = given.a_user_at_the_store()`)
  - No HTTP, JSON, database, SQL, or technical details
  - Use language from the user story ("create task", not "POST /tasks")
  - Could be read by a non-technical stakeholder
  - Docstring describes scenario in Gherkin format
- **Layer 2 (DSL)**: Domain-specific language that composes driver operations
  - Single DSL class with `given`, `when`, `then` as aliases to the same instance
  - `given.*` methods set up world state and return state objects
  - `when.*` methods perform actions, accept and return state objects
  - `then.*` methods make assertions on state objects
  - Methods named after user actions, not system interactions
  - Must compose multiple driver calls — never single-line proxies
  - Holds all assertions in domain terms (no HTTP codes, no JSON field names)
- **Layer 3 (Protocol Driver)**: Elementary operations on application modules
  - Each method calls exactly one module (one responsibility)
  - Driver imports define the application's module structure
  - Minimal mocking (see mocking policy below)
- **Layer 4 (System Under Test)**: Real application modules
  - For acceptance tests: application modules called directly (not HTTP server)
  - For unit tests: individual module under test

**Mocking Policy:**

- Your own modules: Use real implementations
- AWS services (DynamoDB, S3, etc.): Use real via moto/localstack
- File system, temp data: Use real (temp files, tmp dirs)
- External OAuth, payment gateways, third-party APIs: Mock (not under your control)

**Critical Rule:** If a DSL `when` method has a single line calling the driver, the driver is doing too much. Composition of steps belongs in the DSL, not hidden inside the driver.

## File Structure

```
src/task_tracker/
  __init__.py      # Package initialization
  models.py        # Task data model and validation
  storage.py       # Storage backend protocol
  json_backend.py  # JSON file storage implementation
  store.py         # Task business logic with ID generation
  filter.py        # Task filtering logic
  formatter.py     # Output formatting
  cli.py           # Click CLI interface (create, list, get commands)

tests/
  test_smoke.py    # Infrastructure smoke tests
  acceptance/      # Layer 1 & 2: Test cases and DSL (30+ scenarios)
  unit/            # Unit tests for all modules
```

## Naming Conventions

- Modules: snake_case (`task_store.py`)
- Classes: PascalCase (`TaskStore`)
- Functions: snake_case (`create_task`)
- Constants: UPPER_SNAKE_CASE (`DEFAULT_STATUS`)
- Test files: `test_<module>.py`
- Test functions: `test_<behavior>`

## Adding New Features

Follow the ATDD workflow from the `atdd` skill:

1. **Write acceptance test first (RED)**
   - Layer 1: Test case in domain language
   - Layer 2: DSL methods that compose driver calls
   - Layer 3: Protocol driver with elementary module calls
   - Driver imports define what modules you'll need to build
   - Test will fail — that's the point

2. **Run test to confirm it fails** (RED state confirmed)

3. **Identify modules needed** (look at driver imports in Layer 3)

4. **For each module, write unit tests first (RED)**
   - Test specific examples and edge cases
   - Tests will fail — no implementation yet

5. **Implement minimal code (GREEN)**
   - Write simplest implementation to pass tests
   - Run tests until they pass

6. **Refactor if needed** (keep tests GREEN)

7. **Update code-index.md** with new modules and functions

## Common Commands

```sh
# Development
make install                     # install/update dependencies
make run                         # run the CLI
make run ARGS="--help"           # run with arguments
make clean                       # remove generated files
uv sync                          # install/update dependencies
uv add <package>                 # add new dependency

# Testing
make test                        # all tests
make test-unit                   # unit tests only
make test-acceptance             # acceptance tests only
uv run pytest                    # all tests
uv run pytest -k "test_add"      # tests matching pattern
uv run pytest --lf               # last failed tests
uv run pytest -x                 # stop on first failure

# CLI Usage
uv run task-tracker create "Write tests"              # create task
uv run task-tracker create "Deploy" --tag urgent      # create with tag
uv run task-tracker create "Done" --status complete   # create complete
uv run task-tracker list                              # list all tasks
uv run task-tracker list --status pending             # filter by status
uv run task-tracker list --tag urgent                 # filter by tag
uv run task-tracker get 1                             # get task by ID
uv run task-tracker --help                            # show help
uv run task-tracker --version                         # show version
```
