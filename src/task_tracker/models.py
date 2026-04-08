"""Task data model and validation functions."""

from typing import TypedDict, List


class Task(TypedDict):
    """Task data structure."""
    id: int
    title: str
    tags: List[str]
    status: str
    created_at: str


def validate_title(title: str) -> None:
    """Validate task title.
    
    Args:
        title: The task title to validate
        
    Raises:
        ValueError: If title is invalid
    """
    if not title or not title.strip():
        raise ValueError("Title cannot be empty")


def validate_status(status: str) -> None:
    """Validate task status.
    
    Args:
        status: The task status to validate
        
    Raises:
        ValueError: If status is invalid
    """
    valid_statuses = ["pending", "complete"]
    if status not in valid_statuses:
        raise ValueError(f"Invalid status. Must be 'pending' or 'complete'")


def validate_task_id(task_id: int) -> None:
    """Validate task ID.
    
    Args:
        task_id: The task ID to validate
        
    Raises:
        ValueError: If task ID is invalid
    """
    if task_id <= 0:
        raise ValueError("Task ID must be a positive integer")


def validate_timestamp(timestamp: str) -> None:
    """Validate ISO timestamp.
    
    Args:
        timestamp: The timestamp to validate
        
    Raises:
        ValueError: If timestamp is invalid
    """
    from datetime import datetime
    
    if not timestamp:
        raise ValueError("Timestamp cannot be empty")
    
    # Require 'T' separator for ISO format (date and time required)
    if 'T' not in timestamp:
        raise ValueError(f"Invalid ISO timestamp format: {timestamp}")
    
    try:
        datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
    except (ValueError, AttributeError):
        raise ValueError(f"Invalid ISO timestamp format: {timestamp}")
