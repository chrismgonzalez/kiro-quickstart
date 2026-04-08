---
description: Overview of all steering files and their inclusion rules
---

# Steering Files Overview

This directory contains steering files that guide Kiro's behavior when working on this project.

## Inclusion Rules

Steering files can be included in different ways:

- **Auto inclusion**: Always included in context automatically
- **Manual inclusion**: Referenced explicitly with `#filename.md` in chat
- **No inclusion rule**: Included by default (always auto-included)

## Available Steering Files

### Always Included (Auto/Default)

These files are automatically included in every interaction:

| File                   | Description                                                                       |
| ---------------------- | --------------------------------------------------------------------------------- |
| `development-guide.md` | Core development workflow, coding standards, ATDD principles, and common commands |
| `code-index.md`        | Maps every component, function, and module to its exact file location             |
| `testing-guide.md`     | Quick reference for ATDD testing practices and when to use the atdd skill         |

### Manual Inclusion Only

These files are referenced explicitly when needed:

| File                          | Description                                                                         | When to Use                                       |
| ----------------------------- | ----------------------------------------------------------------------------------- | ------------------------------------------------- |
| `spec-design-construction.md` | Guide for translating EARS requirements into Gherkin behaviors and technical design | When creating or reviewing `design.md` for a spec |
| `spec-task-construction.md`   | Guide for constructing tasks.md following strict ATDD principles                    | When creating or reviewing `tasks.md` for a spec  |

## Usage Examples

### Automatic Inclusion

Files without `inclusion: manual` are always available:

```
"How do I run tests?"
→ development-guide.md is already in context
```

### Manual Inclusion

Reference manual files explicitly:

```
"#spec-design-construction.md - help me create the design document"
→ Loads the design construction guide
```

```
"#spec-task-construction.md - review my tasks.md for ATDD compliance"
→ Loads the task construction guide
```

## Maintenance

When adding new steering files:

1. Add frontmatter with `description` field
2. Set `inclusion: manual` if the file should only be loaded on demand
3. Update this README with the new file
4. Reference the file in `development-guide.md` if it's part of a workflow

## File Relationships

```
development-guide.md (always included)
├── References: code-index.md (for finding code)
├── References: spec-design-construction.md (for design.md)
└── References: spec-task-construction.md (for tasks.md)

testing-guide.md (always included)
└── References: atdd skill (for detailed guidance)

spec-design-construction.md (manual)
├── Used when: Creating/reviewing design.md
└── Works with: spec-task-construction.md, atdd skill

spec-task-construction.md (manual)
├── Used when: Creating/reviewing tasks.md
└── Works with: spec-design-construction.md, atdd skill

code-index.md (always included)
└── Updated when: Adding new modules, functions, or components
```

## Best Practices

1. **Keep descriptions concise**: One sentence explaining the file's purpose
2. **Use manual inclusion for specialized guides**: Don't clutter context with rarely-needed details
3. **Reference related files**: Help users discover related steering files
4. **Update code-index.md frequently**: Keep it current as the codebase evolves
5. **Test inclusion rules**: Verify auto-included files don't make context too large
