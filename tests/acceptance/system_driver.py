"""Layer 3: Protocol Driver - Elementary calls to application modules.

This driver defines the application structure through its imports.
Each method makes exactly one call to an application module.
"""

from pathlib import Path
from typing import List, Optional
import tempfile
import shutil

# These imports define the application architecture
from task_tracker.models import Task
from task_tracker.store import TaskStore
from task_tracker.json_backend import JSONFileBackend


class SystemDriver:
    """Protocol driver that makes elementary calls to application modules."""

    def __init__(self):
        """Initialize driver with temporary storage for test isolation."""
        self.temp_dir = None
        self.storage_path = None
        self.backend = None
        self.store = None

    def initialize_storage(self) -> None:
        """Create temporary storage location for tests."""
        self.temp_dir = tempfile.mkdtemp()
        self.storage_path = Path(self.temp_dir) / "tasks.json"
        self.backend = JSONFileBackend(str(self.storage_path))
        self.store = TaskStore(self.backend)

    def cleanup_storage(self) -> None:
        """Remove temporary storage after tests."""
        if self.temp_dir and Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)

    def create_task(self, title: str, tags: Optional[List[str]] = None, 
                   status: str = "pending") -> Task:
        """Create a task through the TaskStore."""
        return self.store.create_task(title=title, tags=tags, status=status)

    def get_all_tasks(self) -> List[Task]:
        """Retrieve all tasks from the TaskStore."""
        return self.store.get_all_tasks()

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Retrieve a specific task by ID from the TaskStore."""
        return self.store.get_task(task_id)

    def corrupt_storage(self) -> None:
        """Corrupt the storage file to simulate invalid JSON."""
        if self.storage_path:
            self.storage_path.write_text("{ invalid json }")

    def storage_exists(self) -> bool:
        """Check if storage file exists."""
        return self.storage_path and self.storage_path.exists()
