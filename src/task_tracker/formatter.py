"""Task formatter for output display."""

from typing import List
from task_tracker.models import Task


class TaskFormatter:
    """Formats task data for display."""

    def format_task(self, task: Task) -> str:
        """Format a single task for display.
        
        Args:
            task: The task to format
            
        Returns:
            Formatted task string
        """
        raise NotImplementedError

    def format_task_list(self, tasks: List[Task]) -> str:
        """Format a list of tasks for display.
        
        Args:
            tasks: List of tasks to format
            
        Returns:
            Formatted task list string
        """
        raise NotImplementedError

    def format_empty_list(self) -> str:
        """Format message for empty task list.
        
        Returns:
            Empty list message
        """
        raise NotImplementedError
