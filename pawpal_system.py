from dataclasses import dataclass, field
from datetime import date, time as Time
from typing import Optional


@dataclass
class Pet:
    pet_id: int
    pet_name: str
    species: str
    breed: str
    pet_dob: date
    weight: float = 0.0
    medical_notes: str = ""
    tasks: list = field(default_factory=list)

    def get_age(self) -> int:
        today = date.today()
        return (today - self.pet_dob).days // 365

    def get_tasks(self) -> list:
        return self.tasks


@dataclass
class Task:
    task_id: int
    pet_id: int             # links task to a specific Pet
    title: str
    task_type: str          # walk | feeding | meds | grooming | enrichment | appointment
    duration: int           # minutes
    task_date: date
    task_time: Time
    priority: int
    status: str = "pending" # pending | completed | skipped
    notes: str = ""
    is_recurring: bool = False

    def mark_complete(self) -> None:
        pass

    def mark_skipped(self) -> None:
        pass


class Owner:
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
        self.tasks: list[Task] = []

    def add_pet(self, pet: Pet) -> None:
        pass

    def edit_pet(self, pet_id: int, updates: dict) -> None:
        pass

    def get_pet(self, pet_id: int) -> Optional[Pet]:
        pass

    def remove_pet(self, pet_id: int) -> None:
        pass

    def add_task(self, task: Task) -> None:
        pass

    def edit_task(self, task_id: int, updates: dict) -> None:
        pass

    def remove_task(self, task_id: int) -> None:
        pass

    def get_tasks(self) -> list[Task]:
        return []

    def get_schedule(self) -> list[Task]:
        return []


class Scheduler:
    def __init__(self, owner: Owner, schedule_date: date):
        self.owner = owner
        self.schedule_date = schedule_date  # renamed: was shadowing datetime.date
        self.daily_plan: list[Task] = []   # removed self.tasks; use owner.tasks as single source

    def generate_plan(self) -> list[Task]:
        pass

    def prioritize_tasks(self) -> list[Task]:
        pass

    def notify(self, message: str) -> None:
        pass

    def explain_plan(self) -> str:
        pass
