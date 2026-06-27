from pawpal_system import Owner, Pet, Scheduler, Task

import streamlit as st


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan")

if "selected_pet_name" not in st.session_state:
    st.session_state.selected_pet_name = None

owner = st.session_state.owner

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file now connects the Streamlit UI to the backend classes so pets and tasks can be added and scheduled.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.
"""
    )

st.divider()

st.subheader("Owner and Pets")
owner_name = st.text_input("Owner name", value=owner.name)
if owner_name.strip():
    owner.name = owner_name.strip()

pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    if pet_name.strip():
        new_pet = Pet(name=pet_name.strip())
        owner.add_pet(new_pet)
        st.session_state.selected_pet_name = new_pet.name
        st.success(f"Added pet: {new_pet.name}")
    else:
        st.warning("Please enter a pet name.")

if owner.pets:
    pet_names = [pet.name for pet in owner.pets]
    if st.session_state.selected_pet_name not in pet_names:
        st.session_state.selected_pet_name = pet_names[0]

    selected_pet_name = st.selectbox(
        "Select pet",
        pet_names,
        index=pet_names.index(st.session_state.selected_pet_name),
    )
    st.session_state.selected_pet_name = selected_pet_name
    selected_pet = next(pet for pet in owner.pets if pet.name == selected_pet_name)
else:
    selected_pet = None
    st.info("No pets yet. Add one above.")

st.markdown("### Tasks")
st.caption("Add a few tasks for the selected pet.")

if selected_pet is not None:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        task_time = st.text_input("Time", value="08:00")
    with col3:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col4:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    if st.button("Add task"):
        if task_title.strip():
            task = Task(
                description=task_title.strip(),
                time=task_time.strip() or None,
                duration=int(duration),
                priority=priority,
            )
            selected_pet.add_task(task)
            st.success(f"Added task for {selected_pet.name}")
        else:
            st.warning("Please enter a task title.")

    if selected_pet.tasks:
        st.write(f"Current tasks for {selected_pet.name}:")
        task_rows = [
            {
                "description": task.description,
                "duration": task.duration,
                "priority": task.priority,
                "time": task.time or "-",
                "completed": task.completion_status,
            }
            for task in selected_pet.tasks
        ]
        st.table(task_rows)
    else:
        st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generate a simple ordered schedule from your current owner data.")

if st.button("Generate schedule"):
    scheduler = Scheduler(owner)
    scheduled_tasks = scheduler.sort_by_time()
    conflicts = scheduler.detect_conflicts()

    if scheduled_tasks:
        st.subheader("Today's Schedule")
        for task in scheduled_tasks:
            st.write(f"- {task.time or '-'} | {task.description} | Priority: {task.priority} | Duration: {task.duration} min | Completed: {task.completion_status}")
    else:
        st.info("No tasks available to schedule yet.")

    if conflicts:
        st.warning("Conflicts detected:")
        for first, second in conflicts:
            st.write(f"- {first.description} and {second.description} share the same time")
