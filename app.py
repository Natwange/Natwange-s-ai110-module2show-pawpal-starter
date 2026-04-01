import streamlit as st
from pawpal_system import PetOwner, Pet, Task, Scheduler
from datetime import date

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

# ── Owner form ────────────────────────────────────────────────────────────────
st.subheader("Owner Details")

with st.form("owner_form"):
    owner_name = st.text_input("Full name", value="Jordan")
    owner_email = st.text_input("Email", value="owner@example.com")
    owner_submitted = st.form_submit_button("Save owner")

if owner_submitted or "owner" not in st.session_state:
    st.session_state.owner = PetOwner(
        id=1,
        name=owner_name,
        email=owner_email,
    )
    if owner_submitted:
        st.success(f"Owner saved: {owner_name}")

owner = st.session_state.owner
st.caption(f"Current owner: **{owner.name}** — {owner.email}")

st.divider()

# ── Pet form ──────────────────────────────────────────────────────────────────
st.subheader("Pet Info")

with st.form("pet_form"):
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "rabbit", "bird", "other"])
    pet_age = st.number_input("Age (years)", min_value=0, max_value=30, value=2)
    pet_submitted = st.form_submit_button("Save pet")

if pet_submitted or "pet" not in st.session_state:
    st.session_state.pet = Pet(
        id=1,
        owner_id=owner.id,
        name=pet_name,
        species=species,
        age=pet_age,
    )
    if pet_submitted:
        st.success(f"Pet saved: {pet_name} ({species}, age {pet_age})")

pet = st.session_state.pet
st.caption(f"Current pet: **{pet.name}** — {pet.get_species()}, age {pet.get_age()}")

# ── Scheduler (created once, tied to pet) ─────────────────────────────────────
if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler(
        id=1,
        pet_id=pet.id,
        date=date.today(),
        status="active",
    )

owner.scheduler = st.session_state.scheduler

st.divider()

# ── Tasks ─────────────────────────────────────────────────────────────────────
st.subheader("Tasks")
st.caption("Add care tasks for your pet. These feed into the schedule.")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

PRIORITY_MAP = {"high": 1, "medium": 2, "low": 3}

if st.button("Add task"):
    new_task = Task(
        id=len(owner.get_tasks()) + 1,
        pet_id=pet.id,
        status="pending",
        description=task_title,
        frequency=1,
        time="08:00 AM",
        priority=PRIORITY_MAP[priority],
    )
    owner.add_task(new_task)
    st.success(f"Added task: {task_title}")

current_tasks = owner.get_tasks()

if current_tasks:
    st.write("Current tasks:")
    st.table([
        {
            "id": task.id,
            "description": task.description,
            "status": task.status,
            "frequency": task.frequency,
            "time": task.time,
        }
        for task in current_tasks
    ])
else:
    st.info("No tasks yet. Add one above.")

st.divider()

# ── Generate schedule ─────────────────────────────────────────────────────────
st.subheader("Build Schedule")

if st.button("Generate schedule"):
    plan = st.session_state.scheduler.generate_plan()
    if plan:
        st.success("Schedule generated!")
        st.table([
            {
                "id": task.id,
                "description": task.description,
                "priority": task.priority,
                "status": task.status,
                "frequency": task.frequency,
                "time": task.time,
            }
            for task in plan
        ])
    else:
        st.info("No tasks to schedule. Add some tasks first.")
