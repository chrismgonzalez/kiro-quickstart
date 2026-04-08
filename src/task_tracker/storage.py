"""Storage backend protocol definition."""

from typing import Protocol, List, Optional
from task_tracker.models import Task


class StorageBackend(Protocol):
    """Protocol defining storage operations for tasks."""
    
    def save_task(self, task: Task) -> None:
        """Save a single task to storage.
        
        Args:
            task: The task to save
        """
        ...

    def load_tasks(self) -> List[Task]:
        """Load all tasks from storage.
        
        Returns:
            List of all tasks
        """
        ...

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Retrieve a specific task by ID.
        
        Args:
            task_id: The ID of the task to retrieve
            
        Returns:
            The task if found, None otherwise
        """
        ...
