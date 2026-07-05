import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from datetime import date, time, timedelta
from pawpal_system import Owner, Pet, Task, Scheduler


# ── Helpers ───────────────────────────────────────────────────────────────────

TODAY = date(2026, 7, 5)


def make_task(task_id=1, pet_id=1, title="Morning Walk", task_time=time(7, 0),
              duration=30, priority=2, frequency="once",
              task_date=TODAY, required=False, status="pending"):
    """Helper: returns a minimal Task with sensible defaults."""
    return Task(
        task_id=task_id,
        pet_id=pet_id,
        title=title,
        task_type="walk",
        description="Walk around the block.",
        duration=duration,
        task_date=task_date,
        task_time=task_time,
        priority=priority,
        frequency=frequency,
        required=required,
        status=status,
    )


def make_pet(pet_id=1, name="Buddy"):
    """Helper: returns a minimal Pet."""
    return Pet(
        pet_id=pet_id,
        pet_name=name,
        species="Dog",
        breed="Labrador",
        pet_dob=date(2020, 3, 15),
    )


def make_owner(available_time=120):
    return Owner(owner_id=1, name="Alex", available_time=available_time)


def make_scheduler(owner, schedule_date=TODAY):
    return Scheduler(owner=owner, schedule_date=schedule_date)


# ── Original Tests ────────────────────────────────────────────────────────────

def test_mark_complete_changes_status():
    """Happy path: pending task becomes completed."""
    task = make_task()
    assert task.status == "pending"
    task.mark_complete()
    assert task.status == "completed"


def test_add_task_increases_pet_task_count():
    """Happy path: tasks routed to correct pet."""
    owner = make_owner()
    pet = make_pet()
    owner.add_pet(pet)

    assert len(pet.tasks) == 0

    owner.add_task(make_task(task_id=1, pet_id=pet.pet_id))
    owner.add_task(make_task(task_id=2, pet_id=pet.pet_id))

    assert len(pet.tasks) == 2


# ── sort_by_time ──────────────────────────────────────────────────────────────

def test_sort_by_time_happy_path():
    """Tasks inserted out of order come back sorted chronologically."""
    owner = make_owner()
    pet = make_pet()
    owner.add_pet(pet)
    t_late  = make_task(1, 1, task_time=time(18, 0))
    t_early = make_task(2, 1, task_time=time(7, 0))
    t_mid   = make_task(3, 1, task_time=time(9, 30))
    sched = make_scheduler(owner)
    result = sched.sort_by_time([t_late, t_early, t_mid])
    assert [t.task_time for t in result] == [time(7, 0), time(9, 30), time(18, 0)]


def test_sort_by_time_empty_list():
    """Edge case: sorting an empty list returns empty, no crash."""
    owner = make_owner()
    sched = make_scheduler(owner)
    assert sched.sort_by_time([]) == []


def test_sort_by_time_two_tasks_same_time():
    """Edge case: two tasks at identical time — both returned, order stable."""
    owner = make_owner()
    pet = make_pet()
    owner.add_pet(pet)
    t1 = make_task(1, 1, title="Feed",  task_time=time(8, 0))
    t2 = make_task(2, 1, title="Meds",  task_time=time(8, 0))
    sched = make_scheduler(owner)
    result = sched.sort_by_time([t1, t2])
    assert len(result) == 2
    assert result[0].task_time == result[1].task_time == time(8, 0)


def test_sort_by_time_does_not_mutate_input():
    """sort_by_time must return a new list, not reorder the original."""
    owner = make_owner()
    pet = make_pet()
    owner.add_pet(pet)
    t1 = make_task(1, 1, task_time=time(10, 0))
    t2 = make_task(2, 1, task_time=time(7, 0))
    original = [t1, t2]
    make_scheduler(owner).sort_by_time(original)
    assert original[0] is t1  # unchanged


# ── prioritize_tasks ──────────────────────────────────────────────────────────

