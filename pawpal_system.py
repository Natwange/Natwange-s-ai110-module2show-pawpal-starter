from dataclasses import dataclass, field
from datetime import date
from typing import List

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
    time: str
        
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
    pet_id: int  #suggested fix
    date: date
    status: str
    tasks: List[Task] = field(default_factory=list)

    def create_plan(self) -> None:
        """Create a new task plan for the pet"""
        self.status = "active"
    
    def list_plan(self) -> List[Task]:
        """Return all tasks in the current plan."""
        return self.tasks or []

    def add_task(self, task: Task) -> None:
        """Append a task to the scheduler's task list."""
        self.tasks.append(task)
    
    def edit_task(self, task_id: int, description: str = None, frequency: int = None) -> None:
        """Edit an existing task by its ID."""
        for task in self.tasks:
            if task.id == task_id:
                if description is not None:
                    task.description = description
                if frequency is not None:
                    task.frequency = frequency
                break

    def remove_task(self, task_id: int) -> None:
        """Remove a task from the scheduler by its ID."""
        self.tasks = [t for t in self.tasks if t.id != task_id]

    def perform_task(self, task_id: int) -> None:
        """Mark a task as completed by its ID."""
        for task in self.tasks:
            if task.id == task_id:
                task.mark_complete()
                break

    def get_tasks_by_status(self, status: str) -> List[Task]:
        """Return all tasks matching the given status."""
        return [t for t in self.tasks if t.status == status]

    def organize_by_frequency(self) -> dict:
        """Group tasks into a dict keyed by their daily frequency."""
        organized = {}
        for task in self.tasks:
            freq = task.get_frequency()
            if freq not in organized:
                organized[freq] = []
            organized[freq].append(task)
        return organized

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
        if self.scheduler:
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
        return self.scheduler.list_plan() if self.scheduler else []