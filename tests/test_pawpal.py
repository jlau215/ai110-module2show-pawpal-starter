import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from datetime import date, time
from pawpal_system import Owner, Pet, Task


def make_task(task_id=1, pet_id=1):
    """Helper: returns a minimal Task with default values."""
    return Task(
        task_id=task_id,
        pet_id=pet_id,
        title="Morning Walk",
        task_type="walk",
        description="Walk around the block.",
        duration=30,
        task_date=date(2026, 7, 5),
        task_time=time(7, 0),
        priority=2,
    )


def make_pet(pet_id=1):
    """Helper: returns a minimal Pet."""
    return Pet(
        pet_id=pet_id,
        pet_name="Buddy",
        species="Dog",
        breed="Labrador",
        pet_dob=date(2020, 3, 15),
    )


# ── Test 1: Task Completion ───────────────────────────────────────────────────

def test_mark_complete_changes_status():
    task = make_task()
    assert task.status == "pending"     # starts pending

    task.mark_complete()

    assert task.status == "completed"   # status updated after call


# ── Test 2: Task Addition ─────────────────────────────────────────────────────

def test_add_task_increases_pet_task_count():
    owner = Owner(owner_id=1, name="Alex", available_time=120)
    pet = make_pet()
    owner.add_pet(pet)

    assert len(pet.tasks) == 0          # no tasks yet

    owner.add_task(make_task(task_id=1, pet_id=pet.pet_id))
    owner.add_task(make_task(task_id=2, pet_id=pet.pet_id))

    assert len(pet.tasks) == 2          # two tasks added