def test_prioritize_tasks_happy_path():
    """High-priority tasks appear first; ties broken by earlier time."""
    owner = make_owner()
    pet = make_pet()
    owner.add_pet(pet)
    lo_pri = make_task(1, 1, priority=1, task_time=time(7, 0))
    hi_late = make_task(2, 1, priority=3, task_time=time(9, 0))
    hi_early = make_task(3, 1, priority=3, task_time=time(8, 0))
    owner.add_task(lo_pri); owner.add_task(hi_late); owner.add_task(hi_early)
    result = make_scheduler(owner).prioritize_tasks()
    # priority-3 tasks first, then priority-1
    assert result[0].priority == 3
    assert result[1].priority == 3
    assert result[2].priority == 1
    # within priority-3 tie, earlier time first
    assert result[0].task_time < result[1].task_time


def test_prioritize_tasks_only_today():
    """Tasks on other dates must not appear in today's prioritized list."""
    owner = make_owner()
    pet = make_pet()
    owner.add_pet(pet)
    t_today    = make_task(1, 1, task_date=TODAY)
    t_tomorrow = make_task(2, 1, task_date=TODAY + timedelta(days=1))
    owner.add_task(t_today); owner.add_task(t_tomorrow)
    result = make_scheduler(owner).prioritize_tasks()
    assert len(result) == 1
    assert result[0].task_id == 1


# ── filter_tasks ──────────────────────────────────────────────────────────────

def test_filter_by_status_completed():
    """Happy path: filter returns only completed tasks."""
    owner = make_owner()
    pet = make_pet()
    owner.add_pet(pet)
    done    = make_task(1, 1, title="Walk",  status="completed")
    pending = make_task(2, 1, title="Feed",  status="pending")
    owner.add_task(done); owner.add_task(pending)
    result = make_scheduler(owner).filter_tasks(status="completed")
    assert len(result) == 1
    assert result[0].title == "Walk"


def test_filter_by_pet_name_case_insensitive():
    """Happy path: pet name filter ignores case."""
    owner = make_owner()
    buddy = make_pet(pet_id=1, name="Buddy")
    luna  = make_pet(pet_id=2, name="Luna")
    owner.add_pet(buddy); owner.add_pet(luna)
    owner.add_task(make_task(1, 1))
    owner.add_task(make_task(2, 2))
    result = make_scheduler(owner).filter_tasks(pet_name="buddy")  # lowercase
    assert len(result) == 1
    assert result[0].pet_id == 1


def test_filter_combined_and():
    """Happy path: status + pet_name both applied (AND logic)."""
    owner = make_owner()
    pet = make_pet(pet_id=1, name="Buddy")
    owner.add_pet(pet)
    done    = make_task(1, 1, title="Walk", status="completed")
    pending = make_task(2, 1, title="Feed", status="pending")
    owner.add_task(done); owner.add_task(pending)
    result = make_scheduler(owner).filter_tasks(pet_name="Buddy", status="pending")
    assert len(result) == 1
    assert result[0].title == "Feed"


def test_filter_no_match_returns_empty():
    """Edge case: filter with no matching tasks returns []."""
    owner = make_owner()
    pet = make_pet()
    owner.add_pet(pet)
    owner.add_task(make_task(1, 1, status="pending"))
    result = make_scheduler(owner).filter_tasks(status="skipped")
    assert result == []


def test_filter_unknown_pet_returns_empty():
    """Edge case: filtering by a pet name that doesn't exist returns []."""
    owner = make_owner()
    pet = make_pet(name="Buddy")
    owner.add_pet(pet)
    owner.add_task(make_task(1, 1))
    result = make_scheduler(owner).filter_tasks(pet_name="Ghost")
    assert result == []


# ── detect_conflicts ──────────────────────────────────────────────────────────

def test_no_tasks_no_conflicts():
    """Edge case: empty task list → no warnings."""
    owner = make_owner()
    sched = make_scheduler(owner)
    assert sched.detect_conflicts([]) == []


