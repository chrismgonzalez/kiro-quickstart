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

All tests use the namespace pattern with `given`, `when`, `then` objects:

```python
def test_should_allow_user_to_buy_book():
    """Scenario: User purchases a book
    Given a user at the store
    When the user searches for "Continuous Delivery"
    And the user selects book by author "Jez Humble"
    And the user adds selected book to basket
    And the user proceeds to checkout
    And the user pays with credit card
    Then item has been purchased
    """
    user = given.a_user_at_the_store()
    user = when.user_searches_for_book(user, "Continuous Delivery")
    user = when.user_selects_book_by_author(user, "Jez Humble")
    user = when.user_adds_selected_book_to_basket(user)
    user = when.user_proceeds_to_checkout(user)
    user = when.user_pays_with_credit_card(user)
    then.item_has_been_purchased(user)
```

**Key principles:**

- `given.*` methods set up world state and return state objects
- `when.*` methods perform actions, accept and return state objects
- `then.*` methods make assertions on state objects
- State flows through the test via return values
- Docstring describes the scenario in Gherkin format

### Test Locations

- **Acceptance tests** (story-level): `tests/acceptance/`
- **Unit tests** (sub-task-level): `tests/unit/`
- **Shared test infrastructure**: `tests/shared/`

### When to Use the ATDD Skill

Ask Kiro to use the `atdd` skill when you need:

- Scaffolding acceptance tests for a new user story
- Scaffolding unit tests for a sub-task or component
- Guidance on the four-layer architecture (test cases → DSL → protocol driver → SUT)
- Help deriving the module map from test scenarios
- Examples of realistic test data and fixture design
- Patterns for mocking external dependencies while running real business logic
- Detailed scenario design guidance (happy path, boundary, failure cases)
