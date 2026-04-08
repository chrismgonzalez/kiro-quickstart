"""JSON file storage backend implementation."""

import json
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
        self._ensure_directory_exists()
        
        # Load existing tasks
        tasks = self._read_json_file()
        
        # Append new task
        tasks.append(task)
        
        # Write back to file
        self._write_json_file(tasks)

    def load_tasks(self) -> List[Task]:
        """Load all tasks from JSON file.
        
        Returns:
            List of all tasks
        """
        return self._read_json_file()

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Find task by ID in JSON file.
        
        Args:
            task_id: The ID of the task to retrieve
            
        Returns:
            The task if found, None otherwise
        """
        tasks = self._read_json_file()
        
        for task in tasks:
            if task["id"] == task_id:
                return task
        
        return None

    def _ensure_directory_exists(self) -> None:
        """Create directory structure if missing."""
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

    def _read_json_file(self) -> List[Task]:
        """Read and parse JSON file.
        
        Returns:
            List of tasks from the file
            
        Raises:
            json.JSONDecodeError: If JSON is invalid or corrupted
            TypeError: If JSON is not an array
        """
        # Return empty list if file doesn't exist
        if not self.file_path.exists():
            return []
        
        # Read and parse JSON file
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            # Re-raise with more context about the file
            raise json.JSONDecodeError(
                f"Invalid JSON in storage file {self.file_path}: {e.msg}",
                e.doc,
                e.pos
            )
        
        # Validate that data is a list
        if not isinstance(data, list):
            raise TypeError(f"Expected JSON array in {self.file_path}, got {type(data).__name__}")
        
        return data

    def _write_json_file(self, tasks: List[Task]) -> None:
        """Write tasks to JSON file.
        
        Args:
            tasks: List of tasks to write
        """
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(tasks, f, ensure_ascii=False, indent=2)
