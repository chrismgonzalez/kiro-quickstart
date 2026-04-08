---
name: atdd
description: Coach and scaffold acceptance tests and unit tests using the four-layer architecture (test cases → DSL → protocol driver → SUT). Use when implementing a user story or sub-task and need to write tests first following ATDD methodology.
tags:
  [
    atdd,
    bdd,
    testing,
    acceptance-tests,
    unit-tests,
    four-layer,
    tdd,
    red-green-refactor,
  ]
---

# ATDD — Four-Layer Test Architecture

Guide the user through writing tests first using the four-layer architecture, applied at both the story level (acceptance tests) and sub-task level (unit tests). Coach the approach, then scaffold the actual test files.

## When to Use This Skill

- **Starting a user story**: Scaffold acceptance tests before writing any implementation
- **Starting a sub-task**: Scaffold unit tests before writing any component code
- **Reviewing fragile tests**: Identify which layer a test belongs to and restructure it
- **Setting up a new service**: Bootstrap the full four-layer test infrastructure

---

## The Four Layers

Every test suite — regardless of language or framework — is organized into four layers:

### Layer 1: Test Cases (Executable Specifications)

**What it is:** The test functions themselves. They describe WHAT the system should do in problem-domain language only.

**Rules:**

- No mention of HTTP, buttons, fields, SQL, queues, or any technical detail
- Language matches the user story ("buy book", not "POST /checkout")
- Could be read by a non-technical stakeholder and make sense
- One test = one scenario

```python
# Python example
def test_should_allow_user_to_buy_book():
    user = given.a_user_at_the_store()
    user = when.user_searches_for_book(user, "Continuous Delivery")
    user = when.user_selects_book_by_author(user, "Jez Humble")
    user = when.user_adds_selected_book_to_basket(user)
    user = when.user_proceeds_to_checkout(user)
    user = when.user_pays_with_credit_card(user)
    then.item_has_been_purchased(user)
```

### Layer 2: DSL (Domain Specific Language)

**What it is:** Composes elementary driver operations into test scenarios. It holds the scenario logic — the sequencing and composition of steps that together express a behavior.

**Rules:**

- Methods named after user actions, not system interactions
- `when` methods compose multiple driver calls — they are not 1:1 wrappers
- `given` methods set up world state by composing driver calls
- `then` methods hold all assertions in domain terms — no HTTP codes, no field names from JSON
- Still no system-specific details (no HTTP, no selectors, no module names)
- Build incrementally — add methods only when a test needs them

**Critical rule — DSL must compose, not proxy:**

If a DSL `when` method has a single line calling the driver, the driver is doing too much. The composition of steps (e.g. validate → fetch → navigate) belongs in the DSL, not hidden inside the driver. The DSL is where scenario logic lives.

```python
# Anti-pattern: DSL as proxy (driver absorbs all complexity)
async def consumer_browses_the_catalog_root(self, consumer):
    return await self.driver.browse_catalog_root(consumer)  # driver does everything

# Correct: DSL as composer (scenario logic is visible)
async def consumer_browses_the_catalog_root(self, consumer):
    store = consumer._state["store"]
    index = await self.driver.get_or_build_index(store, consumer)
    return self.driver.get_tree_root(index)
```

The second form forces the questions: what is an index? what is tree navigation? Those questions produce distinct modules with distinct interfaces — before any implementation is written.

```python
# Python example
class StoryDsl:
    def __init__(self):
        self.driver = SystemDriver()

    # given: compose driver calls to set up world state
    async def a_user_at_the_store(self):
        session = await self.driver.create_session()
        await self.driver.load_inventory(session)
        return session

    # when: compose driver calls into a scenario action
    async def user_searches_for_book(self, user, title):
        results = await self.driver.run_search(user, title)
        user["search_results"] = results
        return user

    async def user_proceeds_to_checkout(self, user):
        payment = user.get("payment_method", "credit_card")
        order = await self.driver.create_order(user)
        return await self.driver.submit_payment(order, payment)

    # then: pure assertions on domain terms
    def item_has_been_purchased(self, user):
        assert user.get("order_confirmed"), "Expected order to be confirmed"
        assert user.get("receipt"), "Expected receipt to be issued"

dsl = StoryDsl()
given = when = then = dsl
```

