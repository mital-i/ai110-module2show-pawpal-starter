import pytest
from pawpal_system import Task, Pet


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
