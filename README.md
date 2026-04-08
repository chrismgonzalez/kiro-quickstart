# Kiro Quickstart

Template repository for CodeStock talk - "What the Spec! Battle Tested Practices for Spec Driven Development using Kiro"

This repository demonstrates ATDD (Acceptance Test-Driven Development) and spec-driven development using Kiro, featuring a Task Tracker CLI proof-of-concept.

## What's Inside

This repository contains:

1. **Task Tracker CLI** - A working POC demonstrating the four-layer ATDD architecture
2. **Kiro Configuration** - Steering documents, skills, and hooks for guided development
3. **Complete Test Suite** - Acceptance and unit tests following ATDD principles
4. **Documentation** - Comprehensive guides for development, testing, and architecture

## Quick Start

```bash
# Install dependencies
make install

# Run tests
make test

# Use the CLI
uv run task-tracker
# or
make run
```

## Task Tracker CLI

A proof-of-concept CLI demonstrating ATDD with the four-layer architecture. Currently a minimal "Hello World" implementation - features will be added using spec-driven development.

### What This Will Demonstrate

1. **ATDD Four-Layer Architecture**
   - Layer 1: Test cases in plain domain language
   - Layer 2: DSL that composes driver operations
   - Layer 3: Protocol driver with elementary module calls
   - Layer 4: Application modules (to be implemented via specs)

2. **Steering Documents**
   - Development guide with standards and quick commands
   - Code index mapping every module and function
   - Testing guide for quick ATDD reference

3. **Spec-Driven Development**
   - Features defined in `.kiro/specs/`
   - Acceptance tests written before implementation (RED)
   - Module boundaries derived from driver imports
   - Unit tests for each module
   - Red-green-refactor cycle

## Project Structure

```
kiro-quickstart/
├── .kiro/                    # Kiro configuration
│   ├── skills/               # On-demand guidance
│   │   ├── atdd.md          # Four-layer architecture guide
│   │   └── docs.md          # Documentation sync skill
│   ├── steering/             # Always-on context
│   │   ├── development-guide.md
│   │   ├── code-index.md
│   │   └── testing-guide.md
│   ├── specs/                # Spec-driven development
│   │   └── task-tracker-cli-poc/
│   └── hooks/                # Automation (to be added)
├── src/
│   └── task_tracker/
│       ├── __init__.py      # Package initialization
│       └── cli.py           # CLI interface (hello world)
├── tests/
│   ├── acceptance/          # Story-level tests (ready for spec)
│   ├── unit/                # Component-level tests (ready for spec)
│   └── test_smoke.py        # Infrastructure smoke tests
├── Makefile                 # Development commands
└── pyproject.toml           # Project configuration
```

## Development Workflow

1. **Start with an acceptance test** (RED)
2. **Derive module boundaries** from driver imports
3. **Write unit tests** for each module (RED)
4. **Implement** minimal code (GREEN)
5. **Refactor** while keeping tests green
6. **Update code-index.md** when adding modules

## Key Concepts

### Four-Layer Architecture

The acceptance tests are organized into four distinct layers:

**Layer 1 - Test Cases** (`test_add_task_story.py`):

```python
def test_user_adds_task_with_tags():
    user = given.a_user_with_empty_task_list()
    when.user_adds_task(user, "Write tests", tags=["testing"])
    then.task_appears_in_list(user, "Write tests")
```

**Layer 2 - DSL** (`story_dsl.py`):

```python
def user_adds_task(self, user, title, tags=None):
    task = self.driver.create_task(title, tags)
    self.driver.save_task(user, task)
    return user
```

**Layer 3 - Protocol Driver** (`system_driver.py`):

```python
def create_task(self, title, tags=None):
    from task_tracker.store import TaskStore
    store = TaskStore()
    return store.create(title=title, tags=tags or [])
```

**Layer 4 - System Under Test** (application modules):

```python
# task_tracker/store.py
class TaskStore:
    def create(self, title, tags):
        # Implementation
```

### Why This Matters

- **Tests drive design**: Module boundaries emerge from what the driver needs to call
- **Tests are documentation**: Layer 1 reads like a specification
- **Tests are maintainable**: Changes to implementation don't break tests
- **Tests are fast**: Real modules, minimal mocking

## Extending This POC

Try adding these features using ATDD:

1. **Task priorities**: Add high/medium/low priority levels
2. **Due dates**: Add and filter by due dates
3. **Task notes**: Add detailed notes to tasks
4. **Export**: Export tasks to JSON/CSV
5. **Search**: Full-text search across tasks

For each feature:

1. Write the acceptance test first (it will fail)
2. Let the driver imports tell you what modules to create
3. Write unit tests for new modules
4. Implement and watch tests go green
5. Update the code index

## Learning Resources

- Read `.kiro/skills/atdd.md` for comprehensive ATDD guidance
- Check `.kiro/steering/code-index.md` to navigate the codebase
- See `.kiro/steering/testing-guide.md` for quick testing reference
- Review `.kiro/steering/development-guide.md` for coding standards
- Read `docs/ARCHITECTURE.md` for four-layer architecture deep dive
- See `docs/MAKEFILE.md` for Makefile command reference

## Technology Stack

- **Language**: Python 3.11+
- **Package Manager**: uv
- **CLI Framework**: Click
- **Testing**: pytest
- **Storage**: JSON file

## Common Commands

```bash
# Development
make install                     # install/update dependencies
make run                         # run the CLI
make run ARGS="--help"           # run with arguments
uv sync                          # install/update dependencies
uv add <package>                 # add new dependency

# Testing
make test                        # all tests
make test-unit                   # unit tests only
make test-acceptance             # acceptance tests only
uv run pytest                    # all tests
uv run pytest -v                 # verbose output
uv run pytest -k "test_add"      # tests matching pattern
uv run pytest --lf               # last failed tests
uv run pytest -x                 # stop on first failure

# CLI Usage (current hello world)
uv run task-tracker              # prints "Hello, Task Tracker!"
uv run task-tracker --help       # show help
uv run task-tracker --version    # show version

# Maintenance
make clean                       # remove generated files
```

> Full task management commands (add, list, complete, delete) will be implemented via spec-driven development.

## About Kiro

Kiro is an AI-powered IDE that supports spec-driven development with:

- **Steering documents**: Always-on context for consistent development
- **Skills**: On-demand guidance for specific techniques
- **Hooks**: Automated workflows triggered by events
- **Specs**: Structured feature development with requirements and tasks

This repository demonstrates how to leverage these features for effective ATDD and spec-driven development.
