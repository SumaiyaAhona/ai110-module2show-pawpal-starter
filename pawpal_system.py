from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    title: str
    time: str
    priority: str
    status: str = "pending"

    def update_status(self, new_status: str) -> None:
        pass


@dataclass
class Pet:
    name: str
    type: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, task: Task) -> None:
        pass


class Owner:
    def __init__(self, name: str):
        self.name: str = name
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        pass

    def remove_pet(self, pet: Pet) -> None:
        pass


class Scheduler:
    def __init__(self):
        self.all_tasks: List[Task] = []

    def organize_tasks(self) -> None:
        pass

    def sort_by_time(self) -> List[Task]:
        pass

    def detect_conflicts(self) -> List[Task]:
        pass
