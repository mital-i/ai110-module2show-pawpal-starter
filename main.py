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

    # Add tasks to dog
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

    # Add tasks to cat
    cat_task1 = Task(
        title='Insulin injection',
        duration_minutes=10,
        priority='high',
        category='medical',
        frequency='daily',
        preferred_time_range='morning',
        is_mandatory=True
    )
    cat_task2 = Task(
        title='Feeding',
        duration_minutes=15,
        priority='medium',
        category='feeding',
        frequency='daily',
        preferred_time_range='evening',
        is_mandatory=True
    )
    cat.add_task(cat_task1)
    cat.add_task(cat_task2)

    # Add pets to owner
    owner.add_pet(dog)
    owner.add_pet(cat)

    # Create scheduler
    scheduler = Scheduler(owner)

    # Generate today's schedule
    today = '2024-01-01'  # Example date
    schedule = scheduler.generate_schedule(today)

    # Print the schedule
    print("Today's Schedule:")
    print(scheduler.display_schedule(schedule))

if __name__ == "__main__":
    main()