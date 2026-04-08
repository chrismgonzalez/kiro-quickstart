"""Task filter for filtering tasks by criteria."""

from typing import List, Optional
from task_tracker.models import Task


class TaskFilter:
    """Filters tasks by various criteria."""

    def filter_by_status(self, tasks: List[Task], status: str) -> List[Task]:
        """Filter tasks by status.
        
        Args:
            tasks: List of tasks to filter
            status: Status to filter by
            
        Returns:
            Filtered list of tasks
        """
        raise NotImplementedError

    def filter_by_tags(self, tasks: List[Task], tags: List[str]) -> List[Task]:
        """Filter tasks by tags.
        
        Args:
            tasks: List of tasks to filter
            tags: Tags to filter by
            
        Returns:
            Filtered list of tasks
        """
        raise NotImplementedError

    def filter_by_id(self, tasks: List[Task], task_id: int) -> Optional[Task]:
        """Filter tasks by ID.
        
        Args:
            tasks: List of tasks to filter
            task_id: ID to filter by
            
        Returns:
            The task if found, None otherwise
        """
        raise NotImplementedError
