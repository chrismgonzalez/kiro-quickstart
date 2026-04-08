"""CLI interface for Task Tracker."""

import click
import sys
import os
from typing import Optional
from task_tracker.store import TaskStore
from task_tracker.json_backend import JSONFileBackend
from task_tracker.formatter import TaskFormatter
from task_tracker.filter import TaskFilter
from task_tracker.models import validate_title, validate_status, validate_task_id


def get_backend():
    """Get the storage backend, using TEST_TASK_FILE env var if set."""
    file_path = os.environ.get('TEST_TASK_FILE', '~/.task-tracker/tasks.json')
    return JSONFileBackend(file_path)


@click.group()
@click.version_option(package_name='task-tracker-cli')
def cli():
    """Task Tracker - A simple CLI demonstrating ATDD."""
    pass


@cli.command()
@click.argument('title')
@click.option('--tag', multiple=True, help='Add a tag to the task')
@click.option('--status', default='pending', help='Task status (pending or complete)')
def create(title: str, tag: tuple, status: str):
    """Create a new task with a title, optional tags, and status."""
    try:
        # Validate inputs
        validate_title(title)
        validate_status(status)
        
        # Convert tags tuple to list (use builtin list, not the command)
        tags = [t for t in tag] if tag else []
        
        # Create task
        backend = get_backend()
        store = TaskStore(backend)
        formatter = TaskFormatter()
        
        task = store.create_task(title=title, tags=tags, status=status)
        
        # Display created task
        click.echo(formatter.format_task(task))
        
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error creating task: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--status', help='Filter by status (pending or complete)')
@click.option('--tag', help='Filter by tag')
def list(status: Optional[str], tag: Optional[str]):
    """List all tasks, optionally filtered by status or tag."""
    try:
        backend = get_backend()
        store = TaskStore(backend)
        formatter = TaskFormatter()
        task_filter = TaskFilter()
        
        # Get all tasks
        tasks = store.get_all_tasks()
        
        # Apply filters if provided
        if status:
            validate_status(status)
            tasks = task_filter.filter_by_status(tasks, status)
        
        if tag:
            tasks = task_filter.filter_by_tags(tasks, [tag])
        
        # Display tasks
        output = formatter.format_task_list(tasks)
        click.echo(output)
        
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error listing tasks: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('task_id', type=int)
def get(task_id: int):
    """Get a specific task by ID."""
    try:
        # Validate task ID
        validate_task_id(task_id)
        
        backend = get_backend()
        store = TaskStore(backend)
        formatter = TaskFormatter()
        
        # Retrieve task
        task = store.get_task(task_id)
        
        if task is None:
            click.echo(f"Error: Task with ID {task_id} not found", err=True)
            sys.exit(1)
        
        # Display task
        click.echo(formatter.format_task(task))
        
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error retrieving task: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    cli()
