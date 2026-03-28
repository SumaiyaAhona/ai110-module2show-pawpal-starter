import streamlit as st
from datetime import datetime, timedelta
from pawpal_system import Task, Pet, Owner, Scheduler

# --- Page setup ---
st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

# --- Intro ---
st.markdown(
    """
Welcome to the PawPal+ app.

This demo shows your pet care tasks and schedule. Add pets, create tasks,
and see them sorted, with conflict detection and recurring tasks.
"""
)

# --- Session state setup ---
if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan", Scheduler())
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# --- Add Pet Section ---
st.subheader("Add a Pet")
owner_name = st.text_input("Owner name", value=st.session_state.owner.name)
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    if pet_name:
        st.session_state.owner.add_pet(Pet(pet_name, species))
        st.success(f"Pet '{pet_name}' added!")
    else:
        st.warning("Enter a pet name!")

# --- Add Task Section ---
st.subheader("Add a Task")
col1, col2, col3, col4 = st.columns(4)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
with col4:
    frequency = st.selectbox("Repeat", ["none", "daily", "weekly"])

if st.button("Add task"):
    if not st.session_state.owner.pets:
        st.warning("Add a pet first!")
    else:
        pet = next((p for p in st.session_state.owner.pets if p.name == pet_name), None)
        if pet:
            task = Task(
                task_title,
                datetime.now(),
                priority,
                int(duration),
                frequency=frequency if frequency != "none" else None
            )
            st.session_state.owner.schedule_task(pet, task)
            st.session_state.tasks.append({
                "title": task_title,
                "duration_minutes": int(duration),
                "priority": priority,
                "repeat": frequency,
                "pet": pet.name
            })
            st.success(f"Task '{task_title}' added to {pet.name}!")
        else:
            st.warning(f"No pet named '{pet_name}' found!")

# --- Show Current Tasks ---
st.markdown("### Current Tasks")
if st.session_state.tasks:
    st.table(st.session_state.tasks)
else:
    st.info("No tasks yet. Add one above.")

# --- Build Schedule Section ---
st.subheader("Build Schedule")
st.caption("Sorted tasks, conflict warnings, and recurring tasks.")

if st.button("Generate schedule"):
    scheduler = st.session_state.owner.scheduler
    pets = st.session_state.owner.pets

    if not pets:
        st.warning("No pets added yet. Add a pet and some tasks first.")
    else:
        for pet in pets:
            st.markdown(f"#### {pet.name} ({pet.type})")

            # Sort tasks
            sorted_tasks = scheduler.sort_by_time(pet=pet)
            if not sorted_tasks:
                st.info(f"No tasks scheduled for {pet.name}.")
                continue

            # Detect conflicts
            conflicts = scheduler.detect_conflicts(pet)

            # Display tasks
            table_rows = []
            for task in sorted_tasks:
                table_rows.append({
                    "Title": task.title,
                    "Time": task.time.strftime("%H:%M"),
                    "Duration (min)": task.duration,
                    "Priority": task.priority,
                    "Status": task.status,
                    "Repeat": task.frequency or "none",
                })
            st.table(table_rows)

            # Conflict warning
            if conflicts:
                conflict_names = ", ".join(t.title for t in conflicts)
                st.warning(f"⚠ Scheduling conflict detected: {conflict_names}")
            else:
                st.success(f"No conflicts for {pet.name}.")

            # Handle recurring tasks
            for task in sorted_tasks:
                if task.status == "completed" and task.frequency in ("daily", "weekly"):
                    # Queue next occurrence
                    delta = timedelta(days=1 if task.frequency == "daily" else 7)
                    next_task_time = task.time + delta
                    next_task = Task(
                        task.title,
                        next_task_time,
                        task.priority,
                        task.duration,
                        frequency=task.frequency
                    )
                    pet.add_task(next_task)
                    st.info(
                        f"Recurring task '{task.title}' queued for "
                        f"{next_task.time.strftime('%Y-%m-%d %H:%M')}."
                    )