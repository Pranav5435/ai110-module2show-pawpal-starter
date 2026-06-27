python main.pyfrom pawpal_system import Owner, Pet, Scheduler, Task


def build_demo() -> None:
    owner = Owner(name="Jordan")

    mochi = Pet(name="Mochi")
    luna = Pet(name="Luna")

    owner.add_pet(mochi)
    owner.add_pet(luna)

    tasks = [
        Task(description="Morning walk", time="08:00", duration=30, priority="high"),
        Task(description="Feed breakfast", time="07:30", duration=15, priority="medium"),
        Task(description="Evening playtime", time="19:00", duration=45, priority="high"),
    ]

    for task in tasks:
        mochi.add_task(task)

    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.sort_by_time()
    conflicts = scheduler.detect_conflicts()

    print("Today's Schedule")
    print("=" * 20)
    for task in sorted_tasks:
        print(f"- {task.time} | {task.description} | Priority: {task.priority} | Duration: {task.duration} min")

    print("\nConflicts:")
    if conflicts:
        for first, second in conflicts:
            print(f"- {first.description} vs {second.description}")
    else:
        print("- None")


if __name__ == "__main__":
    build_demo()
