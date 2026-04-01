from dataclasses import dataclass, field
from datetime import date, time, timedelta, datetime
from typing import List, Dict, Tuple
from collections import defaultdict

@dataclass
class Pet:
    id: int
    owner_id: int #suggested fix
    name: str
    species: str
    age: int

    def get_age(self) -> int:
        """Return the pet's age."""
        return self.age

    def get_species(self) -> str:
        """Return the pet's species."""
        return self.species


@dataclass
class Task:
    id: int
    pet_id: int
    status: str
    description: str
    frequency: int
    time: time
    priority: int = 1

    def mark_complete(self) -> None:
        """Set the task status to completed."""
        self.status = "completed"

    def mark_pending(self) -> None:
        """Set the task status back to pending."""
        self.status = "pending"

    def get_description(self) -> str:
        """Return the task description."""
        return self.description

    def get_frequency(self) -> int:
        """Return how many times per day the task should occur."""
        return self.frequency


@dataclass
class Scheduler:
    id: int
    date: date
    status: str
    priority: int = 1
    tasks: Dict[int, Task] = field(default_factory=dict)

    def create_plan(self) -> None:
        """Create a new task plan for the pet"""
        self.status = "active"

    def generate_plan(self) -> List[Task]:
        """Return all tasks in the current plan, ordered by time."""
        return sorted(self.tasks.values(), key=lambda t: t.time)

    def add_task(self, task: Task) -> None:
        """Append a task to the scheduler's task list, raising on time conflict."""
        for existing in self.tasks.values():
            if existing.pet_id == task.pet_id and existing.time == task.time:
                raise ValueError(
                    f"Conflict: '{existing.description}' already scheduled at "
                    f"{task.time.strftime('%I:%M %p')} for pet {task.pet_id}."
                )
        self.tasks[task.id] = task

    def edit_task(self, task_id: int, description: str = None, frequency: int = None) -> None:
        """Edit an existing task by its ID."""
        task = self.tasks.get(task_id)
        if task:
            if description is not None:
                task.description = description
            if frequency is not None:
                task.frequency = frequency

    def remove_task(self, task_id: int) -> None:
        """Remove a task from the scheduler by its ID."""
        self.tasks.pop(task_id, None)

    def perform_task(self, task_id: int) -> None:
        """Mark a task as completed by its ID."""
        task = self.tasks.get(task_id)
        if task:
            task.mark_complete()

    def get_tasks_by_pet(self, pet_id: int) -> List[Task]:
        """Return all tasks for a specific pet, ordered by time."""
        return sorted(
            (t for t in self.tasks.values() if t.pet_id == pet_id),
            key=lambda t: t.time
        )

    def get_tasks_by_status(self, status: str) -> List[Task]:
        """Return all tasks matching the given status."""
        return [t for t in self.tasks.values() if t.status == status]

    def generate_recurring_slots(self) -> List[Tuple[time, Task]]:
        """Expand each task by its frequency, spacing slots evenly across 24 hours.
        Returns a list of (slot_time, task) tuples sorted chronologically."""
        slots = []
        for task in self.tasks.values():
            interval = timedelta(hours=24 // task.frequency)
            slot_dt = datetime.combine(self.date, task.time)
            for _ in range(task.frequency):
                slots.append((slot_dt.time(), task))
                slot_dt += interval
        return sorted(slots, key=lambda s: s[0])

    def organize_by_frequency(self) -> dict:
        """Group tasks into a dict keyed by their daily frequency."""
        organized = defaultdict(list)
        for task in self.tasks.values():
            organized[task.frequency].append(task)
        return dict(organized)

@dataclass
class PetOwner:
    id: int
    name: str
    email: str
    pets: List[Pet] = field(default_factory=list)
    scheduler: Scheduler = None

    def perform_task(self, task_id: int) -> None:
        """Mark a task as completed through the owner's scheduler."""
        if self.scheduler:
            self.scheduler.perform_task(task_id)

    def add_task(self, task: Task) -> None:
        """Add a new task through the owner's scheduler."""
        if not self.scheduler:
            raise ValueError("No scheduler assigned to this owner.")
        self.scheduler.add_task(task)

    def edit_task(self, task_id: int, description: str = None, frequency: int = None) -> None:
        """Edit an existing task through the owner's scheduler."""
        if self.scheduler:
            self.scheduler.edit_task(task_id, description, frequency)

    def remove_task(self, task_id: int) -> None:
        """Remove a task through the owner's scheduler."""
        if self.scheduler:
            self.scheduler.remove_task(task_id)

    def get_tasks(self) -> List[Task]:
        """Return all tasks assigned to the owner."""
        return self.scheduler.generate_plan() if self.scheduler else []

    def get_tasks_by_pet(self, pet_id: int) -> List[Task]:
        """Return all tasks for a specific pet."""
        return self.scheduler.get_tasks_by_pet(pet_id) if self.scheduler else []
