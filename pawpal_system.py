from dataclasses import dataclass
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta


@dataclass
class Task:
    title: str  # description
    duration_minutes: int
    priority: str
    category: str
    frequency: str
    preferred_time_range: Optional[str]
    is_mandatory: bool
    completion_status: bool = False  # False = not completed

    def get_priority_score(self) -> int:
        """Return numeric priority score for sorting."""
        priority_map = {"high": 3, "medium": 2, "low": 1}
        return priority_map.get(self.priority, 1)

    def is_due_today(self, date: str) -> bool:
        """Check if task is due on given date."""
        # Simple implementation: daily tasks are always due
        # For weekly, could check day of week, but for now assume daily
        if self.frequency == "daily":
            return True
        # For other frequencies, would need more logic, but stub for now
        return True

    def mark_complete(self) -> None:
        self.completion_status = True

    def can_fit_in_slot(self, time_slot: str, owner_available: bool) -> bool:
        """Check if task fits in time slot considering availability."""
        if not owner_available:
            return False
        if self.preferred_time_range is None:
            return True
        # Simple check: if time_slot contains preferred_time_range
        return self.preferred_time_range in time_slot


@dataclass
class Pet:
    name: str
    species: str
    age: int
    special_needs: List[str]
    tasks: List[Task]

    def get_care_category(self) -> str:
        """Return care category based on species and age."""
        if self.species == "dog":
            if self.age < 1:
                return "puppy"
            elif self.age < 7:
                return "adult_dog"
            else:
                return "senior_dog"
        elif self.species == "cat":
            if self.age < 1:
                return "kitten"
            elif self.age < 10:
                return "adult_cat"
            else:
                return "senior_cat"
        else:
            return "other"

    def requires_special_attention(self) -> bool:
        """Check if pet has special needs requiring attention."""
        return len(self.special_needs) > 0

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def get_tasks(self) -> List[Task]:
        """Return list of tasks for this pet."""
        return self.tasks


class Owner:
    def __init__(self, name: str, available_time_per_day: int, preferred_time_slots: Dict[str, str], preferences: Dict[str, Any]):
        self.name = name
        self.available_time_per_day = available_time_per_day
        self.preferred_time_slots = preferred_time_slots
        self.preferences = preferences
        self.pets: List[Pet] = []

    def update_preferences(self, new_prefs: Dict[str, Any]) -> None:
        """Update owner preferences with new values."""
        self.preferences.update(new_prefs)

    def get_available_slots(self) -> List[str]:
        """Return list of available time slots."""
        # Return list of preferred time slots
        return list(self.preferred_time_slots.values())

    def is_available_at(self, time_slot: str) -> bool:
        """Check if owner is available at given time slot."""
        # Check if time_slot is in preferred slots
        return time_slot in self.preferred_time_slots.values()

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to owner's pet list."""
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks from all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def filter_eligible_tasks(self, date: str) -> List[Task]:
        """Filter tasks that are due and not completed."""
        all_tasks = self.owner.get_all_tasks()
        eligible = []
        for task in all_tasks:
            if task.is_due_today(date) and not task.completion_status:
                eligible.append(task)
        return eligible

    def prioritize_tasks(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by priority score and duration."""
        # Sort by priority score descending, then by duration ascending
        return sorted(tasks, key=lambda t: (-t.get_priority_score(), t.duration_minutes))

    def generate_schedule(self, date: str) -> List[Dict]:
        """Generate daily schedule with time assignments."""
        eligible_tasks = self.filter_eligible_tasks(date)
        prioritized_tasks = self.prioritize_tasks(eligible_tasks)
        
        scheduled = []
        current_time = datetime.strptime("06:00", "%H:%M")  # Start at 6 AM
        total_time_used = 0
        
        for task in prioritized_tasks:
            if total_time_used + task.duration_minutes <= self.owner.available_time_per_day:
                start_time_str = current_time.strftime("%H:%M")
                end_time = current_time + timedelta(minutes=task.duration_minutes)
                end_time_str = end_time.strftime("%H:%M")
                
                reason = f"Scheduled {task.title} at {start_time_str} due to {task.priority} priority"
                if task.is_mandatory:
                    reason += " (mandatory)"
                
                scheduled.append({
                    "task": task,
                    "start_time": start_time_str,
                    "end_time": end_time_str,
                    "reason": reason
                })
                
                current_time = end_time
                total_time_used += task.duration_minutes
            else:
                # Couldn't fit, mark as unscheduled
                break
        
        return scheduled

    def resolve_conflicts(self, tasks: List[Task]) -> List[Task]:
        """Resolve scheduling conflicts by prioritizing tasks."""
        # For now, just return prioritized tasks, drop if over time
        # In generate_schedule, we already handle time limits
        return self.prioritize_tasks(tasks)

    def explain_choice(self, task: Task, time_slot: str) -> str:
        """Explain why a task was scheduled at a specific time."""
        return f"Task '{task.title}' was scheduled at {time_slot} because it has {task.priority} priority and fits within available time."

    def display_schedule(self, schedule: List[Dict]) -> str:
        """Format schedule for display."""
        if not schedule:
            return "No tasks scheduled for today."
        
        output = "Daily Schedule:\n"
        for item in schedule:
            task = item["task"]
            output += f"- {item['start_time']}-{item['end_time']}: {task.title} ({task.category})\n"
            output += f"  Reason: {item['reason']}\n"
        return output
