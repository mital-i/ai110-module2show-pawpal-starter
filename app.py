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
        with st.expander(f"🐾 {pet.name} ({pet.species}, {pet.age} years)"):
            st.write(f"**Care Category:** {pet.get_care_category()}")
            if pet.special_needs:
                st.write(f"**Special Needs:** {', '.join(pet.special_needs)}")
                st.info("This pet requires special attention")
            
            if pet.tasks:
                st.write("**Tasks:**")
                # Use Scheduler to sort tasks by time
                scheduler = Scheduler(st.session_state.owner)
                sorted_tasks = scheduler.sort_by_time(pet.tasks)
                
                # Display tasks in a table
                task_data = []
                for task in sorted_tasks:
                    status_icon = "✅" if task.completion_status else "⏳"
                    mandatory_icon = "⚠️" if task.is_mandatory else ""
                    task_data.append({
                        "Status": status_icon,
                        "Task": task.title,
                        "Priority": task.priority.title(),
                        "Duration": f"{task.duration_minutes} min",
                        "Time": task.preferred_time_range or "Any",
                        "Category": task.category,
                        "Mandatory": mandatory_icon
                    })
                
                if task_data:
                    st.table(task_data)
            else:
                st.info("No tasks added yet.")
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

# Show all tasks sorted by time preference
if st.session_state.owner.pets and any(pet.tasks for pet in st.session_state.owner.pets):
    st.subheader("📋 All Tasks (Sorted by Time)")
    scheduler = Scheduler(st.session_state.owner)
    all_tasks = st.session_state.owner.get_all_tasks()
    sorted_tasks = scheduler.sort_by_time(all_tasks)
    
    # Filter to show only incomplete tasks
    incomplete_tasks = [task for task in sorted_tasks if not task.completion_status]
    
    if incomplete_tasks:
        task_overview = []
        for task in incomplete_tasks:
            pet_name = next((pet.name for pet in st.session_state.owner.pets if task in pet.tasks), "Unknown")
            task_overview.append({
                "Pet": pet_name,
                "Task": task.title,
                "Priority": task.priority.title(),
                "Time Slot": task.preferred_time_range or "Flexible",
                "Duration": f"{task.duration_minutes} min",
                "Category": task.category,
                "Mandatory": "Yes" if task.is_mandatory else "No"
            })
        
        st.table(task_overview)
        st.info(f"📊 Total incomplete tasks: {len(incomplete_tasks)} | Total time needed: {sum(task.duration_minutes for task in incomplete_tasks)} min")
    else:
        st.success("🎉 All tasks are completed!")

# Validation: Check total task time vs available time
total_task_time = sum(task.duration_minutes for pet in st.session_state.owner.pets for task in pet.tasks if not task.completion_status)
if total_task_time > st.session_state.owner.available_time_per_day:
    st.warning(f"⚠️ Total incomplete task time ({total_task_time} min) exceeds available time ({st.session_state.owner.available_time_per_day} min). Some tasks may not be scheduled.")

if st.button("Generate schedule"):
    if st.session_state.owner.pets:
        scheduler = Scheduler(st.session_state.owner)
        today = datetime.now().strftime("%Y-%m-%d")
        schedule, warnings = scheduler.generate_schedule(today)
        
        st.subheader("📅 Today's Schedule")
        
        if schedule:
            # Display schedule in a professional table format
            schedule_data = []
            for item in schedule:
                task = item["task"]
                pet_name = next((pet.name for pet in st.session_state.owner.pets if task in pet.tasks), "Unknown")
                schedule_data.append({
                    "Time": f"{item['start_time']}-{item['end_time']}",
                    "Pet": pet_name,
                    "Task": task.title,
                    "Category": task.category,
                    "Priority": task.priority.title(),
                    "Duration": f"{task.duration_minutes} min"
                })
            
            st.table(schedule_data)
            st.success(f"✅ Successfully scheduled {len(schedule)} tasks")
        else:
            st.info("📭 No tasks scheduled for today")
        
        # Display warnings prominently
        if warnings:
            st.subheader("⚠️ Schedule Warnings")
            for warning in warnings:
                st.warning(warning)
        
    else:
        st.warning("🐾 Add pets and tasks first.")
