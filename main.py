from pawpal_system import Owner, Pet, Scheduler, Task


def build_demo() -> None:
    owner = Owner(name="Jordan")

    mochi = Pet(name="Mochi")
    luna = Pet(name="Luna")

    owner.add_pet(mochi)
    owner.add_pet(luna)

    tasks = [
        Task(description="Evening playtime", time="19:00", duration=45, priority="high"),
        Task(description="Feed breakfast", time="07:30", duration=15, priority="medium"),
        Task(description="Morning walk", time="08:00", duration=30, priority="high"),
    ]

    for task in tasks:
        mochi.add_task(task)

    completed_task = Task(description="Vet visit", time="10:00", duration=20, priority="low")
    completed_task.mark_complete()
    mochi.add_task(completed_task)

    recurring_task = Task(description="Medicine", time="21:00", duration=10, priority="high", frequency="daily")
    mochi.add_task(recurring_task)
    recurring_task.mark_complete(pet=mochi)

    conflict_a = Task(description="Grooming", time="09:00", duration=None, priority="medium")
    conflict_b = Task(description="Pill time", time="09:00", duration=None, priority="high")
    mochi.add_task(conflict_a)
    mochi.add_task(conflict_b)

    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.sort_by_time()
    pending_tasks = scheduler.filter_tasks(tasks=sorted_tasks, completion_status=False)

    print("Today's Schedule")
    print("=" * 20)
    for task in sorted_tasks:
        status = "DONE" if task.completion_status else "PENDING"
        print(f"- {task.time or '-'} | {task.description} | Priority: {task.priority} | Duration: {task.duration} min | {status}")

    print("\nFiltered Pending Tasks:")
    for task in pending_tasks:
        print(f"- {task.description} ({task.time or '-'})")

    conflicts = scheduler.detect_conflicts()
    print("\nConflict Check:")
    if conflicts:
        print("Warning: overlapping tasks detected!")
        for first, second in conflicts:
            print(f"- {first.description} vs {second.description}")
    else:
        print("- None")


if __name__ == "__main__":
    build_demo()
