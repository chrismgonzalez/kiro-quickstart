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
    raise NotImplementedError


def validate_status(status: str) -> None:
    """Validate task status.
    
    Args:
        status: The task status to validate
        
    Raises:
        ValueError: If status is invalid
    """
    raise NotImplementedError


def validate_task_id(task_id: int) -> None:
    """Validate task ID.
    
    Args:
        task_id: The task ID to validate
        
    Raises:
        ValueError: If task ID is invalid
    """
    raise NotImplementedError


def validate_timestamp(timestamp: str) -> None:
    """Validate ISO timestamp.
    
    Args:
        timestamp: The timestamp to validate
        
    Raises:
        ValueError: If timestamp is invalid
    """
    raise NotImplementedError