### Layer 3: Protocol Driver

**What it is:** Elementary operations on application modules. Each method calls exactly one module and returns a result. The driver's imports define the application's module structure.

**Rules:**

- Each method is small and single-purpose — it calls one real application module
- The driver's imports ARE the application's package map — writing the driver designs the application
- Handles error mapping: translates module-level errors into domain result objects
- Minimal mocking (see Mocking Policy below)
- No scenario logic — sequencing and composition belong in the DSL

**The driver drives architecture emergence:**

By asking "what does the driver need to call to implement this behavior?" you derive the module map before writing any production code. The imports at the top of the driver file become the application's directory structure.

```python
# The imports define the application's modules — they are RED until implementation
from myapp.catalog.store import CatalogStore
from myapp.catalog.index import CatalogIndex
from myapp.catalog.tree import TreeNavigator
from myapp.search.engine import SearchEngine
from myapp.github.client import GitHubClient

class SystemDriver:
    # Each method = one module, one responsibility
    def get_tree_root(self, index: CatalogIndex) -> Result:
        navigator = TreeNavigator(index)
        root = navigator.get_root()
        return Result(ok=True, data=root)

    def resolve_tree_path(self, index: CatalogIndex, path: str) -> Result:
        navigator = TreeNavigator(index)
        node = navigator.resolve(path)
        if node is None:
            return Result(ok=False, data={}, error="not_found")
        return Result(ok=True, data=node)

    def search_index(self, index: CatalogIndex, query: str) -> Result:
        engine = SearchEngine(index)
        results = engine.search(query)
        return Result(ok=True, data={"query": query, "total": len(results), "results": results})
```

### Layer 4: System Under Test

**What it is:** For acceptance tests — the application modules themselves, called directly. For unit tests — the individual module under test.

**Important:** For acceptance tests, Layer 4 is NOT the running HTTP server. HTTP is a delivery mechanism. Acceptance tests validate business logic by calling application modules directly with real external dependencies. The HTTP layer is a thin adapter that gets wired to these modules and does not require the same test rigor.

---

## Mocking Policy

This policy applies at both levels:

| Target                                   | Policy                              |
| ---------------------------------------- | ----------------------------------- |
| Your own services, repositories, modules | **Use real implementations**        |
| AWS services (DynamoDB, KMS, S3, etc.)   | **Use real via moto/localstack**    |
| File system, temp data                   | **Use real** (temp files, tmp dirs) |
| External OAuth providers                 | **Mock** — not under your control   |
| Payment gateways, third-party APIs       | **Mock** — not under your control   |
| Network failures, timeouts               | **Mock** — to test error paths      |

The boundary is: **do you control the code?** If yes, use the real thing.

---

## Two Levels of Application

### Acceptance Tests (Story Level)

Tests a complete user story end-to-end. Written before implementation begins (RED). Passes when all sub-tasks are complete (GREEN).

**File layout:**

```
tests/acceptance/
  test_<story>.py          # Layer 1 — test cases
  story_dsl.py             # Layer 2 — shared story-level DSL
  system_driver.py         # Layer 3 — drives application modules directly
```

**Protocol driver scope:** Calls application modules directly with real external dependencies. Mocks only third parties you don't control. Does NOT drive an HTTP server.

**Test level separation:**

- Acceptance tests validate business logic end-to-end with real dependencies
- Unit tests validate individual component behavior with mocked dependencies
- HTTP integration: thin smoke tests only — trust the framework for routing and serialization

### Unit Tests (Sub-Task Level)

Tests a single component or module. Written before implementing that component (RED). Passes when the component is done (GREEN). Committed to trunk.

**File layout:**

```
tests/unit/
  test_<module>.py         # Layer 1 — test cases
  dsl.py                   # Layer 2 — component-level DSL
  protocol_driver.py       # Layer 3 — drives individual components
```

**Protocol driver scope:** Calls the real component directly. Uses moto/localstack for AWS. Mocks only external third parties.

---

## ATDD Workflow