def test_non_overlapping_tasks_no_conflict():
    """Happy path: tasks far apart → no conflict."""
    owner = make_owner()
    pet = make_pet()
    owner.add_pet(pet)
    t1 = make_task(1, 1, task_time=time(7, 0),  duration=30)  # ends 07:30
    t2 = make_task(2, 1, task_time=time(9, 0),  duration=30)  # starts 09:00
    sched = make_scheduler(owner)
    assert sched.detect_conflicts([t1, t2]) == []


def test_adjacent_tasks_are_not_a_conflict():
    """Edge case: task ending at 07:30, next starting at 07:30 — NOT a conflict."""
    owner = make_owner()
    pet = make_pet()
    owner.add_pet(pet)
    t1 = make_task(1, 1, task_time=time(7, 0),  duration=30)  # ends exactly 07:30
    t2 = make_task(2, 1, task_time=time(7, 30), duration=30)  # starts exactly 07:30
    sched = make_scheduler(owner)
    assert sched.detect_conflicts([t1, t2]) == []


def test_same_pet_same_time_conflict():
    """Edge case: two tasks for one pet at identical time → [same pet] warning."""
    owner = make_owner()
    pet = make_pet()
    owner.add_pet(pet)
    t1 = make_task(1, 1, title="Walk",     task_time=time(7, 0), duration=30)
    t2 = make_task(2, 1, title="Vet Check",task_time=time(7, 0), duration=20)
    sched = make_scheduler(owner)
    warnings = sched.detect_conflicts([t1, t2])
    assert len(warnings) == 1
    assert "[same pet]" in warnings[0]


def test_cross_pet_same_time_conflict():
    """Edge case: tasks for different pets overlap → [owner time] warning."""
    owner = make_owner()
    buddy = make_pet(pet_id=1, name="Buddy")
    luna  = make_pet(pet_id=2, name="Luna")
    owner.add_pet(buddy); owner.add_pet(luna)
    t1 = make_task(1, 1, title="Walk",     task_time=time(7, 0), duration=30)
    t2 = make_task(2, 2, title="Meds",     task_time=time(7, 0), duration=10)
    sched = make_scheduler(owner)
    warnings = sched.detect_conflicts([t1, t2])
    assert len(warnings) == 1
    assert "[owner time]" in warnings[0]


def test_partial_overlap_detected():
    """Edge case: t1 07:00–07:30, t2 07:15–07:45 → overlap flagged."""
    owner = make_owner()
    pet = make_pet()
    owner.add_pet(pet)
    t1 = make_task(1, 1, task_time=time(7, 0),  duration=30)
    t2 = make_task(2, 1, task_time=time(7, 15), duration=30)
    sched = make_scheduler(owner)
    assert len(sched.detect_conflicts([t1, t2])) == 1


# ── generate_plan ─────────────────────────────────────────────────────────────

def test_generate_plan_happy_path():
    """Happy path: optional tasks fit within budget → all included."""
    owner = make_owner(available_time=60)
    pet = make_pet()
    owner.add_pet(pet)
    t1 = make_task(1, 1, duration=20, priority=2)
    t2 = make_task(2, 1, duration=20, priority=1)
    owner.add_task(t1); owner.add_task(t2)
    plan = make_scheduler(owner).generate_plan()
    assert t1 in plan and t2 in plan
    assert sum(t.duration for t in plan) <= 60


def test_generate_plan_required_task_always_included():
    """Edge case: zero available time — required task still appears in plan."""
    owner = make_owner(available_time=0)
    pet = make_pet()
    owner.add_pet(pet)
    req = make_task(1, 1, title="Meds", duration=10, required=True)
    opt = make_task(2, 1, title="Walk", duration=30, required=False)
    owner.add_task(req); owner.add_task(opt)
    plan = make_scheduler(owner).generate_plan()
    assert req in plan
    assert opt not in plan


