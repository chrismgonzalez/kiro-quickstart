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
        tags_str = ", ".join(task["tags"]) if task["tags"] else "no tags"
        return (
            f"Task #{task['id']}: {task['title']}\n"
            f"  Status: {task['status']}\n"
            f"  Tags: {tags_str}\n"
            f"  Created: {task['created_at']}"
        )

    def format_task_list(self, tasks: List[Task]) -> str:
        """Format a list of tasks for display.
        
        Args:
            tasks: List of tasks to format
            
        Returns:
            Formatted task list string
        """
        if not tasks:
            return self.format_empty_list()
        
        formatted_tasks = []
        for task in tasks:
            tags_str = ", ".join(task["tags"]) if task["tags"] else "no tags"
            formatted_tasks.append(
                f"#{task['id']} {task['title']} [{task['status']}] ({tags_str})"
            )
        
        return "\n".join(formatted_tasks)

    def format_empty_list(self) -> str:
        """Format message for empty task list.
        
        Returns:
            Empty list message
        """
        return "No tasks found."