### Story Level

1. Write acceptance test → **RED** (no implementation)
2. Identify sub-tasks needed to make it pass
3. Implement each sub-task using unit-level ATDD
4. Run acceptance test → **GREEN** (story done)

### Sub-Task Level (Red-Green-Refactor)

1. Write unit test for the sub-task behavior → **RED**
2. Write minimal implementation to pass the test → **GREEN**
3. Refactor if needed (keep tests green)
4. Commit to trunk

---

## Scaffolding Instructions

When asked to scaffold tests for a story or sub-task:

1. **Ask for context** if not provided:
   - What is the story/sub-task in one sentence?
   - What language/framework is in use?
   - Are there existing test infrastructure files to extend, or starting fresh?
   - For acceptance tests: what are the external dependencies? (third-party APIs, external services)

2. **Determine the level**: acceptance test (story) or unit test (sub-task)

3. **For acceptance tests — derive the module map before writing Layer 3:**
   - Walk through each behavior in the spec and ask: "what does the driver need to call?"
   - Name the modules that emerge (e.g. `CatalogStore`, `TreeNavigator`, `SearchEngine`)
   - Confirm the module names and boundaries with the user before writing code
   - The driver imports will define the application's package structure

4. **Generate files in order**:
   - Layer 1 first: write the test case(s) in pure domain language — they will fail immediately (RED)
   - Layer 2: write DSL methods that compose driver calls — check that each `when` method has meaningful composition
   - Layer 3: write elementary driver methods, one per module — imports define the app structure
   - Note what Layer 4 (the implementation) will need to look like

5. **Label each file with its layer** so the user knows where they are

6. **State explicitly**: "This test will fail until you implement [component]. That's the point."

7. **For property-based tests** (where applicable): add a property test to the unit test layer to validate correctness invariants across a wide input range (e.g., round-trip storage, all fields preserved, ordering invariants).

---

## Language-Agnostic Layer Mapping

The four layers apply in any language or framework:

| Layer           | Python                                        | JavaScript/TypeScript                | Java                                 | Gherkin/Cucumber          |
| --------------- | --------------------------------------------- | ------------------------------------ | ------------------------------------ | ------------------------- |
| Test Cases      | pytest functions                              | Jest `it()` blocks                   | `@Test` methods                      | Feature file scenarios    |
| DSL             | Class with methods, `given/when/then` aliases | Object with methods                  | Fluent builder class                 | Step definitions          |
| Protocol Driver | Class that calls application modules          | Class that calls application modules | Class that calls application modules | Step implementation class |
| SUT             | Application modules (not the HTTP server)     | Application modules                  | Application modules                  | Your deployed system      |

---

## Anti-Patterns to Flag and Correct

When reviewing or writing tests, call out these violations:

| Anti-Pattern                                                  | Problem                                      | Fix                                                |
| ------------------------------------------------------------- | -------------------------------------------- | -------------------------------------------------- |
| Test case mentions HTTP status codes                          | Technical detail leaked into Layer 1         | Move to protocol driver                            |
| DSL method name contains "GET", "POST", "query", "table"      | Implementation leaked into Layer 2           | Rename to user action                              |
| DSL `when` method has one line calling the driver             | DSL is a proxy; driver is a god object       | Split driver into elementary calls; compose in DSL |
| Driver method does multiple things (fetch + parse + navigate) | Hides module boundaries; produces bad design | One driver method = one module call                |
| Protocol driver mocks your own module                         | Defeats purpose of real testing              | Use real implementation                            |
| All four layers collapsed into one test function              | No separation; breaks on any change          | Refactor into layers                               |
| Test infrastructure built upfront before any tests            | Speculative DSL nobody needs yet             | Build incrementally as tests demand                |
| Horizontal test: "test the database layer"                    | Tests implementation, not behavior           | Rewrite as behavior scenario                       |
| Acceptance tests drive the HTTP server                        | Tests delivery mechanism, not business logic | Call application modules directly                  |

---

## Example: Scaffolding from Scratch

**Given:** "User can store OAuth credentials for Google"

**Step 1 — Derive the module map (before writing Layer 3)**

