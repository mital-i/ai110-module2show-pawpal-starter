import pytest
from datetime import datetime
from pawpal_system import Task, Pet, Owner, Scheduler


def test_task_completion():
    """Verify that calling mark_complete() changes the task's status."""
    task = Task(
        title="Test Task",
        duration_minutes=30,
        priority="medium",
        category="test",
        frequency="daily",
        preferred_time_range=None,
        is_mandatory=False,
        completion_status=False
    )
    
    # Initially not completed
    assert task.completion_status == False
    
    # Mark as complete
    task.mark_complete()
    
    # Now should be completed
    assert task.completion_status == True


def test_task_addition():
    """Verify that adding a task to a Pet increases that pet's task count."""
    pet = Pet(
        name="TestPet",
        species="dog",
        age=2,
        special_needs=[],
        tasks=[]
    )
    
    # Initially no tasks
    assert len(pet.tasks) == 0
    
    # Create and add a task
    task = Task(
        title="Test Task",
        duration_minutes=15,
        priority="low",
        category="test",
        frequency="daily",
        preferred_time_range=None,
        is_mandatory=False
    )
    pet.add_task(task)
    
    # Now should have one task
    assert len(pet.tasks) == 1
    assert pet.tasks[0] == task


def test_sorting_correctness():
    """Verify tasks are returned in chronological order by preferred time range."""
    # Create owner and scheduler
    owner = Owner(
        name="Test Owner",
        available_time_per_day=120,
        preferred_time_slots={"morning": "06:00-12:00", "afternoon": "12:00-18:00", "evening": "18:00-22:00"},
        preferences={}
    )
    scheduler = Scheduler(owner)
    
    # Create tasks with different time preferences (out of order)
    evening_task = Task(
        title="Evening Walk",
        duration_minutes=30,
        priority="medium",
        category="exercise",
        frequency="daily",
        preferred_time_range="evening",
        is_mandatory=False
    )
    morning_task = Task(
        title="Morning Feed",
        duration_minutes=15,
        priority="high",
        category="feeding",
        frequency="daily",
        preferred_time_range="morning",
        is_mandatory=True
    )
    afternoon_task = Task(
        title="Afternoon Play",
        duration_minutes=20,
        priority="low",
        category="enrichment",
        frequency="daily",
        preferred_time_range="afternoon",
        is_mandatory=False
    )
    
    tasks = [evening_task, morning_task, afternoon_task]
    
    # Sort by time
    sorted_tasks = scheduler.sort_by_time(tasks)
    
    # Verify chronological order: morning (06:00), afternoon (12:00), evening (18:00)
    assert len(sorted_tasks) == 3
    assert sorted_tasks[0].preferred_time_range == "morning"
    assert sorted_tasks[1].preferred_time_range == "afternoon"
    assert sorted_tasks[2].preferred_time_range == "evening"


def test_recurrence_logic():
    """Confirm that marking a daily task complete creates a new task for the following day."""
    # Create owner with a pet
    owner = Owner(
        name="Test Owner",
        available_time_per_day=120,
        preferred_time_slots={"morning": "06:00-12:00"},
        preferences={}
    )
    pet = Pet(
        name="TestPet",
        species="dog",
        age=2,
        special_needs=[],
        tasks=[]
    )
    owner.add_pet(pet)
    
    # Create a daily task
    task = Task(
        title="Daily Walk",
        duration_minutes=30,
        priority="high",
        category="exercise",
        frequency="daily",
        preferred_time_range="morning",
        is_mandatory=True
    )
    pet.add_task(task)
    
    # Initially one task
    initial_task_count = len(owner.get_all_tasks())
    assert initial_task_count == 1
    
    # Create scheduler and complete the task
    scheduler = Scheduler(owner)
    today = "2024-01-01"
    scheduler.complete_task(task, today)
    
    # Verify task is marked complete
    assert task.completion_status == True
    
    # Verify new task was created
    all_tasks_after = owner.get_all_tasks()
    assert len(all_tasks_after) == 2
    
    # Find the new task
    new_task = None
    for t in all_tasks_after:
        if t != task:
            new_task = t
            break
    
    assert new_task is not None
    assert new_task.title == task.title
    assert new_task.frequency == "daily"
    assert new_task.due_date == datetime.strptime("2024-01-02", "%Y-%m-%d")  # Next day
    assert new_task.completion_status == False  # New task is incomplete


def test_conflict_detection():
    """Verify that the Scheduler flags duplicate times."""
    # Create owner with a pet
    owner = Owner(
        name="Test Owner",
        available_time_per_day=120,
        preferred_time_slots={"morning": "06:00-12:00", "afternoon": "12:00-18:00"},
        preferences={}
    )
    pet = Pet(
        name="TestPet",
        species="dog",
        age=2,
        special_needs=[],
        tasks=[]
    )
    owner.add_pet(pet)
    
    # Create two tasks with same preferred time range (morning)
    task1 = Task(
        title="Morning Walk",
        duration_minutes=30,
        priority="high",
        category="exercise",
        frequency="daily",
        preferred_time_range="morning",
        is_mandatory=True
    )
    task2 = Task(
        title="Morning Feed",
        duration_minutes=20,
        priority="high",
        category="feeding",
        frequency="daily",
        preferred_time_range="morning",
        is_mandatory=True
    )
    pet.add_task(task1)
    pet.add_task(task2)
    
    # Create scheduler and generate schedule
    scheduler = Scheduler(owner)
    today = "2024-01-01"
    schedule, warnings = scheduler.generate_schedule(today)
    
    # Verify both tasks are scheduled (they fit in the slot)
    assert len(schedule) == 2
    
    # Verify conflicts are detected (both start at same time in morning slot)
    assert len(warnings) > 0
    conflict_found = any("overlap" in w.lower() or "conflict" in w.lower() for w in warnings)
    assert conflict_found, f"No conflict detected in warnings: {warnings}"
