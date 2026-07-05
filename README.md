# PawPal+ — Pet Care Scheduler

A Streamlit app that helps pet owners plan and manage daily care tasks across multiple pets. PawPal+ applies scheduling algorithms — priority sorting, time-conflict detection, and recurring task management — to produce a daily plan that fits within the owner's available time budget.

---

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track care tasks across multiple pets (walks, feeding, meds, enrichment, grooming, vet appointments)
- Respect constraints: time budget, task priority, and required tasks (e.g., medication)
- Detect and warn about scheduling conflicts before the day starts
- Auto-schedule the next occurrence when a recurring task is completed

---

## Features

### Scheduling Algorithms

| Feature | Method | Behavior |
|---|---|---|
| **Chronological sort** | `Scheduler.sort_by_time()` | Returns tasks ordered earliest → latest by `task_time`; never mutates the input list |
| **Priority sort** | `Scheduler.prioritize_tasks()` | Sorts today's tasks by priority descending, then by time ascending to break ties |
| **Daily plan generation** | `Scheduler.generate_plan()` | Required tasks (e.g., meds) are always included first; optional tasks fill the remaining time budget by priority order; final plan is sorted chronologically |
| **Time-conflict detection** | `Scheduler.detect_conflicts()` | Checks every pair of tasks for overlap using interval math (`a_start < b_end AND b_start < a_end`); distinguishes same-pet overlaps from cross-pet owner-time conflicts; returns warning strings and never crashes |
| **Status + pet filtering** | `Scheduler.filter_tasks()` | Filter by `status` (`pending` / `completed` / `skipped`) and/or `pet_name` (case-insensitive); both filters apply as AND logic when combined |
| **Recurring task completion** | `Scheduler.complete_task()` | Marks a task complete and auto-creates the next occurrence: +1 day for `daily`, +7 days for `weekly`; `once` tasks just close out |
| **Recurring task expansion** | `Scheduler.expand_recurring()` | Clones all recurring tasks forward N days, assigning unique IDs to each clone; used for weekly planning |
| **Plan summary** | `Scheduler.explain_plan()` | Returns a human-readable string: total tasks, required vs. optional counts, total minutes, and any conflict warnings |

### Data Model

| Class | Responsibility |
|---|---|
| `Task` | Single care activity — title, type, date, time, duration, priority, frequency, required flag |
| `Pet` | Pet profile; owns its own task list; computes age from DOB |
| `Owner` | Manages multiple pets via O(1) dict index; aggregates tasks across all pets; stores the last generated plan |
| `Scheduler` | Brain — retrieves, organizes, and manages tasks; holds `daily_plan` and `conflicts` lists after `generate_plan()` |

### Streamlit UI

- **Owner Profile** — Create an owner once; update name and time budget any time without wiping pets or tasks
- **Add a Pet** — Additive: add any number of pets to an existing owner; each pet gets its own profile (name, species, breed, DOB)
- **Add a Task** — Assign tasks to a specific pet via dropdown; set type, duration, priority, required flag, frequency, date, and time
- **Sort & Filter view** — Sort all tasks chronologically or by priority; filter by status and/or pet; live caption shows matching count and total minutes
- **Generate Schedule** — Runs `generate_plan()` and displays the day's plan; conflict warnings appear as `st.warning()` banners with plain-English messages and suggested reschedule times; conflicting rows are highlighted amber in the plan table
- **Mark Task Complete** — Select any pending task from a dropdown sorted by time; completing a recurring task shows the auto-scheduled next occurrence

---

## Getting Started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Run the Streamlit app

```bash
streamlit run app.py
```

### Run the CLI demo

```bash
python main.py
```

---

## Demo Walkthrough

### UI workflow

**Step 1 — Create an owner**
Open the "Owner Profile" expander. Enter a name (e.g., `Jordan`) and set today's available time (e.g., `120 min`). Click **Save Owner**. The status bar at the bottom of Section 1 confirms the owner and shows their time budget.

