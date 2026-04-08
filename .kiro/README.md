# Kiro Configuration

This directory contains Kiro-specific configuration for this talk/presentation.

## Structure

```
.kiro/
├── skills/              # On-demand specialized guidance
│   ├── atdd.md          # 4-layer acceptance testing framework
│   └── docs.md          # Documentation sync process
├── steering/            # Always-on context and guidance
│   ├── development-guide.md    # Coding standards, tech stack
│   ├── code-index.md           # Complete file/symbol map
│   └── testing-guide.md        # Testing quick reference
└── hooks/               # Automated agent triggers
    └── source-to-docs-sync.kiro.hook  # Doc drift detection
```

## Skills

Skills are comprehensive guides loaded on-demand to keep context focused.

### testing.md

**When to use:** When writing tests, building test infrastructure, or deciding what kind of test to write.

**Provides:**

- 4-layer acceptance testing architecture (Scenarios → DSL → Protocol Driver → System)
- TypeScript and Python examples
- Realistic test data and fixture design guidance
- Scenario design patterns (happy path, boundary, failure)

**Activate with:**

- "Use the testing skill to help me write tests"
- "Create a DSL for the application domain"
- "Set up acceptance tests"

### docs.md

**When to use:** When syncing docs, checking for drift, or updating documentation after code changes.

**Provides:**

- 6-step documentation sync process
- Discovery of existing documentation
- Semantic change analysis
- Gap identification
- Systematic update proposals

**Activate with:**

- "Use the docs skill to sync documentation"
- "Check for doc drift before this PR"
- "Update docs for this feature"

## Steering Files

Steering files are always-on context that guides Kiro's behavior.

### development-guide.md

Core development guidance including:

- Quick start commands
- Technology stack
- Coding standards
- Testing requirements
- File structure and naming conventions

### code-index.md

Complete map of the codebase:

- Source file locations
- Key functions and classes
- Architecture patterns
- Testing strategy

**Always update when:**

- Adding new files
- Renaming or moving files
- Deleting files
- Adding new exported functions/classes

### testing-guide.md

Quick testing reference:

- Test-first development principles
- Test structure (Given-When-Then)
- Test locations
- Running tests
- When to use the testing skill

## Hooks

Hooks automate agent actions based on IDE events.

### source-to-docs-sync.kiro.hook

**Trigger:** User-triggered (manual)

**Action:** Asks agent to use the docs skill to check for documentation drift

**Use when:**

- Before opening a PR
- After completing a feature
- After a refactor
- When you suspect docs are stale

**Trigger from:** Kiro Hooks panel in the IDE or command palette

## Best Practices

### When to Use Skills vs Steering

**Use skills when:**

- You need comprehensive, detailed guidance
- Building new infrastructure (test DSLs, documentation systems)
- Learning a new pattern or framework
- Need step-by-step processes

**Use steering when:**

- You need quick reference information
- Following established patterns
- Checking conventions or standards
- Getting oriented in the codebase

### Keeping Configuration in Sync

**Update steering files when:**

- Project structure changes
- New conventions are established
- Technology stack changes
- Common patterns emerge

**Update skills when:**

- Processes evolve
- New frameworks are adopted
- Best practices change
- Examples need updating

**Update hooks when:**

- Workflow automation needs change
- New events need monitoring
- Trigger conditions change

## Contributing

When adding new configuration:

1. **Skills:** Create for comprehensive, process-oriented guidance
2. **Steering:** Create for quick reference and always-on context
3. **Hooks:** Create for workflow automation

Keep all configuration files:

- Focused and single-purpose
- Well-documented with examples
- Up-to-date with the codebase
