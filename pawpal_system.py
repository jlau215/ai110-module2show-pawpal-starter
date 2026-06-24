from dataclasses import dataclass
from datetime import date
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

    def get_age(self) -> int:
        today = date.today()
        return (today - self.pet_dob).days // 365

    def get_tasks(self) -> list:
        pass


@dataclass
class Task:
    task_id: int
    title: str
    task_type: str          # walk | feeding | meds | grooming | enrichment | appointment
    duration: int           # minutes
    date: str
    time: str
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
        pass

    def get_schedule(self) -> list[Task]:
        pass


class Scheduler:
    def __init__(self, owner: Owner, date: str):
        self.owner = owner
        self.date = date
        self.tasks: list[Task] = []
        self.daily_plan: list[Task] = []

    def generate_plan(self) -> list[Task]:
        pass

    def prioritize_tasks(self) -> list[Task]:
        pass

    def notify(self, message: str) -> None:
        pass

    def explain_plan(self) -> str:
        pass
