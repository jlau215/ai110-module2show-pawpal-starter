import streamlit as st
from datetime import date, time
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

# ── Session state vault ───────────────────────────────────────────────────────
if "owner" not in st.session_state:
    st.session_state.owner = None
if "next_pet_id" not in st.session_state:
    st.session_state.next_pet_id = 1
if "next_task_id" not in st.session_state:
    st.session_state.next_task_id = 1
if "plan" not in st.session_state:
    st.session_state.plan = []

# ── Section 1: Owner & Pet setup ──────────────────────────────────────────────
st.subheader("1. Owner & Pet Setup")

col1, col2 = st.columns(2)
with col1:
    owner_name     = st.text_input("Owner name", value="Jordan")
    available_time = st.number_input("Available time today (min)", min_value=10, max_value=480, value=120)
with col2:
    pet_name = st.text_input("Pet name", value="Mochi")
    species  = st.selectbox("Species", ["Dog", "Cat", "Other"])
    breed    = st.text_input("Breed", value="Mixed")

if st.button("Save Owner & Pet"):
    if st.session_state.owner is not None:
        # Owner already exists — warn instead of silently wiping tasks
        st.warning("An owner already exists. Saving again will reset all pets and tasks.")
    owner = Owner(owner_id=1, name=owner_name, available_time=int(available_time))
    pet = Pet(
        pet_id=st.session_state.next_pet_id,
        pet_name=pet_name,
        species=species,
        breed=breed,
        pet_dob=date(2020, 1, 1),
    )
    owner.add_pet(pet)
    st.session_state.owner        = owner
    st.session_state.next_pet_id  = st.session_state.next_pet_id + 1
    st.session_state.next_task_id = 1
    st.session_state.plan         = []     # clear stale plan when owner resets
    st.success(f"Saved! Owner: {owner_name} | Pet: {pet_name} ({species})")

if st.session_state.owner:
    o = st.session_state.owner
    pets_str = ", ".join(p.pet_name for p in o.pets)
    st.caption(f"Active owner: **{o.name}** — Pets: {pets_str} — Budget: {o.available_time} min")

st.divider()

# ── Section 2: Add a task ─────────────────────────────────────────────────────
st.subheader("2. Add a Task")

PRIORITY_MAP = {"Low": 1, "Medium": 2, "High": 3}

if st.session_state.owner is None:
    st.info("Save an owner and pet above before adding tasks.")
else:
    owner = st.session_state.owner
    pet   = owner.pets[0] if owner.pets else None

    col1, col2, col3 = st.columns(3)
    with col1:
        task_title     = st.text_input("Task title", value="Morning walk")
        task_type      = st.selectbox("Type", ["walk", "feeding", "meds", "grooming", "enrichment", "appointment"])
    with col2:
        duration       = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
        priority_label = st.selectbox("Priority", ["Low", "Medium", "High"], index=2)
    with col3:
        task_date_input = st.date_input("Date", value=date.today())
        task_time_input = st.time_input("Time", value=time(8, 0))

    if st.button("Add Task"):
        if pet is None:
            st.error("No pet found. Save a pet first.")
        else:
            task = Task(
                task_id     = st.session_state.next_task_id,
                pet_id      = pet.pet_id,
                title       = task_title,
                task_type   = task_type,
                description = task_title,
                duration    = int(duration),
                task_date   = task_date_input,
                task_time   = task_time_input,
                priority    = PRIORITY_MAP[priority_label],
            )
            owner.add_task(task)
            st.session_state.next_task_id += 1
            st.success(f"Added: {task_title} ({duration} min, priority {PRIORITY_MAP[priority_label]})")

    all_tasks = owner.get_tasks()
    if all_tasks:
        st.write(f"**{len(all_tasks)} task(s) on record:**")
        st.table([{
            "Title"         : t.title,
            "Type"          : t.task_type,
            "Date"          : str(t.task_date),
            "Time"          : t.task_time.strftime("%H:%M"),
            "Duration (min)": t.duration,
            "Priority"      : t.priority,
            "Status"        : t.status,
        } for t in all_tasks])
    else:
        st.info("No tasks yet. Add one above.")

st.divider()

# ── Section 3: Generate schedule ──────────────────────────────────────────────
st.subheader("3. Generate Today's Schedule")

if st.session_state.owner is None:
    st.info("Set up an owner and tasks first.")
else:
    if st.button("Generate Schedule"):
        owner     = st.session_state.owner
        scheduler = Scheduler(owner=owner, schedule_date=date.today())
        st.session_state.plan = scheduler.generate_plan()  # persisted — survives reruns

    # Display from session_state so the table stays visible after any widget interaction
    plan = st.session_state.plan
    if plan:
        owner     = st.session_state.owner
        total_min = sum(t.duration for t in plan)
        st.success(f"{len(plan)} task(s) scheduled — {total_min} / {owner.available_time} min used")
        rows = []
        for t in plan:
            matched_pet = owner.get_pet(t.pet_id)          # safe None check
            rows.append({
                "Time"          : t.task_time.strftime("%H:%M"),
                "Task"          : t.title,
                "Type"          : t.task_type,
                "Pet"           : matched_pet.pet_name if matched_pet else "?",
                "Duration (min)": t.duration,
                "Priority"      : t.priority,
                "Status"        : t.status,
            })
        st.table(rows)
    elif st.session_state.owner:
        st.info("Click 'Generate Schedule' to build today's plan.")
