from datetime import datetime, timedelta
from pawpal_system import Task, Pet, Scheduler

def test_mark_complete():
    task = Task("Feed pet", datetime.now(), "medium", 30)
    task.update_status("completed")
    assert task.status == "completed"

def test_add_task_to_pet():
    pet = Pet("Milo", "dog")
    task = Task("Walk", datetime.now(), "low", 20)

    pet.add_task(task)

    assert len(pet.tasks) == 1


# --- Sorting ---

def test_sort_by_time_returns_tasks_in_order():
    scheduler = Scheduler()
    pet = Pet("Milo", "dog")
    scheduler.organize_tasks(pet)

    t1 = Task("Vet",  datetime(2024, 1, 1, 10, 0), "high", 30)
    t2 = Task("Walk", datetime(2024, 1, 1,  8, 0), "high", 20)
    pet.add_task(t1)
    pet.add_task(t2)

    result = scheduler.sort_by_time()
    assert result[0] == t2
    assert result[1] == t1

def test_sort_by_time_single_pet_excludes_others():
    scheduler = Scheduler()
    dog = Pet("Milo", "dog")
    cat = Pet("Luna", "cat")
    scheduler.organize_tasks(dog)
    scheduler.organize_tasks(cat)

    dog_task = Task("Walk", datetime(2024, 1, 1, 8, 0), "high", 20)
    cat_task = Task("Feed", datetime(2024, 1, 1, 9, 0), "low", 10)
    dog.add_task(dog_task)
    cat.add_task(cat_task)

    result = scheduler.sort_by_time(pet=dog)
    assert dog_task in result
    assert cat_task not in result


# --- Recurring tasks ---

def test_daily_recurring_task_returns_next_day():
    task = Task("Walk", datetime(2024, 1, 1, 8, 0), "high", 30, frequency="daily")
    next_task = task.update_status("completed")

    assert next_task is not None
    assert next_task.time == datetime(2024, 1, 2, 8, 0)

def test_weekly_recurring_task_returns_next_week():
    task = Task("Groom", datetime(2024, 1, 1, 10, 0), "medium", 45, frequency="weekly")
    next_task = task.update_status("completed")

    assert next_task is not None
    assert next_task.time == datetime(2024, 1, 8, 10, 0)

def test_non_recurring_task_returns_none():
    task = Task("Feed", datetime(2024, 1, 1, 8, 0), "high", 15)
    result = task.update_status("completed")

    assert result is None

def test_recurring_task_next_occurrence_is_pending():
    task = Task("Walk", datetime(2024, 1, 1, 8, 0), "high", 30, frequency="daily")
    next_task = task.update_status("completed")

    assert next_task.status == "pending"


# --- Conflict detection ---

def test_no_conflict_when_tasks_do_not_overlap():
    scheduler = Scheduler()
    pet = Pet("Milo", "dog")
    scheduler.organize_tasks(pet)

    pet.add_task(Task("Walk", datetime(2024, 1, 1, 8,  0), "high", 30))
    pet.add_task(Task("Feed", datetime(2024, 1, 1, 9,  0), "high", 15))

    assert scheduler.detect_conflicts(pet) == []

def test_conflict_detected_when_tasks_overlap():
    scheduler = Scheduler()
    pet = Pet("Milo", "dog")
    scheduler.organize_tasks(pet)

    t1 = Task("Walk", datetime(2024, 1, 1, 8,  0), "high", 60)
    t2 = Task("Feed", datetime(2024, 1, 1, 8, 30), "high", 15)
    pet.add_task(t1)
    pet.add_task(t2)

    conflicts = scheduler.detect_conflicts(pet)
    assert t1 in conflicts
    assert t2 in conflicts

def test_conflict_pairs_returns_correct_tuple():
    scheduler = Scheduler()
    pet = Pet("Milo", "dog")
    scheduler.organize_tasks(pet)

    t1 = Task("Walk", datetime(2024, 1, 1, 8,  0), "high", 60)
    t2 = Task("Feed", datetime(2024, 1, 1, 8, 30), "high", 15)
    pet.add_task(t1)
    pet.add_task(t2)

    pairs = scheduler.get_conflict_pairs(pet)
    assert len(pairs) == 1
    assert pairs[0] == (t1, t2)

def test_no_cross_pet_conflicts():
    scheduler = Scheduler()
    dog = Pet("Milo", "dog")
    cat = Pet("Luna", "cat")
    scheduler.organize_tasks(dog)
    scheduler.organize_tasks(cat)

    dog.add_task(Task("Walk", datetime(2024, 1, 1, 8, 0), "high", 60))
    cat.add_task(Task("Feed", datetime(2024, 1, 1, 8, 0), "high", 15))

    assert scheduler.detect_conflicts(dog) == []
    assert scheduler.detect_conflicts(cat) == []


# --- Pets with no tasks ---

def test_sort_by_time_empty_pet_returns_empty_list():
    scheduler = Scheduler()
    pet = Pet("Milo", "dog")
    scheduler.organize_tasks(pet)

    assert scheduler.sort_by_time(pet=pet) == []

def test_detect_conflicts_empty_pet_returns_empty_list():
    scheduler = Scheduler()
    pet = Pet("Milo", "dog")
    scheduler.organize_tasks(pet)

    assert scheduler.detect_conflicts(pet) == []

def test_get_conflict_pairs_unregistered_pet_returns_empty_list():
    scheduler = Scheduler()
    pet = Pet("Milo", "dog")  # not registered

    assert scheduler.get_conflict_pairs(pet) == []

def test_filter_tasks_empty_pet_returns_empty_list():
    scheduler = Scheduler()
    pet = Pet("Milo", "dog")
    scheduler.organize_tasks(pet)

    assert scheduler.filter_tasks(pet=pet) == []
