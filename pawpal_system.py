from dataclasses import dataclass, field
from datetime import date, time as Time
from typing import Optional


@dataclass
class Task:
    """Single pet care activity."""
    task_id: int
    pet_id: int             # links task to a specific Pet
    title: str
    task_type: str          # walk | feeding | meds | grooming | enrichment | appointment
    description: str        # longer detail about the activity
    duration: int           # minutes
    task_date: date
    task_time: Time
    priority: int
    frequency: str = "once" # once | daily | weekly — how often task repeats
    status: str = "pending" # pending | completed | skipped
    notes: str = ""

    def mark_complete(self) -> None:
        pass

    def mark_skipped(self) -> None:
        pass


@dataclass
class Pet:
    """Stores pet profile and owns that pet's task list."""
    pet_id: int
    pet_name: str
    species: str
    breed: str
    pet_dob: date
    weight: float = 0.0
    medical_notes: str = ""
    tasks: list[Task] = field(default_factory=list)

    def get_age(self) -> int:
        today = date.today()
        return (today - self.pet_dob).days // 365

    def get_tasks(self) -> list[Task]:
        return self.tasks


class Owner:
    """Manages multiple pets; aggregates tasks across all of them."""
    def __init__(
        self,
        owner_id: int,
        name: str,
        available_time: int,        # minutes per day
        preferences: Optional[list] = None,
    ):
        self.owner_id = owner_id
        self.name = name
        self.available_time = available_time
        self.preferences: list = preferences or []
        self.pets: list[Pet] = []
        # no self.tasks — tasks live on Pet, Owner aggregates via get_tasks()

    def add_pet(self, pet: Pet) -> None:
        pass

    def edit_pet(self, pet_id: int, updates: dict) -> None:
        pass

    def get_pet(self, pet_id: int) -> Optional[Pet]:
        pass

    def remove_pet(self, pet_id: int) -> None:
        pass

    def add_task(self, task: Task) -> None:
        """Add task to the correct pet's task list."""
        pass

    def edit_task(self, task_id: int, updates: dict) -> None:
        pass

    def remove_task(self, task_id: int) -> None:
        pass

    def get_tasks(self) -> list[Task]:
        """Aggregate tasks from all pets."""
        return [task for pet in self.pets for task in pet.tasks]

    def get_schedule(self) -> list[Task]:
        return []


class Scheduler:
    """Brain: retrieves, organizes, and manages tasks across all pets."""
    def __init__(self, owner: Owner, schedule_date: date):
        self.owner = owner
        self.schedule_date = schedule_date
        self.daily_plan: list[Task] = []

    def get_tasks_for_pet(self, pet_id: int) -> list[Task]:
        """Retrieve all tasks belonging to one pet."""
        return [t for t in self.owner.get_tasks() if t.pet_id == pet_id]

    def get_tasks_for_date(self, target: date) -> list[Task]:
        """Retrieve all tasks scheduled on a specific date."""
        return [t for t in self.owner.get_tasks() if t.task_date == target]

    def prioritize_tasks(self) -> list[Task]:
        """Sort today's tasks by priority and time."""
        pass

    def generate_plan(self) -> list[Task]:
        """Fit prioritized tasks into owner's available_time budget."""
        return []

    def notify(self, message: str) -> None:
        pass

    def explain_plan(self) -> str:
        """Return human-readable reasoning for the generated plan."""
        pass