def test_generate_plan_optional_excluded_when_full():
    """Edge case: lowest-priority optional task dropped when budget is full."""
    owner = make_owner(available_time=30)
    pet = make_pet()
    owner.add_pet(pet)
    fills  = make_task(1, 1, duration=30, priority=3)  # uses full budget
    excess = make_task(2, 1, duration=10, priority=1)  # won't fit
    owner.add_task(fills); owner.add_task(excess)
    plan = make_scheduler(owner).generate_plan()
    assert fills in plan
    assert excess not in plan


def test_generate_plan_no_pets_empty_plan():
    """Edge case: owner with no pets → empty plan."""
    owner = make_owner()
    plan = make_scheduler(owner).generate_plan()
    assert plan == []


def test_generate_plan_sorted_by_time():
    """Plan is always returned in chronological order regardless of priority."""
    owner = make_owner(available_time=120)
    pet = make_pet()
    owner.add_pet(pet)
    t_late  = make_task(1, 1, task_time=time(18, 0), priority=3, duration=20)
    t_early = make_task(2, 1, task_time=time(7, 0),  priority=1, duration=20)
    owner.add_task(t_late); owner.add_task(t_early)
    plan = make_scheduler(owner).generate_plan()
    times = [t.task_time for t in plan]
    assert times == sorted(times)


def test_get_schedule_returns_last_plan():
    """owner.get_schedule() reflects whatever generate_plan() last produced."""
    owner = make_owner(available_time=60)
    pet = make_pet()
    owner.add_pet(pet)
    owner.add_task(make_task(1, 1))
    sched = make_scheduler(owner)
    plan = sched.generate_plan()
    assert owner.get_schedule() == plan


# ── complete_task (recurring logic) ──────────────────────────────────────────

def test_complete_once_task_no_recurrence():
    """Happy path: 'once' task marked complete, no new task created."""
    owner = make_owner()
    pet = make_pet()
    owner.add_pet(pet)
    task = make_task(1, 1, frequency="once")
    owner.add_task(task)
    result = make_scheduler(owner).complete_task(1)
    assert result is None
    assert task.status == "completed"


def test_complete_daily_task_creates_next_day():
    """Happy path: completing a daily task auto-schedules tomorrow."""
    owner = make_owner()
    pet = make_pet()
    owner.add_pet(pet)
    task = make_task(1, 1, frequency="daily", task_date=TODAY)
    owner.add_task(task)
    next_task = make_scheduler(owner).complete_task(1)
    assert next_task is not None
    assert next_task.task_date == TODAY + timedelta(days=1)
    assert next_task.frequency == "daily"
    assert next_task.status == "pending"


def test_complete_weekly_task_creates_next_week():
    """Happy path: completing a weekly task auto-schedules 7 days later."""
    owner = make_owner()
    pet = make_pet()
    owner.add_pet(pet)
    task = make_task(1, 1, frequency="weekly", task_date=TODAY)
    owner.add_task(task)
    next_task = make_scheduler(owner).complete_task(1)
    assert next_task is not None
    assert next_task.task_date == TODAY + timedelta(weeks=1)


def test_complete_task_already_completed_returns_none():
    """Edge case: completing an already-completed task → returns None (idempotent)."""
    owner = make_owner()
    pet = make_pet()
    owner.add_pet(pet)
    task = make_task(1, 1, frequency="daily", status="completed")
    owner.add_task(task)
    result = make_scheduler(owner).complete_task(1)
    assert result is None


def test_complete_task_invalid_id_returns_none():
    """Edge case: task ID that doesn't exist → returns None, no crash."""
    owner = make_owner()
    result = make_scheduler(owner).complete_task(999)
    assert result is None


def test_complete_task_next_inherits_same_time():
    """Recurring task's next occurrence must keep the same task_time."""
    owner = make_owner()
    pet = make_pet()
    owner.add_pet(pet)
    task = make_task(1, 1, frequency="daily", task_time=time(8, 30))
    owner.add_task(task)
    next_task = make_scheduler(owner).complete_task(1)
    assert next_task is not None
    assert next_task.task_time == time(8, 30)


