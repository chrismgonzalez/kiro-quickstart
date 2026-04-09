# Documentation

This directory contains detailed documentation for the Task Tracker CLI project.

## Available Documentation

### [ARCHITECTURE.md](ARCHITECTURE.md)

Deep dive into the four-layer test architecture:

- Layer 1: Test Cases (30+ scenarios implemented)
- Layer 2: Domain-Specific Language (DSL)
- Layer 3: Protocol Driver
- Layer 4: System Under Test (complete implementation)

Explains the benefits, design principles, and development workflow.

### [MAKEFILE.md](MAKEFILE.md)

Complete reference for all Makefile commands:

- Setup commands (`make install`)
- Testing commands (`make test`, `make test-unit`, `make test-acceptance`)
- Code quality commands (`make lint`)
- Running commands (`make run`)
- Maintenance commands (`make clean`)

## Quick Links

**Getting Started:**

- [Main README](../README.md) - Project overview and quick start
- [Development Guide](../.kiro/steering/development-guide.md) - Coding standards and workflow

**Code Navigation:**

- [Code Index](../.kiro/steering/code-index.md) - Complete codebase map
- [Testing Guide](../.kiro/steering/testing-guide.md) - Testing reference

**Skills (On-Demand):**

- [ATDD Skill](../.kiro/skills/atdd.md) - Comprehensive ATDD guidance
- [Docs Skill](../.kiro/skills/docs.md) - Documentation sync process

## Implementation Status

The Task Tracker CLI is fully implemented with:

- Complete task management (create, list, get)
- JSON file persistence
- Task filtering by status and tags
- Input validation
- 30+ acceptance tests (all passing)
- Complete unit test coverage (all passing)
- CLI with Click framework

## Documentation Philosophy

Documentation should:

- Stay in sync with code (use the docs skill to check for drift)
- Be concise and actionable
- Use examples over explanations
- Be easy to navigate

When code changes, update docs immediately. Use `#docs` in Kiro to sync documentation.
