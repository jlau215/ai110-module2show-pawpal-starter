from datetime import date, time
from pawpal_system import Owner, Pet, Task, Scheduler

# ── Setup ────────────────────────────────────────────────────────────────────

today = date.today()

owner = Owner(
    owner_id=1,
    name="Alex",
    available_time=120,
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

# ── Tasks added INTENTIONALLY OUT OF ORDER to demo sort_by_time() ─────────────
# Insertion order: 18:00 → 08:00 → 08:00 → 07:00 → 07:30

owner.add_task(Task(          # added 1st — latest time
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

owner.add_task(Task(          # added 2nd
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
    required=True,
))

owner.add_task(Task(          # added 3rd
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

owner.add_task(Task(          # added 4th — earliest time
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

owner.add_task(Task(          # added 5th
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

# Deliberately overlapping tasks to demo conflict detection:
#   task_id=6 — Luna "Morning Stretch" at 07:00 overlaps Buddy's Morning Walk
#               (different pets, same time → owner-time conflict)
#   task_id=7 — Buddy "Vet Check" at 07:00 overlaps Buddy's Morning Walk
#               (same pet, same time → same-pet conflict)
owner.add_task(Task(
    task_id=6,
    pet_id=2,
    title="Morning Stretch",
    task_type="enrichment",
    description="Guided stretching for Luna's joints.",
    duration=15,
    task_date=today,
    task_time=time(7, 0),
    priority=1,
    frequency="once",
))

owner.add_task(Task(
    task_id=7,
    pet_id=1,
    title="Vet Check",
    task_type="appointment",
    description="Quick weight and temperature check.",
    duration=20,
    task_date=today,
    task_time=time(7, 0),
    priority=2,
    frequency="once",
))

# ── Scheduler setup ───────────────────────────────────────────────────────────

scheduler = Scheduler(owner=owner, schedule_date=today)

# ── Demo: sort_by_time() ──────────────────────────────────────────────────────

WIDTH = 62

print()
print("=" * WIDTH)
print("  DEMO: sort_by_time()".center(WIDTH))
print("  Tasks as added (out of order) vs sorted by time".center(WIDTH))
print("=" * WIDTH)

raw_tasks = owner.get_tasks()
sorted_tasks = scheduler.sort_by_time()

print(f"\n  {'--- As Added (insertion order) ---':^{WIDTH - 2}}")
print(f"  {'#':<3} {'Time':<7} {'Pet':<8} {'Task'}")
print("  " + "-" * (WIDTH - 2))
for i, t in enumerate(raw_tasks, 1):
    pet = owner.get_pet(t.pet_id)
    pet_name = pet.pet_name if pet else "?"
    print(f"  {i:<3} {t.task_time.strftime('%H:%M'):<7} {pet_name:<8} {t.title}")

print(f"\n  {'--- After sort_by_time() ---':^{WIDTH - 2}}")
print(f"  {'#':<3} {'Time':<7} {'Pet':<8} {'Task'}")
print("  " + "-" * (WIDTH - 2))
for i, t in enumerate(sorted_tasks, 1):
    pet = owner.get_pet(t.pet_id)
    pet_name = pet.pet_name if pet else "?"
    print(f"  {i:<3} {t.task_time.strftime('%H:%M'):<7} {pet_name:<8} {t.title}")

# ── Generate the plan + mark some tasks complete for filter demo ──────────────

plan = scheduler.generate_plan()

# Simulate Morning Walk and Buddy Breakfast as already done
owner.edit_task(1, {"status": "completed"})   # Morning Walk
owner.edit_task(3, {"status": "completed"})   # Buddy Breakfast

# ── Demo: filter_tasks() by status ───────────────────────────────────────────

print()
print("=" * WIDTH)
print("  DEMO: filter_tasks(status=...)".center(WIDTH))
print("  Shows which tasks are done vs still pending".center(WIDTH))
print("=" * WIDTH)

for status_val, label in [("completed", "Completed"), ("pending", "Pending")]:
    filtered = scheduler.filter_tasks(status=status_val)
    print(f"\n  [{label}]  ({len(filtered)} task(s))")
    if filtered:
        for t in scheduler.sort_by_time(filtered):
            pet = owner.get_pet(t.pet_id)
            pet_name = pet.pet_name if pet else "?"
            print(f"    {t.task_time.strftime('%H:%M')}  {pet_name:<8} {t.title}")
    else:
        print("    (none)")

# ── Demo: filter_tasks() by pet name ─────────────────────────────────────────

print()
print("=" * WIDTH)
print("  DEMO: filter_tasks(pet_name=...)".center(WIDTH))
print("  Shows tasks belonging to a specific pet".center(WIDTH))
print("=" * WIDTH)

for name in ["Buddy", "Luna"]:
    filtered = scheduler.filter_tasks(pet_name=name)
    print(f"\n  [{name}]  ({len(filtered)} task(s))")
    for t in scheduler.sort_by_time(filtered):
        print(f"    {t.task_time.strftime('%H:%M')}  {t.title:<26} [{t.status}]")

# ── Demo: filter_tasks() combining both ──────────────────────────────────────

print()
print("=" * WIDTH)
print("  DEMO: filter_tasks(pet_name=..., status=...)".center(WIDTH))
print("  Combined filter: Buddy's pending tasks".center(WIDTH))
print("=" * WIDTH)

combined = scheduler.filter_tasks(pet_name="Buddy", status="pending")
print(f"\n  Buddy | pending  ({len(combined)} task(s))")
for t in scheduler.sort_by_time(combined):
    print(f"    {t.task_time.strftime('%H:%M')}  {t.title}")

# ── Full schedule (original plan) ─────────────────────────────────────────────

total_scheduled = sum(t.duration for t in plan)
remaining_time = owner.available_time - total_scheduled

print()
print("=" * WIDTH)
print("  PawPal -- Today's Schedule".center(WIDTH))
print(f"  {today.strftime('%A, %B %d, %Y')}".center(WIDTH))
print("=" * WIDTH)
print(f"  Owner : {owner.name}")
print(f"  Budget: {owner.available_time} min  |  {total_scheduled} min scheduled  |  {remaining_time} min free")
print("-" * WIDTH)
print(f"  {'#':<3} {'Time':<7} {'Pet':<8} {'Task':<22} {'Min':>4}  {'Pri':>5}")
print("-" * WIDTH)

for i, task in enumerate(plan, start=1):
    pet = owner.get_pet(task.pet_id)
    pet_name = pet.pet_name if pet else "?"
    priority_bar = "[" + "#" * task.priority + "." * (3 - task.priority) + "]"
    req_marker = "*" if task.required else " "
    print(f"  {i:<3} {task.task_time.strftime('%H:%M'):<7} {pet_name:<8} {task.title:<22} {task.duration:>3}m  {priority_bar}{req_marker}")

print("-" * WIDTH)
print(f"  Total: {total_scheduled} / {owner.available_time} min used  ({remaining_time} min remaining)")

if scheduler.conflicts:
    print()
    for warning in scheduler.conflicts:
        print(f"  !! {warning}")

print("=" * WIDTH)
print()

# ── Demo: detect_conflicts() — same-pet and cross-pet warnings ────────────────

print()
print("=" * WIDTH)
print("  DEMO: detect_conflicts()".center(WIDTH))
print("  Lightweight conflict detection — warns, never crashes".center(WIDTH))
print("=" * WIDTH)
print()
print("  Tasks in today's plan that overlap:")
print("  " + "-" * (WIDTH - 2))

all_warnings = scheduler.detect_conflicts()   # checks ALL of today's tasks
if all_warnings:
    for warning in all_warnings:
        print(f"  {warning}")
else:
    print("  No conflicts detected.")

print()
print("  Key:")
print("  [same pet]   two tasks for ONE pet overlap - can't do both at once")
print("  [owner time] tasks for DIFFERENT pets overlap - owner only has one set of hands")
print("=" * WIDTH)
print()

# ── Demo: complete_task() auto-schedules next occurrence ──────────────────────

print()
print("=" * WIDTH)
print("  DEMO: complete_task() — auto-schedule next occurrence".center(WIDTH))
print("=" * WIDTH)

# Complete two recurring tasks and capture the auto-generated next instances
to_complete = [
    (4, "Luna Breakfast",    "daily"),   # still pending — not touched by filter demo
    (2, "Allergy Medication","daily"),   # required recurring task
    (5, "Evening Grooming",  "weekly"),  # weekly recurring task
]

print()
for task_id, label, freq in to_complete:
    next_task = scheduler.complete_task(task_id)
    original = next((t for t in owner.get_tasks() if t.task_id == task_id), None)
    if next_task:
        print(f"  [[x]] '{label}' marked complete  ({freq})")
        print(f"      Next occurrence scheduled:")
        print(f"        date  : {next_task.task_date.strftime('%A, %B %d, %Y')}")
        print(f"        time  : {next_task.task_time.strftime('%H:%M')}")
        print(f"        id    : {next_task.task_id}")
        print(f"        status: {next_task.status}")
    else:
        print(f"  [[x]] '{label}' marked complete  (no recurrence)")
    print()

# Show all tasks now registered, grouped by date, to confirm new instances exist
all_tasks = scheduler.sort_by_time(owner.get_tasks())
all_tasks_by_date = {}
for t in all_tasks:
    all_tasks_by_date.setdefault(t.task_date, []).append(t)

print("  Full task list after completions (all dates):")
print("  " + "-" * (WIDTH - 2))
for d in sorted(all_tasks_by_date):
    label = "TODAY" if d == today else d.strftime("%A, %B %d")
    print(f"  {label}")
    for t in all_tasks_by_date[d]:
        pet = owner.get_pet(t.pet_id)
        pet_name = pet.pet_name if pet else "?"
        status_icon = "[x]" if t.status == "completed" else "[ ]"
        print(f"    {status_icon} {t.task_time.strftime('%H:%M')}  {pet_name:<8} {t.title:<24} [{t.status}]")
    print()

print("=" * WIDTH)
print()