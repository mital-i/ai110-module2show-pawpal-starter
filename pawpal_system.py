from dataclasses import dataclass
from typing import List, Dict, Optional, Any, Tuple
from datetime import datetime, timedelta
from functools import lru_cache


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
    due_date: Optional[datetime] = None

    def get_priority_score(self) -> int:
        """Return numeric priority score for sorting."""
        priority_map = {"high": 3, "medium": 2, "low": 1}
        return priority_map.get(self.priority, 1)

    def is_due_today(self, date: str) -> bool:
        """Check if task is due on given date based on frequency or due_date."""
        if self.due_date:
            return self.due_date.strftime("%Y-%m-%d") == date
        # Fallback to old logic for tasks without due_date
        if self.frequency == "daily":
            return True
        elif self.frequency == "weekly":
            # Assume weekly tasks are due on Mondays (weekday 0); can be made configurable
            task_date = datetime.strptime(date, "%Y-%m-%d")
            return task_date.weekday() == 0
        # For other frequencies, return False for now (extend as needed)
        return False

    def mark_complete(self) -> None:
        self.completion_status = True

    def can_fit_in_slot(self, time_slot: str, owner_available: bool) -> bool:
        """Check if task fits in time slot considering availability and parsing ranges."""
        if not owner_available:
            return False
        if self.preferred_time_range is None:
            return True
        # Parse time_slot if it's a range like "06:00-12:00"
        if '-' in time_slot:
            start_str, end_str = time_slot.split('-')
            try:
                slot_start = datetime.strptime(start_str.strip(), "%H:%M").time()
                slot_end = datetime.strptime(end_str.strip(), "%H:%M").time()
                # For simplicity, check if preferred_time_range matches the slot name
                # Could extend to check if task duration fits within the range
                return self.preferred_time_range in ['morning', 'afternoon', 'evening'] and time_slot in ['06:00-12:00', '12:00-18:00', '18:00-22:00']
            except ValueError:
                return False
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
        self._cached_tasks: Optional[List[Task]] = None
        self._cache_dirty = True

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
        self._cache_dirty = True

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks from all pets, with caching."""
        if self._cache_dirty or self._cached_tasks is None:
            self._cached_tasks = []
            for pet in self.pets:
                self._cached_tasks.extend(pet.tasks)
            self._cache_dirty = False
        return self._cached_tasks

    def get_tasks_by_pet(self, pet_name: Optional[str] = None, status: Optional[bool] = None) -> List[Task]:
        """Filter tasks by pet name and/or completion status."""
        tasks = self.get_all_tasks()
        if pet_name:
            tasks = [t for t in tasks if any(p.name == pet_name for p in self.pets if t in p.tasks)]
        if status is not None:
            tasks = [t for t in tasks if t.completion_status == status]
        return tasks


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def filter_eligible_tasks(self, date: str, pet_name: Optional[str] = None) -> List[Task]:
        """Filter tasks that are due and not completed, optionally by pet."""
        tasks = self.owner.get_tasks_by_pet(pet_name, status=False)  # Only incomplete
        return [t for t in tasks if t.is_due_today(date)]

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by their preferred time range, converting to HH:MM format.
        
        Maps 'morning' to '06:00', 'afternoon' to '12:00', 'evening' to '18:00',
        and sorts chronologically using datetime parsing for accurate ordering.
        
        Args:
            tasks: List of Task objects to sort.
            
        Returns:
            Sorted list of tasks by preferred time.
        """
        def time_key(task: Task) -> str:
            if task.preferred_time_range == "morning":
                return "06:00"
            elif task.preferred_time_range == "afternoon":
                return "12:00"
            elif task.preferred_time_range == "evening":
                return "18:00"
            else:
                return "00:00"  # Default for None or unknown
        
        return sorted(tasks, key=lambda t: datetime.strptime(time_key(t), "%H:%M"))

    def filter_tasks(self, tasks: List[Task], pet_name: Optional[str] = None, status: Optional[bool] = None) -> List[Task]:
        """Filter tasks by pet name and/or completion status.
        
        Args:
            tasks: List of Task objects to filter.
            pet_name: Optional name of the pet to filter tasks for.
            status: Optional completion status (True for completed, False for incomplete).
            
        Returns:
            Filtered list of tasks matching the criteria.
        """
        filtered = tasks
        if pet_name:
            filtered = [t for t in filtered if any(p.name == pet_name for p in self.owner.pets if t in p.tasks)]
        if status is not None:
            filtered = [t for t in filtered if t.completion_status == status]
        return filtered

    def complete_task(self, task: Task, date: str) -> None:
        """Mark task complete and create new instance for next occurrence if recurring.
        
        For daily tasks, creates a new task due the next day.
        For weekly tasks, creates a new task due in 7 days.
        Uses timedelta for accurate date calculation.
        
        Args:
            task: The Task object to mark complete.
            date: The current date string in 'YYYY-MM-DD' format.
        """
        task.mark_complete()
        if task.frequency in ["daily", "weekly"]:
            days_to_add = 1 if task.frequency == "daily" else 7
            new_due = datetime.strptime(date, "%Y-%m-%d") + timedelta(days=days_to_add)
            new_task = Task(
                title=task.title,
                duration_minutes=task.duration_minutes,
                priority=task.priority,
                category=task.category,
                frequency=task.frequency,
                preferred_time_range=task.preferred_time_range,
                is_mandatory=task.is_mandatory,
                due_date=new_due
            )
            # Find the pet and add the new task
            for pet in self.owner.pets:
                if task in pet.tasks:
                    pet.add_task(new_task)
                    self.owner._cache_dirty = True  # Invalidate cache
                    break

    def prioritize_tasks(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by time fit, priority score, and duration."""
        def time_fit_score(task: Task) -> int:
            available_slots = self.owner.get_available_slots()
            return 10 if any(task.can_fit_in_slot(slot, True) for slot in available_slots) else 0
        
        def pet_priority_bonus(task: Task) -> int:
            # Find the pet for this task
            for pet in self.owner.pets:
                if task in pet.tasks:
                    # Bonus for senior pets or special needs
                    bonus = 0
                    if pet.age >= 7 and pet.species == "dog" or pet.age >= 10 and pet.species == "cat":
                        bonus += 2
                    if pet.requires_special_attention():
                        bonus += 1
                    return bonus
            return 0
        
        return sorted(tasks, key=lambda t: (-time_fit_score(t), -t.get_priority_score() - pet_priority_bonus(t), t.duration_minutes))

    def generate_schedule(self, date: str) -> Tuple[List[Dict], List[str]]:
        """Generate daily schedule with time assignments and conflict detection.
        
        Uses slot-based scheduling (morning/afternoon/evening) where tasks in the same
        preferred slot start simultaneously. Detects and returns warnings for conflicts.
        
        Args:
            date: The date string in 'YYYY-MM-DD' format for which to generate the schedule.
            
        Returns:
            Tuple of (scheduled tasks list, warnings list).
        """
        eligible_tasks = self.filter_eligible_tasks(date)
        prioritized_tasks = self.prioritize_tasks(eligible_tasks)
        
        scheduled = []
        total_time_used = 0
        warnings = []
        
        # Define time slots
        slot_times = {
            'morning': ('06:00', '12:00'),
            'afternoon': ('12:00', '18:00'),
            'evening': ('18:00', '22:00')
        }
        
        # Group tasks by preferred_time_range
        task_groups = {}
        for task in prioritized_tasks:
            pref = task.preferred_time_range or 'morning'  # default to morning
            if pref not in task_groups:
                task_groups[pref] = []
            task_groups[pref].append(task)
        
        # Schedule tasks in each slot
        for slot_name, tasks_in_slot in task_groups.items():
            if slot_name in slot_times:
                slot_start_str, slot_end_str = slot_times[slot_name]
                slot_start = datetime.strptime(slot_start_str, '%H:%M')
                slot_end = datetime.strptime(slot_end_str, '%H:%M')
                
                # For testing conflicts, schedule all tasks in the slot starting at the same time
                for task in tasks_in_slot:
                    start_dt = slot_start
                    end_dt = start_dt + timedelta(minutes=task.duration_minutes)
                    
                    if end_dt <= slot_end and total_time_used + task.duration_minutes <= self.owner.available_time_per_day:
                        start_time_str = start_dt.strftime("%H:%M")
                        end_time_str = end_dt.strftime("%H:%M")
                        
                        reason = f"Scheduled {task.title} at {start_time_str} due to {task.priority} priority"
                        if task.is_mandatory:
                            reason += " (mandatory)"
                        
                        scheduled.append({
                            "task": task,
                            "start_time": start_time_str,
                            "end_time": end_time_str,
                            "reason": reason
                        })
                        
                        total_time_used += task.duration_minutes
                    else:
                        warnings.append(f"Task {task.title} does not fit in {slot_name} slot or exceeds time limit.")
        
        # Detect conflicts
        warnings.extend(self.detect_conflicts(scheduled))
        
        return scheduled, warnings

    def detect_conflicts(self, schedule: List[Dict]) -> List[str]:
        """Detect scheduling conflicts in the generated schedule.
        
        Checks for time overlaps within the same pet's tasks and across different pets.
        Returns warning messages for any detected conflicts without crashing the program.
        
        Args:
            schedule: List of scheduled task dictionaries with 'task', 'start_time', 'end_time'.
            
        Returns:
            List of warning strings describing detected conflicts.
        """
        warnings = []
        pet_tasks = {}
        for item in schedule:
            task = item['task']
            start = datetime.strptime(item['start_time'], '%H:%M')
            end = datetime.strptime(item['end_time'], '%H:%M')
            for pet in self.owner.pets:
                if task in pet.tasks:
                    if pet.name not in pet_tasks:
                        pet_tasks[pet.name] = []
                    pet_tasks[pet.name].append((start, end, task.title))
                    break
        
        # Check for overlaps within the same pet
        for pet_name, intervals in pet_tasks.items():
            intervals.sort(key=lambda x: x[0])  # sort by start time
            for i in range(len(intervals) - 1):
                start1, end1, title1 = intervals[i]
                start2, end2, title2 = intervals[i + 1]
                if start1 < end2 and end1 > start2:
                    warnings.append(f"Conflict for pet {pet_name}: {title1} overlaps with {title2} at {start1.strftime('%H:%M')}-{end1.strftime('%H:%M')} and {start2.strftime('%H:%M')}-{end2.strftime('%H:%M')}")
        
        # Check for overlaps between different pets (global overlaps)
        all_intervals = []
        for pet_name, intervals in pet_tasks.items():
            for start, end, title in intervals:
                all_intervals.append((start, end, title, pet_name))
        all_intervals.sort(key=lambda x: x[0])
        for i in range(len(all_intervals) - 1):
            start1, end1, title1, pet1 = all_intervals[i]
            start2, end2, title2, pet2 = all_intervals[i + 1]
            if pet1 != pet2 and start1 < end2 and end1 > start2:
                warnings.append(f"Global conflict: {title1} ({pet1}) overlaps with {title2} ({pet2}) at {start1.strftime('%H:%M')}-{end1.strftime('%H:%M')} and {start2.strftime('%H:%M')}-{end2.strftime('%H:%M')}")
        
        return warnings

    def explain_choice(self, task: Task, time_slot: str) -> str:
        """Explain why a task was scheduled at a specific time."""
        return f"Task '{task.title}' was scheduled at {time_slot} because it has {task.priority} priority and fits within available time."

    def display_schedule(self, schedule: List[Dict], warnings: List[str] = None) -> str:
        """Format schedule for display.
        
        Args:
            schedule: List of scheduled task dictionaries.
            warnings: Optional list of warning messages to include.
            
        Returns:
            Formatted string representation of the schedule and warnings.
        """
        if not schedule:
            output = "No tasks scheduled for today."
        else:
            output = "Daily Schedule:\n"
            for item in schedule:
                task = item["task"]
                output += f"- {item['start_time']}-{item['end_time']}: {task.title} ({task.category})\n"
                output += f"  Reason: {item['reason']}\n"
        
        if warnings:
            output += "\nWarnings:\n"
            for w in warnings:
                output += f"- {w}\n"
        
        return output
