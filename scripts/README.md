# Demo Scripts

## checkpoint.sh

Tool for managing demo checkpoint branches.

### Usage

```bash
# Save current state as a checkpoint
bash scripts/checkpoint.sh save 00-start-here

# List all checkpoints (shows which are saved)
bash scripts/checkpoint.sh list

# Switch to a checkpoint
bash scripts/checkpoint.sh goto 04-test-first-red

# Push checkpoints to remote
bash scripts/checkpoint.sh push                # Push all
bash scripts/checkpoint.sh push 00-start-here  # Push one

# Delete checkpoints
bash scripts/checkpoint.sh delete 00-start-here  # Delete one
bash scripts/checkpoint.sh delete-all            # Delete all
```

### Available Checkpoints

1. `00-start-here` - Starting point with minimal CLI
2. `01-your-first-spec` - Spec file created
3. `02-requirements-complete` - Requirements defined
4. `03-design-approved` - Design complete with tasks
5. `04-test-first-red` - Acceptance test written (RED)
6. `05-module-implemented` - TaskStore module complete
7. `06-feature-complete-green` - CLI integrated (GREEN)
8. `07-docs-updated` - Documentation synced

### Workflow

See `docs/DEMO_WORKFLOW.md` for step-by-step instructions on preparing your demo branches.

### During Demo

See `docs/DEMO_GUIDE.md` for talking points and what to show at each checkpoint.

## Make the script executable

```bash
chmod +x scripts/checkpoint.sh
```