Ask: what does the driver need to call?

- Something that creates a user session → `SessionStore`
- Something that stores credentials → `CredentialStore`
- Something that retrieves credentials → `CredentialStore`
- External OAuth provider → mock (not under our control)

Module map:

```
SessionStore    ← manages user sessions
CredentialStore ← stores and retrieves credentials
```

**Step 2 — Layer 1: Write the acceptance test (RED)**

```python
# tests/acceptance/test_credential_storage_story.py
from tests.acceptance.story_dsl import given, when, then

class TestCredentialStorageStory:
    async def test_developer_stores_google_credentials(self):
        developer = await given.a_developer_with_a_valid_google_token()
        await when.developer_stores_credentials_for_google(developer)
        then.credentials_are_retrievable_for_google(developer)
```

**Step 3 — Layer 2: Compose driver calls into scenarios**

```python
# tests/acceptance/story_dsl.py
class StoryDsl:
    def __init__(self):
        self.driver = SystemDriver()

    # given: compose driver calls to set up world state
    async def a_developer_with_a_valid_google_token(self):
        token = self.driver.issue_mock_oauth_token(provider="google")
        session = await self.driver.create_session()
        session["token"] = token
        return session

    # when: compose driver calls — note the explicit sequence
    async def developer_stores_credentials_for_google(self, developer):
        credential = self.driver.build_credential(developer["token"], provider="google")
        await self.driver.persist_credential(developer, credential)
        return developer

    # then: pure assertions in domain terms
    def credentials_are_retrievable_for_google(self, developer):
        result = self.driver.retrieve_credential(developer, provider="google")
        assert result is not None, "Expected credential to be stored"
        assert result.get("provider") == "google"

dsl = StoryDsl()
given = when = then = dsl
```

**Step 4 — Layer 3: Elementary module calls — imports define the app**

```python
# tests/acceptance/system_driver.py
# These imports are RED until implementation — that is intentional.
# Writing this file is designing the application.
from myapp.sessions.store import SessionStore
from myapp.credentials.store import CredentialStore

class SystemDriver:
    def __init__(self):
        self.mock_oauth = MockOAuthProvider()  # external, not under our control

    async def create_session(self) -> dict:
        store = SessionStore()
        session_id = await store.create()
        return {"session_id": session_id}

    def issue_mock_oauth_token(self, provider: str) -> str:
        return self.mock_oauth.issue_token(provider=provider)

    def build_credential(self, token: str, provider: str) -> dict:
        return {"provider": provider, "access_token": token}

    async def persist_credential(self, session: dict, credential: dict) -> None:
        store = CredentialStore()
        await store.save(session_id=session["session_id"], credential=credential)

    def retrieve_credential(self, session: dict, provider: str) -> dict | None:
        store = CredentialStore()
        return store.get(session_id=session["session_id"], provider=provider)
```

**State:** Test is RED. `SessionStore` and `CredentialStore` don't exist yet. The module boundaries are defined. Now drive sub-tasks with unit-level ATDD to implement each module.

---

## Coaching Notes

- **"I don't know what to put in Layer 1"** → Write the scenario in plain English first. If you can't say it without technical words, the story isn't clear enough yet.
- **"My DSL is getting huge"** → Each method should map to one user action or one assertion group. If it's growing fast, check that you're not putting driver logic in the DSL.
- **"My DSL `when` methods are all one-liners"** → The DSL is a proxy. Split the driver into elementary calls and move the composition into the DSL.
- **"The protocol driver is doing too much"** → Split it. One method per module. If a driver method fetches, parses, and navigates, that's three methods.
- **"Should I mock the database?"** → No. Use moto or a real local instance. Mocking the database is how tests pass when the real system is broken.
- **"Should acceptance tests hit the HTTP server?"** → No. Call application modules directly. HTTP is a delivery mechanism — test the business logic, not the wiring.
- **"The acceptance test is slow"** → That's expected for story-level tests. Unit tests should be fast. Don't sacrifice correctness for speed at the acceptance level.
- **"How do I know what modules to create?"** → Walk through each driver method and ask what it calls. Each answer is a module. The driver's imports are the answer.