**Step 2 — Add pets**
Open the "Add a Pet" expander. Enter `Buddy` (Dog, Labrador). Click **Add Pet**. Repeat for `Luna` (Cat, Siamese). The status bar updates to show both pets.

**Step 3 — Add tasks**
In Section 2, use the "For pet" dropdown to choose which pet each task belongs to. Add several tasks at overlapping or adjacent times to see the conflict system in action. Examples:

| Pet | Task | Time | Duration | Priority | Required |
|---|---|---|---|---|---|
| Buddy | Morning Walk | 07:00 | 30 min | High | No |
| Buddy | Vet Check | 07:00 | 20 min | Medium | No |
| Luna | Allergy Medication | 08:00 | 5 min | High | **Yes** |
| Luna | Luna Breakfast | 08:00 | 10 min | Medium | No |
| Buddy | Evening Grooming | 18:00 | 20 min | Low | No |

**Step 4 — Generate the schedule**
Click **Generate Schedule** in Section 3. PawPal+ runs `generate_plan()`:
- Required tasks (Allergy Medication) are locked in first regardless of time budget.
- Optional tasks fill the remaining budget in priority order.
- The final plan is sorted chronologically.

If any tasks overlap, amber-highlighted rows appear in the table alongside `st.warning()` banners like:

> ⚠️ **Buddy** has 2 tasks at 07:00 — **Morning Walk** and **Vet Check** overlap.
> → Move **Vet Check** to 07:35 or later to clear the overlap.

If the plan is clean, a green banner confirms: ✅ No scheduling conflicts detected.

**Step 5 — Mark a task complete**
In Section 4, select a pending task from the sorted dropdown and click **Mark Complete**. For daily/weekly tasks, a success banner shows the auto-scheduled next occurrence date and time. The plan clears so you can regenerate with updated statuses.

---

### Sample CLI output (`python main.py`)

```
==============================================================
            DEMO: sort_by_time()
  Tasks as added (out of order) vs sorted by time
==============================================================

  --- As Added (insertion order) ---
  #   Time    Pet      Task
  ------------------------------------------------------------
  1   18:00   Buddy    Evening Grooming
  2   08:00   Luna     Allergy Medication
  3   08:00   Luna     Luna Breakfast
  4   07:00   Buddy    Morning Walk
  5   07:30   Buddy    Buddy Breakfast

  --- After sort_by_time() ---
  #   Time    Pet      Task
  ------------------------------------------------------------
  1   07:00   Buddy    Morning Walk
  2   07:00   Luna     Morning Stretch
  3   07:00   Buddy    Vet Check
  4   07:30   Buddy    Buddy Breakfast
  5   08:00   Luna     Allergy Medication
  6   08:00   Luna     Luna Breakfast
  7   18:00   Buddy    Evening Grooming

==============================================================
            DEMO: filter_tasks(status=...)
  Shows which tasks are done vs still pending
==============================================================

  [Completed]  (2 task(s))
    07:00  Buddy    Morning Walk
    07:30  Buddy    Buddy Breakfast

  [Pending]  (5 task(s))
    07:00  Luna     Morning Stretch
    07:00  Buddy    Vet Check
    08:00  Luna     Allergy Medication
    08:00  Luna     Luna Breakfast
    18:00  Buddy    Evening Grooming

==============================================================
               PawPal -- Today's Schedule
                  Saturday, July 05, 2026
==============================================================
  Owner : Alex
  Budget: 120 min  |  110 min scheduled  |  10 min free
------------------------------------------------------------
  #   Time    Pet      Task                    Min    Pri
------------------------------------------------------------
  1   07:00   Buddy    Morning Walk            30m  [###]
  2   07:00   Luna     Morning Stretch         15m  [#..]
  3   07:00   Buddy    Vet Check               20m  [##.]
  4   07:30   Buddy    Buddy Breakfast         10m  [##.]
  5   08:00   Luna     Allergy Medication       5m  [###]*
  6   08:00   Luna     Luna Breakfast          10m  [##.]
  7   18:00   Buddy    Evening Grooming        20m  [#..]
------------------------------------------------------------
  Total: 110 / 120 min used  (10 min remaining)

  !! WARNING [same pet]   'Morning Walk' and 'Vet Check' overlap for Buddy (07:00 vs 07:00)
  !! WARNING [owner time] 'Morning Walk' (Buddy) and 'Morning Stretch' (Luna) overlap (07:00 vs 07:00) -- owner cannot do both at once
  !! WARNING [same pet]   'Allergy Medication' and 'Luna Breakfast' overlap for Luna (08:00 vs 08:00)
==============================================================

==============================================================
             DEMO: detect_conflicts()
  Lightweight conflict detection — warns, never crashes
==============================================================

  Tasks in today's plan that overlap:
  ------------------------------------------------------------
  WARNING [same pet]   'Morning Walk' and 'Vet Check' overlap for Buddy (07:00 vs 07:00)
  WARNING [owner time] 'Morning Walk' (Buddy) and 'Morning Stretch' (Luna) overlap (07:00 vs 07:00) -- owner cannot do both at once
  WARNING [same pet]   'Allergy Medication' and 'Luna Breakfast' overlap for Luna (08:00 vs 08:00)

  Key:
  [same pet]   two tasks for ONE pet overlap - can't do both at once
  [owner time] tasks for DIFFERENT pets overlap - owner only has one set of hands
==============================================================

==============================================================
     DEMO: complete_task() — auto-schedule next occurrence
==============================================================

  [[x]] 'Luna Breakfast' marked complete  (daily)
      Next occurrence scheduled:
        date  : Sunday, July 06, 2026
        time  : 08:00
        id    : 8
        status: pending

  [[x]] 'Allergy Medication' marked complete  (daily)
      Next occurrence scheduled:
        date  : Sunday, July 06, 2026
        time  : 08:00
        id    : 9
        status: pending

  [[x]] 'Evening Grooming' marked complete  (weekly)
      Next occurrence scheduled:
        date  : Saturday, July 12, 2026
        time  : 18:00
        id    : 10
        status: pending
==============================================================
```

