from pawpal_system import Owner, Pet, Task, Scheduler

def main():
    # Create owner
    owner = Owner(
        name='Jordan',
        available_time_per_day=180,  # 3 hours
        preferred_time_slots={'morning': '06:00-12:00', 'afternoon': '12:00-18:00', 'evening': '18:00-22:00'},
        preferences={}
    )

    # Create first pet (dog)
    dog = Pet(
        name='Buddy',
        species='dog',
        age=3,
        special_needs=[],
        tasks=[]
    )

    # Create second pet (cat)
    cat = Pet(
        name='Whiskers',
        species='cat',
        age=2,
        special_needs=['diabetic'],  # Special need for variety
        tasks=[]
    )

    # Add tasks to dog (out of order)
    dog_task1 = Task(
        title='Morning walk',
        duration_minutes=45,
        priority='high',
        category='exercise',
        frequency='daily',
        preferred_time_range='morning',
        is_mandatory=True
    )
    dog.add_task(dog_task1)

    dog_task2 = Task(
        title='Evening play',
        duration_minutes=30,
        priority='medium',
        category='enrichment',
        frequency='daily',
        preferred_time_range='evening',
        is_mandatory=False
    )
    dog.add_task(dog_task2)

    dog_task3 = Task(
        title='Breakfast',
        duration_minutes=10,
        priority='high',
        category='feeding',
        frequency='daily',
        preferred_time_range='morning',
        is_mandatory=True
    )
    dog.add_task(dog_task3)

    # Add tasks to cat (out of order)
    cat_task1 = Task(
        title='Insulin injection',
        duration_minutes=10,
        priority='high',
        category='medical',
        frequency='daily',
        preferred_time_range='morning',
        is_mandatory=True
    )
    cat.add_task(cat_task1)

    cat_task2 = Task(
        title='Feeding',
        duration_minutes=15,
        priority='medium',
        category='feeding',
        frequency='daily',
        preferred_time_range='evening',
        is_mandatory=True
    )
    cat.add_task(cat_task2)

    cat_task3 = Task(
        title='Afternoon grooming',
        duration_minutes=20,
        priority='low',
        category='grooming',
        frequency='weekly',
        preferred_time_range='afternoon',
        is_mandatory=False
    )
    cat.add_task(cat_task3)

    # Add pets to owner
    owner.add_pet(dog)
    owner.add_pet(cat)

    # Create scheduler
    scheduler = Scheduler(owner)

    today = '2024-01-01'  # Example date

    # Demonstrate sorting and filtering
    all_tasks = owner.get_all_tasks()
    print("All tasks (unsorted):")
    for task in all_tasks:
        print(f"- {task.title} ({task.preferred_time_range})")

    # Sort by time
    sorted_tasks = scheduler.sort_by_time(all_tasks)
    print("\nTasks sorted by time:")
    for task in sorted_tasks:
        print(f"- {task.title} ({task.preferred_time_range})")

    # Filter by pet
    buddy_tasks = scheduler.filter_tasks(all_tasks, pet_name="Buddy")
    print("\nTasks for Buddy:")
    for task in buddy_tasks:
        print(f"- {task.title}")

    # Mark one task complete and filter by status
    scheduler.complete_task(dog_task2, today)
    incomplete_tasks = scheduler.filter_tasks(all_tasks, status=False)
    print("\nIncomplete tasks:")
    for task in incomplete_tasks:
        print(f"- {task.title} (status: {task.completion_status})")

    # Show that a new task was created for the next occurrence
    all_tasks_after = owner.get_all_tasks()
    print(f"\nTotal tasks after completing: {len(all_tasks_after)} (was {len(all_tasks)})")
    print("All tasks after completion:")
    for task in all_tasks_after:
        due_str = task.due_date.strftime("%Y-%m-%d") if task.due_date else "N/A"
        print(f"- {task.title} (due: {due_str}, completed: {task.completion_status})")

    # Generate today's schedule
    schedule, warnings = scheduler.generate_schedule(today)

    # Print the schedule
    print("\nToday's Schedule:")
    print(scheduler.display_schedule(schedule, warnings))

if __name__ == "__main__":
    main()