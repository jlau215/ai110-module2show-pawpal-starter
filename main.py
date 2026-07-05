from datetime import date, time
from pawpal_system import Owner, Pet, Task, Scheduler

# ── Setup ────────────────────────────────────────────────────────────────────

today = date.today()

owner = Owner(
    owner_id=1,
    name="Alex",
    available_time=120,     # 2 hours free today
    preferences=["morning walks", "consistent meal times"],
)

buddy = Pet(
    pet_id=1,
    pet_name="Buddy",
    species="Dog",
    breed="Labrador",
    pet_dob=date(2020, 3, 15),
)

luna = Pet(
    pet_id=2,
    pet_name="Luna",
    species="Cat",
    breed="Siamese",
    pet_dob=date(2022, 7, 1),
    medical_notes="On daily allergy medication.",
)

owner.add_pet(buddy)
owner.add_pet(luna)

# ── Tasks ────────────────────────────────────────────────────────────────────

owner.add_task(Task(
    task_id=1,
    pet_id=1,
    title="Morning Walk",
    task_type="walk",
    description="30-min walk around the park.",
    duration=30,
    task_date=today,
    task_time=time(7, 0),
    priority=3,
    frequency="daily",
))

owner.add_task(Task(
    task_id=2,
    pet_id=2,
    title="Allergy Medication",
    task_type="meds",
    description="Give Luna one allergy tablet with food.",
    duration=5,
    task_date=today,
    task_time=time(8, 0),
    priority=3,
    frequency="daily",
    notes="Hide in treat if she refuses.",
    required=True,          # meds are never skipped due to budget (#5)
))

owner.add_task(Task(
    task_id=3,
    pet_id=1,
    title="Buddy Breakfast",
    task_type="feeding",
    description="1.5 cups dry kibble.",
    duration=10,
    task_date=today,
    task_time=time(7, 30),
    priority=2,
    frequency="daily",
))

owner.add_task(Task(
    task_id=4,
    pet_id=2,
    title="Luna Breakfast",
    task_type="feeding",
    description="Half can wet food + fresh water.",
    duration=10,
    task_date=today,
    task_time=time(8, 0),
    priority=2,
    frequency="daily",
))

owner.add_task(Task(
    task_id=5,
    pet_id=1,
    title="Evening Grooming",
    task_type="grooming",
    description="Brush coat and check ears.",
    duration=20,
    task_date=today,
    task_time=time(18, 0),
    priority=1,
    frequency="weekly",
))

# ── Schedule ─────────────────────────────────────────────────────────────────

scheduler = Scheduler(owner=owner, schedule_date=today)
plan = scheduler.generate_plan()

total_scheduled = sum(t.duration for t in plan)
remaining_time = owner.available_time - total_scheduled  # (#10)

WIDTH = 62
print()
print("=" * WIDTH)
print(f"  PawPal -- Today's Schedule".center(WIDTH))
print(f"  {today.strftime('%A, %B %d, %Y')}".center(WIDTH))
print("=" * WIDTH)
print(f"  Owner : {owner.name}")
print(f"  Budget: {owner.available_time} min available  |  {total_scheduled} min scheduled  |  {remaining_time} min free")
print("-" * WIDTH)
print(f"  {'#':<3} {'Time':<7} {'Pet':<8} {'Task':<22} {'Min':>4}  {'Pri':>5}")
print("-" * WIDTH)

for i, task in enumerate(plan, start=1):
    pet = owner.get_pet(task.pet_id)
    pet_name = pet.pet_name if pet else "?"
    time_str = task.task_time.strftime("%H:%M")
    priority_bar = "[" + "#" * task.priority + "." * (3 - task.priority) + "]"
    req_marker = "*" if task.required else " "
    print(f"  {i:<3} {time_str:<7} {pet_name:<8} {task.title:<22} {task.duration:>3}m  {priority_bar}{req_marker}")

print("-" * WIDTH)
print(f"  Total: {total_scheduled} / {owner.available_time} min used  ({remaining_time} min remaining)")

# Conflict warnings (#4)
if scheduler.conflicts:
    print()
    for a, b in scheduler.conflicts:
        print(f"  !! CONFLICT: '{a.title}' and '{b.title}' overlap at {b.task_time.strftime('%H:%M')}")

print("=" * WIDTH)
print()

# ── Per-pet task summary ──────────────────────────────────────────────────────

for pet in owner.pets:
    print(f"  {pet.pet_name} ({pet.species}, age {pet.get_age()}) -- {len(pet.get_tasks(filter_date=today))} task(s) today")
    for task in pet.get_tasks(filter_date=today):  # date-filtered (#9)
        req_tag = " [REQUIRED]" if task.required else ""
        print(f"    > {task.task_time.strftime('%H:%M')}  {task.title:<24} [{task.status}]{req_tag}")
    if pet.medical_notes:
        print(f"    NOTE: {pet.medical_notes}")
    print()