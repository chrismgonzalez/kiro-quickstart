"""Task store for managing task persistence and retrieval."""

from datetime import datetime
from typing import List, Optional
from task_tracker.models import Task, validate_title, validate_status
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
            
        Raises:
            ValueError: If title or status is invalid
        """
        # Validate inputs (defense in depth - CLI also validates)
        validate_title(title)
        validate_status(status)
        
        task: Task = {
            "id": self._generate_next_id(),
            "title": title,
            "tags": tags if tags is not None else [],
            "status": status,
            "created_at": datetime.now().isoformat()
        }
        self.backend.save_task(task)
        return task

    def get_all_tasks(self) -> List[Task]:
        """Retrieve all tasks in creation order.
        
        Returns:
            List of all tasks
        """
        return self.backend.load_tasks()

    def get_task(self, task_id: int) -> Optional[Task]:
        """Retrieve a task by ID.
        
        Args:
            task_id: The ID of the task to retrieve
            
        Returns:
            The task if found, None otherwise
        """
        return self.backend.get_task_by_id(task_id)

    def _generate_next_id(self) -> int:
        """Generate the next sequential task ID.
        
        Returns:
            The next task ID
        """
        tasks = self.backend.load_tasks()
        if not tasks:
            return 1
        return max(task["id"] for task in tasks) + 1
