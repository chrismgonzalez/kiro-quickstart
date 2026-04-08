# Documentation

This directory contains detailed documentation for the Task Tracker CLI project.

## Available Documentation

### [ARCHITECTURE.md](ARCHITECTURE.md)

Deep dive into the four-layer test architecture:

- Layer 1: Test Cases
- Layer 2: Domain-Specific Language (DSL)
- Layer 3: Protocol Driver
- Layer 4: System Under Test

Explains the benefits, design principles, and development workflow.

### [MAKEFILE.md](MAKEFILE.md)

Complete reference for all Makefile commands:

- Setup commands (`make install`)
- Testing commands (`make test`, `make test-unit`, `make test-acceptance`)
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

## Documentation Philosophy

Documentation should:

- Stay in sync with code (use the docs skill to check for drift)
- Be concise and actionable
- Use examples over explanations
- Be easy to navigate

When code changes, update docs immediately. Use `#docs` in Kiro to sync documentation.
