from datetime import datetime
from pawpal_system import Task, Pet, Owner, Scheduler


def print_todays_schedule(owner: Owner, scheduler: Scheduler) -> None:
    col = {"time": 8, "task": 17, "duration": 9, "status": 11}
    width = 45

    print(f"\n{'=' * width}")
    print(f"  PawPal+ Schedule — {owner.name}")
    print(f"{'=' * width}")

    for pet in owner.pets:
        tasks = sorted(scheduler.pet_tasks.get(pet, []), key=lambda t: t.time)
        conflicts = scheduler.detect_conflicts(pet)

        print(f"\n  {pet.name} ({pet.type})")
        print(f"  {'TIME':<{col['time']}} {'TASK':<{col['task']}} {'DURATION':<{col['duration']}} {'STATUS':<{col['status']}}")
        print(f"  {'-' * col['time']} {'-' * col['task']} {'-' * col['duration']} {'-' * col['status']}")

        if not tasks:
            print("    No tasks scheduled.")
        else:
            for task in tasks:
                time_str   = task.time.strftime("%H:%M")
                duration   = f"{task.duration} min"
                conflict   = "  !!" if task in conflicts else ""
                print(f"  {time_str:<{col['time']}} {task.title:<{col['task']}} {duration:<{col['duration']}} {task.status:<{col['status']}}{conflict}")

        if conflicts:
            print(f"           ! {len(conflicts)} conflict(s) detected")

    print(f"\n{'=' * width}\n")


def main():
    # --- Setup ---
    scheduler = Scheduler()
    owner = Owner("Jordan", scheduler)

    # --- Create pets ---
    max_dog = Pet("Max", "dog")
    mochi_cat = Pet("Mochi", "cat")

    owner.add_pet(max_dog)
    owner.add_pet(mochi_cat)

    # --- Tasks for Max ---
    owner.schedule_task(max_dog, Task(
        title="Morning Walk",
        time=datetime(2024, 1, 1, 8, 0),
        priority="high",
        duration=30
    ))
    owner.schedule_task(max_dog, Task(
        title="Breakfast",
        time=datetime(2024, 1, 1, 8, 20),  # overlaps Morning Walk — triggers conflict
        priority="high",
        duration=15
    ))
    owner.schedule_task(max_dog, Task(
        title="Vet Checkup",
        time=datetime(2024, 1, 1, 11, 0),
        priority="medium",
        duration=45
    ))

    # --- Tasks for Mochi ---
    owner.schedule_task(mochi_cat, Task(
        title="Feeding",
        time=datetime(2024, 1, 1, 8, 0),
        priority="high",
        duration=10
    ))
    owner.schedule_task(mochi_cat, Task(
        title="Playtime",
        time=datetime(2024, 1, 1, 14, 0),
        priority="low",
        duration=20
    ))

    # --- Print schedule ---
    print_todays_schedule(owner, scheduler)

    # --- Mark a task complete and reprint ---
    max_dog.tasks[2].update_status("completed")
    print("  (Vet Checkup marked as completed)\n")
    print_todays_schedule(owner, scheduler)


if __name__ == "__main__":
    main()
