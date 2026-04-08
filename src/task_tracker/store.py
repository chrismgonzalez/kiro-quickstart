"""Task store for managing task persistence and retrieval."""

from typing import List, Optional
from task_tracker.models import Task
from task_tracker.storage import StorageBackend


class TaskStore:
    """Manages task persistence and retrieval."""

    def __init__(self, backend: StorageBackend):
        """Initialize with a storage backend.
        
        Args:
            backend: The storage backend to use
        """
        self.backend = backend

    def create_task(
        self,
        title: str,
        tags: Optional[List[str]] = None,
        status: str = "pending"
    ) -> Task:
        """Create a new task with auto-generated ID and timestamp.
        
        Args:
            title: The task title
            tags: Optional list of tags
            status: The task status (default: "pending")
            
        Returns:
            The created task
        """
        raise NotImplementedError

    def get_all_tasks(self) -> List[Task]:
        """Retrieve all tasks in creation order.
        
        Returns:
            List of all tasks
        """
        raise NotImplementedError

    def get_task(self, task_id: int) -> Optional[Task]:
        """Retrieve a task by ID.
        
        Args:
            task_id: The ID of the task to retrieve
            
        Returns:
            The task if found, None otherwise
        """
        raise NotImplementedError

    def _generate_next_id(self) -> int:
        """Generate the next sequential task ID.
        
        Returns:
            The next task ID
        """
        raise NotImplementedError
