from datetime import datetime
from pawpal_system import Task, Pet

def test_mark_complete():
    task = Task("Feed pet", datetime.now(), "medium", 30)
    task.update_status("completed")
    assert task.status == "completed"

def test_add_task_to_pet():
    pet = Pet("Milo", "dog")
    task = Task("Walk", datetime.now(), "low", 20)

    pet.add_task(task)

    assert len(pet.tasks) == 1