def test_complete_task_next_id_is_unique():
    """Two completed daily tasks must produce next tasks with different IDs."""
    owner = make_owner()
    pet = make_pet()
    owner.add_pet(pet)
    t1 = make_task(1, 1, title="Walk", frequency="daily")
    t2 = make_task(5, 1, title="Feed", frequency="daily")
    owner.add_task(t1); owner.add_task(t2)
    sched = make_scheduler(owner)
    n1 = sched.complete_task(1)
    n2 = sched.complete_task(5)
    assert n1 is not None and n2 is not None
    assert n1.task_id != n2.task_id


# ── expand_recurring ──────────────────────────────────────────────────────────

def test_expand_recurring_daily_n_days():
    """Happy path: daily task expands into exactly N new future tasks."""
    owner = make_owner()
    pet = make_pet()
    owner.add_pet(pet)
    task = make_task(1, 1, frequency="daily", task_date=TODAY)
    owner.add_task(task)
    new_tasks = make_scheduler(owner).expand_recurring(days=7)
    assert len(new_tasks) == 7
    dates = [t.task_date for t in new_tasks]
    assert dates == [TODAY + timedelta(days=i) for i in range(1, 8)]


def test_expand_recurring_weekly_one_instance():
    """Happy path: weekly task expands to exactly one task (+7 days)."""
    owner = make_owner()
    pet = make_pet()
    owner.add_pet(pet)
    task = make_task(1, 1, frequency="weekly", task_date=TODAY)
    owner.add_task(task)
    new_tasks = make_scheduler(owner).expand_recurring(days=7)
    assert len(new_tasks) == 1
    assert new_tasks[0].task_date == TODAY + timedelta(weeks=1)


def test_expand_recurring_once_not_expanded():
    """Edge case: 'once' task produces no expanded copies."""
    owner = make_owner()
    pet = make_pet()
    owner.add_pet(pet)
    task = make_task(1, 1, frequency="once")
    owner.add_task(task)
    assert make_scheduler(owner).expand_recurring(days=7) == []


def test_expand_recurring_zero_days_empty():
    """Edge case: expanding for 0 days returns nothing."""
    owner = make_owner()
    pet = make_pet()
    owner.add_pet(pet)
    task = make_task(1, 1, frequency="daily")
    owner.add_task(task)
    assert make_scheduler(owner).expand_recurring(days=0) == []


def test_expand_recurring_all_ids_unique():
    """Two daily tasks expanded 3 days must produce 6 tasks with distinct IDs."""
    owner = make_owner()
    pet = make_pet()
    owner.add_pet(pet)
    owner.add_task(make_task(1, 1, title="Walk", frequency="daily"))
    owner.add_task(make_task(2, 1, title="Feed", frequency="daily"))
    new_tasks = make_scheduler(owner).expand_recurring(days=3)
    ids = [t.task_id for t in new_tasks]
    assert len(ids) == len(set(ids))


# ── Pet with no tasks (edge case) ─────────────────────────────────────────────

def test_pet_with_no_tasks_get_tasks_empty():
    """Edge case: a pet that exists but has no tasks returns empty list."""
    owner = make_owner()
    pet = make_pet()
    owner.add_pet(pet)
    assert owner.get_tasks() == []


def test_pet_with_no_tasks_sort_by_time_empty():
    """Edge case: sort_by_time on a pet with no tasks → []."""
    owner = make_owner()
    pet = make_pet()
    owner.add_pet(pet)
    sched = make_scheduler(owner)
    assert sched.sort_by_time(owner.get_tasks()) == []


def test_pet_with_no_tasks_generate_plan_empty():
    """Edge case: generate_plan with a pet but zero tasks → empty plan."""
    owner = make_owner()
    owner.add_pet(make_pet())
    plan = make_scheduler(owner).generate_plan()
    assert plan == []