---
name: docs
description: This skill should be used when the user asks to "sync docs", "check for doc drift", "update documentation", "review docs before a PR", "find stale docs", "check if docs are up to date", or has just completed a feature or refactor and needs documentation kept in sync with code changes. Discovers existing docs, analyzes what changed semantically, proposes updates, and applies after approval.
---

# Docs Skill

Documentation drifts from code constantly. Every merged PR that changes behavior, adds features, removes services, or introduces new patterns is an opportunity for docs to become stale. This skill exists to catch that drift — it treats documentation as a first-class artifact that must stay in sync with the codebase.

Use this skill to discover what documentation exists, analyze what changed in the code, identify gaps and stale references, and propose updates — never writing anything without approval.

## When to Use

- Before opening a PR — catch doc drift before it ships
- After completing a feature or refactor — sync docs with new behavior
- When reviewing recent commits — scan for accumulated documentation debt
- When documentation feels out of sync with the code

---

## Process

### Step 1: Discover Existing Documentation

Scan the repository for documentation. Do not assume a structure — find what is actually there.

```
Look for:
- README.md (project overview)
- docs/ directory and all files within it
- .kiro/steering/*.md (development guides, always-on context)
- .kiro/skills/*.md (specialized guidance)
- Any *.md files at the root level
- API specs (openapi.json, openapi.yaml)
- Code comments and docstrings in key files
```

Build an inventory of what exists.

---

### Step 2: Understand What Changed

Get the diff against the main branch:

```bash
git diff main...HEAD --name-only          # files changed
git diff main...HEAD                      # full diff
git log main...HEAD --oneline             # commit summary
```

Read each changed file. Reason about what the changes mean semantically — not just which files changed, but what behavior, structure, or interface changed.

---

### Step 3: Map Changes to Documentation

Cross-reference what changed against what exists:

| Code location changed | Documentation likely affected   |
| --------------------- | ------------------------------- |
| `src/components/`     | `code-index.md`, technical docs |
| `src/services/`       | `code-index.md`, API docs       |
| Configuration files   | `README.md`, setup guides       |
| Dependencies          | Setup/installation docs         |
| Test patterns         | `testing-guide.md`              |

**code-index.md is always checked.** Every structural code change — new file, new class, deleted file — potentially affects it.

---

### Step 4: Produce the Documentation Sync Report

Present the full report before making any changes:

```
## Documentation Sync Report

### Documentation found
[list of existing doc files]

### Changes detected
[semantic summary of what changed]

### Updates needed
[affected docs and why]

### Gaps identified
[docs that don't exist yet but should]

### Proposed changes
[specific edits with rationale]
```

Wait for approval before proceeding to Step 5.

---

### Step 5: Apply Documentation Changes

After receiving approval, apply changes systematically:

- Use `strReplace` for targeted edits
- Use `fsAppend` for adding new sections
- Use `fsWrite` only for new files

**For code-index.md updates:**

- Read the entire file first
- Add new entries in the correct section
- Update existing entries if behavior changed
- Remove entries for deleted files
- Maintain logical ordering

Apply changes one file at a time. Re-read each file before editing to ensure context is fresh.

---

### Step 6: Verify

After all changes are applied:

- Re-read each updated file to confirm changes applied correctly
- Check that internal links still resolve
- Verify code examples are syntactically correct
- Confirm no references to deleted files remain
- Ensure consistency in terminology across docs

Summarize what was updated and flag anything that needs manual review.

---

## Style Guidelines

**Voice:**

- Direct and concise
- Use present tense
- Use active voice

**Code examples:**

- Always include language identifier in code blocks
- Keep examples minimal and focused
- Use realistic values
- Include comments only when necessary

**Structure:**

- Use headers for navigation
- Use tables for structured data
- Use bullet lists for steps or options
- Use numbered lists only for sequential steps

**Links:**

- Use relative paths for internal docs
- Use descriptive link text
- Verify links resolve after updates

---

## Limitations

This skill does not:

- Auto-commit documentation — always requires approval
- Generate docs for code it hasn't read
- Make assumptions about undocumented behavior
- Create diagrams (but will flag when one would help)

---

## Tips for Effective Use

**Be specific about scope:**

- "Sync docs for the [feature]" → focused on specific changes
- "Check all docs for drift" → comprehensive review
- "Update code-index.md only" → targeted update

**Provide context:**

- "I just merged 3 PRs, can you check for doc drift?"
- "About to open a PR, review docs"
- "Refactored [area], update docs"

**Review before approval:**

- Check that proposed changes are accurate
- Verify examples match actual code
- Ensure terminology is consistent
- Flag anything that needs more detail
