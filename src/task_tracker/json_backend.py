"""JSON file storage backend implementation."""

from pathlib import Path
from typing import List, Optional
from task_tracker.models import Task


class JSONFileBackend:
    """JSON file storage backend implementation."""

    def __init__(self, file_path: str = "~/.task-tracker/tasks.json"):
        """Initialize with file path.
        
        Args:
            file_path: Path to the JSON file
        """
        self.file_path = Path(file_path).expanduser()

    def save_task(self, task: Task) -> None:
        """Append task to JSON file.
        
        Args:
            task: The task to save
        """
        raise NotImplementedError

    def load_tasks(self) -> List[Task]:
        """Load all tasks from JSON file.
        
        Returns:
            List of all tasks
        """
        raise NotImplementedError

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Find task by ID in JSON file.
        
        Args:
            task_id: The ID of the task to retrieve
            
        Returns:
            The task if found, None otherwise
        """
        raise NotImplementedError

    def _ensure_directory_exists(self) -> None:
        """Create directory structure if missing."""
        raise NotImplementedError

    def _read_json_file(self) -> List[Task]:
        """Read and parse JSON file.
        
        Returns:
            List of tasks from the file
        """
        raise NotImplementedError

    def _write_json_file(self, tasks: List[Task]) -> None:
        """Write tasks to JSON file.
        
        Args:
            tasks: List of tasks to write
        """
        raise NotImplementedError
