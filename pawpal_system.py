from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List


@dataclass
class Task:
    title: str
    time: datetime          # use datetime, not str, for sorting and overlap math
    priority: str           # "high", "medium", "low"
    duration: int           # minutes — required for conflict detection
    status: str = "pending"
    frequency: str = None  # "daily", "weekly", or None

    def update_status(self, new_status: str) -> "Task | None":
        """Update the task's status; returns a new scheduled Task if recurring and completed."""
        valid = {"pending", "in-progress", "completed", "cancelled"}
        if new_status not in valid:
            raise ValueError(f"Invalid status '{new_status}'. Must be one of {valid}")
        self.status = new_status
        if new_status == "completed" and self.frequency in ("daily", "weekly"):
            delta = timedelta(days=1 if self.frequency == "daily" else 7)
            return Task(self.title, self.time + delta, self.priority, self.duration, frequency=self.frequency)
        return None

    def is_completed(self) -> bool:
        """Return True if the task's status is completed."""
        return self.status == "completed"

    def end_time(self) -> datetime:
        """Return the datetime when the task finishes."""
        return self.time + timedelta(minutes=self.duration)

    def __str__(self) -> str:
        """Return a formatted string summary of the task."""
        return (
            f"[{self.priority.upper()}] {self.title} "
            f"@ {self.time.strftime('%H:%M')} for {self.duration}min — {self.status}"
        )


@dataclass
class Pet:
    name: str               # fixed typo: was "setr"
    type: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from this pet's task list, raising ValueError if not found."""
        if task not in self.tasks:
            raise ValueError(f"Task '{task.title}' not found for pet '{self.name}'")
        self.tasks.remove(task)

    def get_pending_tasks(self) -> List[Task]:
        """Return all tasks that are not yet completed."""
        return [t for t in self.tasks if not t.is_completed()]

    def __hash__(self):
        """Return a hash based on the pet's name and type."""
        return hash((self.name, self.type))

    def __str__(self) -> str:
        """Return a formatted string summary of the pet."""
        return f"{self.name} ({self.type}) — {len(self.tasks)} task(s)"


class Owner:
    def __init__(self, name: str, scheduler: "Scheduler"):
        self.name: str = name
        self.pets: List[Pet] = []
        self.scheduler: "Scheduler" = scheduler

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's list and register it with the scheduler."""
        if pet not in self.pets:
            self.pets.append(pet)
            self.scheduler.organize_tasks(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from this owner's list, raising ValueError if not found."""
        if pet not in self.pets:
            raise ValueError(f"Pet '{pet.name}' not found for owner '{self.name}'")
        self.pets.remove(pet)
        self.scheduler.pet_tasks.pop(pet, None)

    def schedule_task(self, pet: Pet, task: Task) -> None:
        """Add a task to a pet owned by this owner, raising ValueError if the pet doesn't belong."""
        if pet not in self.pets:
            raise ValueError(f"Pet '{pet.name}' does not belong to owner '{self.name}'")
        pet.add_task(task)  # scheduler.pet_tasks[pet] is the same list, no second append needed

    def __str__(self) -> str:
        """Return a formatted string summary of the owner."""
        return f"Owner: {self.name} — {len(self.pets)} pet(s)"


class Scheduler:
    def __init__(self):
        self.pet_tasks: dict[Pet, List[Task]] = {} #each Pet maps to its own task list

    def organize_tasks(self, pet: Pet) -> None:
        """Register a pet and sync its existing task list into the scheduler."""
        self.pet_tasks[pet] = pet.tasks

    def sort_by_time(self, pet: Pet = None) -> List[Task]:
        """Return tasks sorted by start time, optionally limited to a single pet."""
        if pet is not None:
            tasks = self.pet_tasks.get(pet, [])
        else:
            tasks = [task for tasks in self.pet_tasks.values() for task in tasks]
        return sorted(tasks, key=lambda t: t.time)

    def filter_tasks(self, pet: Pet = None, status: str = None) -> List[Task]:
        """Return tasks matching the given pet and/or status filter."""
        if pet is not None:
            tasks = self.pet_tasks.get(pet, [])
        else:
            tasks = [task for tasks in self.pet_tasks.values() for task in tasks]
        if status is not None:
            tasks = [t for t in tasks if t.status == status]
        return tasks

    def detect_conflicts(self, pet: Pet) -> List[Task]:
        """
        Return tasks that overlap for a given pet.
        A conflict occurs when a task starts before the previous one ends.
        """
        tasks = sorted(self.pet_tasks.get(pet, []), key=lambda t: t.time)
        conflicts = []
        for i in range(len(tasks) - 1):
            current = tasks[i]
            next_task = tasks[i + 1]
            if current.end_time() > next_task.time:
                if current not in conflicts:
                    conflicts.append(current)
                conflicts.append(next_task)
        return conflicts

    def get_conflict_pairs(self, pet: Pet) -> List[tuple]:
        """Return a list of (task_a, task_b) tuples where the two tasks overlap for a given pet."""
        if pet not in self.pet_tasks:
            return []
        tasks = sorted(self.pet_tasks[pet], key=lambda t: t.time)
        pairs = []
        for i in range(len(tasks) - 1):
            current = tasks[i]
            next_task = tasks[i + 1]
            if current.end_time() > next_task.time:
                pairs.append((current, next_task))
        return pairs

    def print_schedule(self, pet: Pet) -> None:
        """Print a pet's schedule sorted by time, flagging conflicts."""
        tasks = sorted(self.pet_tasks.get(pet, []), key=lambda t: t.time)
        conflicts = self.detect_conflicts(pet)
        print(f"\nSchedule for {pet.name}:")
        print("-" * 40)
        for task in tasks:
            flag = " *** CONFLICT ***" if task in conflicts else ""
            print(f"  {task}{flag}")
        print("-" * 40)
