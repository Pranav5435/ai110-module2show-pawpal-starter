from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Tuple


def _parse_time(value: Optional[str]) -> Optional[datetime]:
    """Parse a supported time string into a datetime object."""
    if not value:
        return None

    for fmt in ("%H:%M", "%I:%M %p", "%H:%M:%S"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    return None


@dataclass
class Task:
    description: str
    time: Optional[str] = None
    frequency: Optional[str] = None
    duration: Optional[int] = None
    priority: Optional[str] = None
    completion_status: bool = False

    def mark_complete(self) -> None:
        """Mark the task as complete."""
        self.completion_status = True

    def mark_incomplete(self) -> None:
        """Mark the task as incomplete."""
        self.completion_status = False

    def is_due(self) -> bool:
        """Return whether the task is still pending."""
        return not self.completion_status

    def to_dict(self) -> dict:
        """Convert the task into a dictionary representation."""
        return {
            "description": self.description,
            "time": self.time,
            "frequency": self.frequency,
            "duration": self.duration,
            "priority": self.priority,
            "completion_status": self.completion_status,
        }


@dataclass
class Pet:
    name: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet."""
        self.tasks.append(task)

    def get_pending_tasks(self) -> List[Task]:
        """Return all pending tasks for this pet."""
        return [task for task in self.tasks if not task.completion_status]


@dataclass
class Owner:
    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        """Collect all tasks belonging to this owner's pets."""
        all_tasks: List[Task] = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks


class Scheduler:
    def __init__(self, owner: Owner):
        """Initialize the scheduler for a specific owner."""
        self.owner = owner

    def _all_tasks(self) -> List[Task]:
        """Return every task owned by the scheduler's owner."""
        return self.owner.get_all_tasks()

    def _parse_minutes(self, value: Optional[str]) -> int:
        """Convert a time string to minutes from midnight."""
        parsed = _parse_time(value)
        if parsed is None:
            return 24 * 60
        return parsed.hour * 60 + parsed.minute

    def _priority_rank(self, task: Task) -> int:
        """Map a priority string to a sortable rank."""
        return {"high": 0, "medium": 1, "low": 2}.get((task.priority or "").lower(), 99)

    def _overlaps(self, first: Task, second: Task) -> bool:
        """Return whether two tasks overlap in time."""
        if not first.time or not second.time or first.duration is None or second.duration is None:
            return False

        first_start = self._parse_minutes(first.time)
        second_start = self._parse_minutes(second.time)
        first_end = first_start + first.duration
        second_end = second_start + second.duration
        return max(first_start, second_start) < min(first_end, second_end)

    def sort_by_time(self) -> List[Task]:
        """Return tasks sorted by completion, time, and priority."""
        return sorted(
            self._all_tasks(),
            key=lambda task: (
                task.completion_status,
                self._parse_minutes(task.time),
                self._priority_rank(task),
                task.description.lower(),
            ),
        )

    def filter_tasks(self) -> List[Task]:
        """Return only tasks that are still pending."""
        return [task for task in self._all_tasks() if not task.completion_status]

    def detect_conflicts(self) -> List[Tuple[Task, Task]]:
        """Find overlapping pending tasks."""
        pending_tasks = [task for task in self._all_tasks() if not task.completion_status and task.time]
        conflicts: List[Tuple[Task, Task]] = []

        for index, first in enumerate(pending_tasks):
            for second in pending_tasks[index + 1 :]:
                if self._overlaps(first, second):
                    conflicts.append((first, second))

        return conflicts

    def handle_recurrence(self) -> List[Task]:
        """Expand recurring tasks into a few example occurrences."""
        expanded_tasks: List[Task] = []

        for task in self._all_tasks():
            if task.completion_status or not task.frequency:
                continue

            for occurrence in range(1, 4):
                expanded_tasks.append(
                    Task(
                        description=f"{task.description} (occurrence {occurrence})",
                        time=task.time,
                        frequency=None,
                        duration=task.duration,
                        priority=task.priority,
                        completion_status=False,
                    )
                )

        return expanded_tasks
