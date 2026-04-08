# Development Guide

## Quick Start

```sh
uv sync                    # install dependencies
uv run pytest              # run all tests
uv run pytest -v           # verbose test output
uv run pytest tests/acceptance/  # acceptance tests only
uv run pytest tests/unit/        # unit tests only
uv run task-tracker --help       # CLI help
```

## Codebase Index

When searching the code during research, debugging, or implementation, read `code-index.md` (steering) — it maps every component, function, and utility to its exact file and location.

## Development Guidelines

1. All production code must have a test. Prefer acceptance tests that describe behavior in Gherkin format. Unit tests are for isolated logic too granular for acceptance tests.

2. Tests first. Write or update the test before writing implementation code. If a behavior changes, update the test first, then make it pass. Follow the red-green-refactor cycle.

3. Author the simplest implementation that works. Do not over-engineer. Start with the simplest code that is correct, readable, and easy to extend. Avoid abstractions not justified by a current need.

4. Do not rewrite complete files — only fix what needs to be fixed.

5. No need for abundant comments or summary documentation unless asked.

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

- Use the four-layer architecture (test cases → DSL → protocol driver → SUT)
- Test cases in plain domain language (no HTTP, no JSON, no file paths)
- DSL methods compose driver calls (no single-line proxies)
- Driver methods are elementary (one module call per method)
- Use real implementations, mock only external third parties

## File Structure

```
src/task_tracker/
  cli.py           # Click CLI interface
  store.py         # Task persistence (JSON file)
  filter.py        # Task filtering logic
  formatter.py     # Output formatting

tests/acceptance/
  test_*.py        # Layer 1: Test cases
  story_dsl.py     # Layer 2: Domain-specific language
  system_driver.py # Layer 3: Protocol driver

tests/unit/
  test_*.py        # Unit tests for individual modules
```

## Naming Conventions

- Modules: snake_case (`task_store.py`)
- Classes: PascalCase (`TaskStore`)
- Functions: snake_case (`create_task`)
- Constants: UPPER_SNAKE_CASE (`DEFAULT_STATUS`)
- Test files: `test_<module>.py`
- Test functions: `test_<behavior>`

## Adding New Features

1. Write acceptance test first (RED)
2. Run test to confirm it fails
3. Identify modules needed (look at driver imports)
4. Write unit tests for each module (RED)
5. Implement minimal code (GREEN)
6. Refactor if needed
7. Update code-index.md

## Common Commands

```sh
# Development
uv sync                          # install/update dependencies
uv add <package>                 # add new dependency
uv run python -m task_tracker.cli  # run CLI directly

# Testing
uv run pytest                    # all tests
uv run pytest -k "test_add"      # tests matching pattern
uv run pytest --lf               # last failed tests
uv run pytest -x                 # stop on first failure

# CLI Usage
uv run task-tracker add "Task title" --tags tag1,tag2
uv run task-tracker list
uv run task-tracker list --tag testing
uv run task-tracker complete 1
uv run task-tracker delete 1
```
