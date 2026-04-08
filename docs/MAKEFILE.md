# Makefile Reference

The Makefile provides convenient shortcuts for common development tasks.

## Setup Commands

### make install

Installs all dependencies using `uv sync`.

```bash
make install
```

Equivalent to:

```bash
uv sync
```

## Testing Commands

### make test

Runs all tests (unit and acceptance).

```bash
make test
```

Equivalent to:

```bash
uv run pytest
```

### make test-unit

Runs only unit tests.

```bash
make test-unit
```

Equivalent to:

```bash
uv run pytest tests/unit/
```

### make test-acceptance

Runs only acceptance tests.

```bash
make test-acceptance
```

Equivalent to:

```bash
uv run pytest tests/acceptance/
```

### make test-watch

Runs tests in watch mode (reruns on file changes).

```bash
make test-watch
```

Equivalent to:

```bash
uv run pytest --watch
```

## Running Commands

### make run

Runs the CLI application.

```bash
make run
```

Equivalent to:

```bash
uv run task-tracker
```

### make run with arguments

Pass arguments to the CLI using the `ARGS` variable.

```bash
make run ARGS="--help"
make run ARGS="--version"
```

Equivalent to:

```bash
uv run task-tracker --help
uv run task-tracker --version
```

## Maintenance Commands

### make clean

Removes generated files and caches.

```bash
make clean
```

Cleans up:

- `__pycache__` directories
- `.pytest_cache` directories
- `*.pyc` files

### make help

Shows all available commands with descriptions.

```bash
make help
```

## Tips

### Chaining Commands

You can run multiple make commands in sequence:

```bash
make install && make test
```

### Checking What a Command Does

Use `make -n <target>` to see what commands would be executed without running them:

```bash
make -n test
```

### Adding Custom Commands

Edit the `Makefile` to add your own commands. Follow the existing pattern:

```makefile
.PHONY: my-command
my-command:
	uv run python -m my_module
```
