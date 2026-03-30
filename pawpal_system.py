from dataclasses import dataclass
from typing import List, Dict, Optional, Any


class Owner:
    def __init__(self, name: str, available_time_per_day: int, preferred_time_slots: Dict[str, str], preferences: Dict[str, Any]):
        self.name = name
        self.available_time_per_day = available_time_per_day
        self.preferred_time_slots = preferred_time_slots
        self.preferences = preferences

    def update_preferences(self, new_prefs: Dict[str, Any]) -> None:
        pass

    def get_available_slots(self) -> List[str]:
        pass

    def is_available_at(self, time_slot: str) -> bool:
        pass


@dataclass
class Pet:
    name: str
    species: str
    age: int
    special_needs: List[str]

    def get_care_category(self) -> str:
        pass

    def requires_special_attention(self) -> bool:
        pass


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str
    category: str
    frequency: str
    preferred_time_range: Optional[str]
    is_mandatory: bool

    def get_priority_score(self) -> int:
        pass

    def is_due_today(self, date: str) -> bool:
        pass

    def can_fit_in_slot(self, time_slot: str, owner_available: bool) -> bool:
        pass


class Schedule:
    def __init__(self, date: str, scheduled_tasks: List[Dict], total_scheduled_time: int, unscheduled_tasks: List[Task]):
        self.date = date
        self.scheduled_tasks = scheduled_tasks
        self.total_scheduled_time = total_scheduled_time
        self.unscheduled_tasks = unscheduled_tasks

    def add_task(self, task: Task, start_time: str, reason: str) -> None:
        pass

    def get_total_time(self) -> int:
        pass

    def display(self) -> str:
        pass

    def get_explanation(self) -> str:
        pass


class Scheduler:
    def __init__(self, owner: Owner, pet: Pet, tasks: List[Task], total_available_time: int):
        self.owner = owner
        self.pet = pet
        self.tasks = tasks
        self.total_available_time = total_available_time

    def filter_eligible_tasks(self, date: str) -> List[Task]:
        pass

    def prioritize_tasks(self, tasks: List[Task]) -> List[Task]:
        pass

    def generate_schedule(self, date: str) -> Schedule:
        pass

    def resolve_conflicts(self, tasks: List[Task]) -> List[Task]:
        pass

    def explain_choice(self, task: Task, time_slot: str) -> str:
        pass
