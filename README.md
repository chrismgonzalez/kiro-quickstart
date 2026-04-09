# Kiro Quickstart

Template repository for CodeStock talk - "What the Spec! Battle Tested Practices for Spec Driven Development using Kiro"

This repository demonstrates ATDD (Acceptance Test-Driven Development) and spec-driven development using Kiro, featuring a Task Tracker CLI proof-of-concept.

## What's Inside

This repository contains:

1. **Task Tracker CLI** - A working POC demonstrating the four-layer ATDD architecture
2. **Kiro Configuration** - Steering documents, skills, and hooks for guided development
3. **Complete Test Suite** - Acceptance and unit tests following ATDD principles
4. **Documentation** - Comprehensive guides for development, testing, and architecture

## Prerequisites

Before you begin, you'll need to install the required tooling for your operating system.

### Installing uv (Python Package Manager)

uv is a fast Python package manager that handles dependencies and virtual environments.

**macOS/Linux:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**

```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Alternative (using pip):**

```bash
pip install uv
```

Verify installation:

```bash
uv --version
```

### Installing Make

Make is used to run common development commands.

**macOS:**

```bash
# Using Homebrew
brew install make

# Or use the built-in make (already installed)
make --version
```

**Linux:**

```bash
# Debian/Ubuntu
sudo apt-get install build-essential

# Fedora/RHEL
sudo dnf install make

# Arch
sudo pacman -S make
```

**Windows:**

Option 1 - Using Chocolatey:

```powershell
choco install make
```

Option 2 - Using Scoop:

```powershell
scoop install make
```

Option 3 - Using WSL (Windows Subsystem for Linux):

```bash
# Install WSL first, then use Linux commands above
wsl --install
```

Option 4 - Run commands directly without Make:

```bash
# Instead of 'make install', use:
uv sync

# Instead of 'make test', use:
uv run pytest

# Instead of 'make run', use:
uv run task-tracker
```

### Installing Python 3.11+

**macOS:**

```bash
# Using Homebrew
brew install python@3.11
```

**Linux:**

```bash
# Debian/Ubuntu
sudo apt-get install python3.11

# Fedora/RHEL
sudo dnf install python3.11

# Arch
sudo pacman -S python
```

**Windows:**
Download from [python.org](https://www.python.org/downloads/) or use:

```powershell
# Using Chocolatey
choco install python

# Using Scoop
scoop install python
```

Verify installation:

```bash
python3 --version  # or python --version on Windows
```

## Quick Start

Once you have the prerequisites installed:

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

A proof-of-concept CLI demonstrating ATDD with the four-layer architecture. Features complete task management with creation, listing, filtering, and retrieval capabilities.

### Current Features

- Create tasks with title, tags, and status
- List all tasks with filtering by status or tag
- Retrieve specific tasks by ID
- Persistent JSON storage at `~/.task-tracker/tasks.json`
- Auto-incrementing task IDs
- ISO timestamp tracking
- Input validation

### CLI Commands

```bash
# Create tasks
uv run task-tracker create "Write tests"
uv run task-tracker create "Deploy app" --tag urgent --tag devops
uv run task-tracker create "Review code" --status complete

# List tasks
uv run task-tracker list                    # all tasks
uv run task-tracker list --status pending   # filter by status
uv run task-tracker list --tag urgent       # filter by tag

# Get specific task
uv run task-tracker get 1                   # get task with ID 1
```

### What This Demonstrates

1. **ATDD Four-Layer Architecture**
   - Layer 1: 30+ test cases in plain domain language
   - Layer 2: DSL that composes driver operations
   - Layer 3: Protocol driver with elementary module calls
   - Layer 4: Complete application modules (models, storage, store, filter, formatter, CLI)

2. **Steering Documents**
   - Development guide with standards and quick commands
   - Code index mapping every module and function
   - Testing guide for quick ATDD reference

3. **Spec-Driven Development**
   - Feature defined in `.kiro/specs/task-creation-and-storage/`
   - Acceptance tests written before implementation (RED)
   - Module boundaries derived from driver imports
   - Unit tests for each module
   - Red-green-refactor cycle completed

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
│   │   └── task-creation-and-storage/
│   └── hooks/                # Automation
├── src/
│   └── task_tracker/
│       ├── __init__.py      # Package initialization
│       ├── models.py        # Task data model and validation
│       ├── storage.py       # Storage backend protocol
│       ├── json_backend.py  # JSON file storage
│       ├── store.py         # Task business logic
│       ├── filter.py        # Task filtering
│       ├── formatter.py     # Output formatting
│       └── cli.py           # CLI interface (create, list, get)
├── tests/
│   ├── acceptance/          # Story-level tests (30+ scenarios)
│   │   ├── test_task_creation.py  # Layer 1: Test cases
│   │   ├── story_dsl.py           # Layer 2: DSL
│   │   └── system_driver.py       # Layer 3: Driver
│   ├── unit/                # Component-level tests
│   │   ├── test_models.py
│   │   ├── test_storage.py
│   │   ├── test_json_backend.py
│   │   ├── test_store.py
│   │   ├── test_filter.py
│   │   ├── test_formatter.py
│   │   └── test_cli.py
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
make run ARGS="create 'My task'" # run with arguments
uv sync                          # install/update dependencies
uv add <package>                 # add new dependency

# Testing
make test                        # all tests
make test-unit                   # unit tests only
make test-acceptance             # acceptance tests only
make lint                        # run ruff, basedpyright, bandit
uv run pytest                    # all tests
uv run pytest -v                 # verbose output
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

# Maintenance
make clean                       # remove generated files
```

## Preparing for Your Talk

This repository includes tools for creating demo checkpoints that you can switch between during your presentation.

### Quick Demo Setup

```bash
# 1. Work through the spec process with Kiro, saving checkpoints as you go
bash scripts/checkpoint.sh save 00-start-here
# ... work with Kiro to create spec ...
bash scripts/checkpoint.sh save 01-your-first-spec
# ... continue through all phases ...

# 2. Verify all checkpoints are saved
bash scripts/checkpoint.sh list

# 3. Push to remote (optional, for backup)
bash scripts/checkpoint.sh push
```

### During Your Talk

```bash
# Navigate between checkpoints
bash scripts/checkpoint.sh goto 00-start-here
bash scripts/checkpoint.sh goto 04-test-first-red
bash scripts/checkpoint.sh goto 06-feature-complete-green
```

## About Kiro

Kiro is an AI-powered IDE that supports spec-driven development with:

- **Steering documents**: Always-on context for consistent development
- **Skills**: On-demand guidance for specific techniques
- **Hooks**: Automated workflows triggered by events
- **Specs**: Structured feature development with requirements and tasks

This repository demonstrates how to leverage these features for effective ATDD and spec-driven development.
