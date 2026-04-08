.PHONY: help install test test-watch test-unit test-acceptance run clean

help:
	@echo "Task Tracker CLI - Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install          Install dependencies with uv"
	@echo ""
	@echo "Testing:"
	@echo "  make test             Run all tests"
	@echo "  make test-watch       Run tests in watch mode"
	@echo "  make test-unit        Run unit tests only"
	@echo "  make test-acceptance  Run acceptance tests only"
	@echo ""
	@echo "Running:"
	@echo "  make run              Run the CLI (use ARGS='...' for arguments)"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean            Remove generated files"

install:
	uv sync

test:
	uv run pytest

test-watch:
	uv run pytest --watch

test-unit:
	uv run pytest tests/unit/

test-acceptance:
	uv run pytest tests/acceptance/

run:
	uv run task-tracker $(ARGS)

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
