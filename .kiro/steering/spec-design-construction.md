---
inclusion: manual
description: Guide for constructing spec design.md files by translating EARS requirements into Gherkin behaviors and technical design
---

# Spec Design Construction Guide

## Core Principle

Design bridges requirements and implementation:

1. **Translate EARS → Gherkin** (executable specifications in domain language)
2. **Define architecture** (components, interfaces, data models)
3. **Document decisions** (error handling, testing strategy)

## Document Structure

```markdown
# Design Document: <Feature Name>

## Overview

[Brief description, key design decisions]

## Behavioral Specifications (Gherkin)

[Translate each EARS criterion into Given-When-Then scenarios]

## Architecture

[Component diagram, layer responsibilities]

## Components and Interfaces

[Module definitions that match protocol driver imports]

## Data Models

[Structures, validation rules, formats]

## Error Handling

[Error types, validation points, recovery strategies]

## Testing Strategy

[Four-layer acceptance tests, unit tests, coverage goals]
```

---

## EARS → Gherkin Translation

### Translation Rules

1. **One EARS criterion → One or more Gherkin scenarios**
2. **EARS "WHEN/WHERE" → Gherkin "Given" + "When"**
3. **EARS "SHALL" → Gherkin "Then"**
4. **Domain language only** (no HTTP, JSON, database, file paths)

### Quick Examples

**EARS:**

```
WHEN a user provides a title, THE CLI SHALL create a task with that title
```

**Gherkin:**

```gherkin
Scenario: User creates task with title
  Given the task tracker is ready
  When the user creates a task with title "Write documentation"
  Then a task exists with title "Write documentation"
```

**EARS with error:**

```
WHEN a user provides an empty title, THE CLI SHALL return an error message "Title cannot be empty"
```

**Gherkin:**

```gherkin
Scenario: User attempts to create task with empty title
  Given the task tracker is ready
  When the user attempts to create a task with an empty title
  Then the task is not created
  And an error message "Title cannot be empty" is displayed
```

**EARS with ordering:**

```
WHEN retrieving tasks, THE Task_Store SHALL return tasks in creation order
```

**Gherkin:**

```gherkin
Scenario: Tasks are listed in creation order
  Given the task tracker is ready
  When the user creates a task with title "First task"
  And the user creates a task with title "Second task"
  And the user lists all tasks
  Then the tasks appear in order: "First task", "Second task"
```

### Gherkin Best Practices

- **Scenario names**: Describe behavior, not implementation ("User creates task" not "POST /tasks")
- **Given**: World state in domain terms ("user has 3 tasks" not "database has 3 records")
- **When**: User action ("user searches for tasks" not "filter module queries store")
- **Then**: Observable outcome ("2 tasks displayed" not "result array length is 2")
- **One scenario = one behavior** (split if you need "And" in scenario name)

---

## Technical Design Sections

### Architecture

Define components and responsibilities:

- Component diagram (Mermaid)
- Layer responsibilities (CLI → Business Logic → Storage)

**Key principle:** Component interfaces must match protocol driver imports. The driver defines the application structure.

### Components and Interfaces

List protocols, classes, and method signatures that the protocol driver will import.

### Data Models

- Structure definitions (TypedDict, schema)
- Validation rules (what's valid/invalid)
- File/storage format (example with comments)

### Error Handling

For each error type:

- **Trigger**: What causes it
- **Response**: Error type and message
- **Layer**: Where validation happens
- **Recovery**: How to fix (if applicable)

### Testing Strategy

- **Four-layer acceptance tests**: Test cases → DSL → Protocol driver → Real modules
- **Unit tests**: Specific examples and edge cases (~20-30 tests)
- **Coverage goals**: Quantify expected test count

---

## Anti-Patterns

### ❌ Wrong: Technical details in Gherkin

```gherkin
Scenario: POST to /tasks endpoint
  Given the database is empty
  When I POST {"title": "Task 1"} to /tasks
  Then the response status is 201
```

### ✅ Correct: Domain language

```gherkin
Scenario: User creates a task
  Given the task tracker is ready
  When the user creates a task with title "Task 1"
  Then a task exists with title "Task 1"
```

### ❌ Wrong: Gherkin doesn't match EARS

EARS says "user provides tags" but Gherkin tests "default empty tags"

### ✅ Correct: Gherkin directly tests EARS

```gherkin
Scenario: User creates task with tags
  Given the task tracker is ready
  When the user creates a task with tags "urgent" and "work"
  Then a task exists with tags "urgent" and "work"
```

---

## Review Checklist

- [ ] Every EARS criterion has at least one Gherkin scenario
- [ ] All Gherkin uses domain language (no HTTP, JSON, database)
- [ ] Scenarios are concrete and testable (specific values)
- [ ] Component interfaces match protocol driver imports
- [ ] Data models include validation rules
- [ ] Error handling covers all validation and storage errors
- [ ] Testing strategy includes acceptance and unit tests

---

## Integration

**Flow:** Requirements (EARS) → Design (Gherkin + Technical) → Tasks (RED-GREEN) → Implementation (ATDD)

**Works with:**

- `spec-task-construction.md` - Defines implementation sequence
- `atdd` skill - Gherkin becomes Layer 1 test cases
- `development-guide.md` - Provides workflow context
