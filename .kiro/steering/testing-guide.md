---
inclusion: auto
description: Quick reference for ATDD testing practices and when to use the atdd skill for detailed guidance
---

# Testing Guide

> For comprehensive ATDD guidance including the four-layer architecture, DSL patterns, and protocol drivers, ask Kiro to use the `atdd` skill.

## ATDD (Acceptance Test-Driven Development)

Write tests first at two levels:

- **Story level**: Acceptance tests (RED) → implement sub-tasks → acceptance tests pass (GREEN)
- **Sub-task level**: Unit test (RED) → minimal implementation (GREEN) → refactor

Follow the red-green-refactor cycle at both levels.

## Quick Reference

### Test Structure

All tests use Given-When-Then format to describe behavior:

```typescript
describe("Feature: [Feature Name]", () => {
  describe("Scenario: [Scenario Name]", () => {
    test("Given [context] When [action] Then [outcome]", async () => {
      // Test implementation
    });
  });
});
```

### Test Locations

- **Acceptance tests** (story-level): `tests/acceptance/`
- **Unit tests** (sub-task-level): `tests/unit/`
- **Shared test infrastructure**: `tests/shared/`

### Running Tests

```bash
npm test                  # All tests
npm run test:watch        # Watch mode
npm run test:coverage     # Coverage report
```

### When to Use the ATDD Skill

Ask Kiro to use the `atdd` skill when you need:

- Scaffolding acceptance tests for a new user story
- Scaffolding unit tests for a sub-task or component
- Guidance on the four-layer architecture (test cases → DSL → protocol driver → SUT)
- Help deriving the module map from test scenarios
- Examples of realistic test data and fixture design
- Patterns for mocking external dependencies while running real business logic
- Detailed scenario design guidance (happy path, boundary, failure cases)