> `*` in the Pri column marks required tasks — always included regardless of time budget.

---

## 📐 Smarter Scheduling

| Feature | Method(s) | Detail |
|---|---|---|
| Chronological sort | `sort_by_time()` | Returns a new sorted list; input list never mutated |
| Priority sort | `prioritize_tasks()` | Priority descending; ties broken by earlier `task_time` |
| Budget-aware plan | `generate_plan()` | Required tasks always in; optional tasks fill by priority until budget exhausted |
| Conflict detection | `detect_conflicts()` | All-pairs interval overlap check; separate labels for same-pet vs. cross-pet conflicts |
| Task filtering | `filter_tasks()` | AND-logic filter by `status` and/or `pet_name` (case-insensitive) |
| Recurring completion | `complete_task()` | Marks done; clones task to next day (daily) or next week (weekly) with a fresh unique ID |
| Future expansion | `expand_recurring()` | Clones all recurring tasks forward N days; unique IDs guaranteed across all clones |
| Plan explanation | `explain_plan()` | Human-readable summary string with task counts, minutes used, and any conflict warnings |

---

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
collected 40 items

tests\test_pawpal.py ........................................  [100%]

======================================================================== 40 passed in 0.08s =========================================================================
```

Test coverage includes:
- `sort_by_time` — happy path, empty list, same-time ties, no mutation of input
- `prioritize_tasks` — correct priority order, ties broken by time, today-only scope
- `filter_tasks` — by status, by pet name (case-insensitive), combined AND, no-match edge cases
- `detect_conflicts` — no tasks, no overlap, adjacent (not a conflict), same-pet overlap, cross-pet overlap, partial overlap
- `generate_plan` — all tasks fit, required task with zero budget, optional dropped when full, no pets, chronological output order
- `complete_task` — once/daily/weekly recurrence, already-completed guard, invalid ID, same time preserved, unique IDs
- `expand_recurring` — daily N days, weekly one instance, once not expanded, zero days, unique IDs across multiple tasks