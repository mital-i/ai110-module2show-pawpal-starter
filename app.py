import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler
from datetime import datetime

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

# Initialize session state
if 'owner' not in st.session_state:
    st.session_state.owner = Owner(
        name='Jordan',
        available_time_per_day=180,
        preferred_time_slots={'morning': '06:00-12:00', 'afternoon': '12:00-18:00', 'evening': '18:00-22:00'},
        preferences={}
    )

st.subheader("Owner Info")
st.write(f"Owner: {st.session_state.owner.name}")

st.subheader("Add a Pet")
with st.form("add_pet_form"):
    pet_name = st.text_input("Pet name")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    age = st.number_input("Age", min_value=0, max_value=30, value=1)
    special_needs = st.text_area("Special needs (comma separated)")
    submitted = st.form_submit_button("Add Pet")
    if submitted:
        special_needs_list = [need.strip() for need in special_needs.split(',') if need.strip()]
        new_pet = Pet(
            name=pet_name,
            species=species,
            age=age,
            special_needs=special_needs_list,
            tasks=[]
        )
        st.session_state.owner.add_pet(new_pet)
        st.success(f"Added pet {pet_name}")

st.subheader("Current Pets")
if st.session_state.owner.pets:
    for pet in st.session_state.owner.pets:
        st.write(f"- {pet.name} ({pet.species}, {pet.age} years)")
        if pet.tasks:
            st.write("  Tasks:")
            for task in pet.tasks:
                st.write(f"    - {task.title} ({task.priority}, {task.duration_minutes} min)")
else:
    st.info("No pets added yet.")

st.markdown("### Add Task to Pet")
if st.session_state.owner.pets:
    pet_options = [pet.name for pet in st.session_state.owner.pets]
    selected_pet = st.selectbox("Select Pet", pet_options)
    with st.form("add_task_form"):
        task_title = st.text_input("Task title")
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        priority = st.selectbox("Priority", ["low", "medium", "high"])
        category = st.text_input("Category", value="exercise")
        frequency = st.selectbox("Frequency", ["daily", "weekly"])
        preferred_time = st.selectbox("Preferred time", ["morning", "afternoon", "evening", None])
        mandatory = st.checkbox("Mandatory")
        submitted_task = st.form_submit_button("Add Task")
        if submitted_task:
            task = Task(
                title=task_title,
                duration_minutes=duration,
                priority=priority,
                category=category,
                frequency=frequency,
                preferred_time_range=preferred_time,
                is_mandatory=mandatory
            )
            pet = next(p for p in st.session_state.owner.pets if p.name == selected_pet)
            pet.add_task(task)
            st.success(f"Added task {task_title} to {selected_pet}")
else:
    st.info("Add a pet first to add tasks.")

st.subheader("Build Schedule")
st.caption("This button calls your scheduling logic.")

# Validation: Check total task time vs available time
total_task_time = sum(task.duration_minutes for pet in st.session_state.owner.pets for task in pet.tasks)
if total_task_time > st.session_state.owner.available_time_per_day:
    st.warning(f"Total task time ({total_task_time} min) exceeds available time ({st.session_state.owner.available_time_per_day} min). Some tasks may not be scheduled.")

if st.button("Generate schedule"):
    if st.session_state.owner.pets:
        scheduler = Scheduler(st.session_state.owner)
        today = datetime.now().strftime("%Y-%m-%d")
        schedule = scheduler.generate_schedule(today)
        st.subheader("Today's Schedule")
        st.code(scheduler.display_schedule(schedule))
    else:
        st.warning("Add pets and tasks first.")
