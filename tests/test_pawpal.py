import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pawpal_system import Owner, Pet, Scheduler, Task


def test_mark_complete_sets_completion_status_true():
    task = Task(description="Walk the dog")

    task.mark_complete()

    assert task.completion_status is True


def test_add_task_increases_pet_task_count_by_one():
    pet = Pet(name="Mochi")
    initial_count = len(pet.tasks)

    task = Task(description="Feed breakfast")
    pet.add_task(task)

    assert len(pet.tasks) == initial_count + 1


def test_mark_complete_creates_next_occurrence_for_recurring_task():
    pet = Pet(name="Mochi")
    task = Task(description="Medicine", time="21:00", frequency="daily", duration=10)
    pet.add_task(task)

    task.mark_complete(pet=pet)

    assert task.completion_status is True
    assert len(pet.tasks) == 2
    assert pet.tasks[-1].completion_status is False
    assert pet.tasks[-1].description == "Medicine"


def test_sort_by_time_orders_tasks_by_time():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi")
    owner.add_pet(pet)

    later_task = Task(description="Evening walk", time="19:00", duration=30, priority="high")
    earlier_task = Task(description="Morning walk", time="08:00", duration=20, priority="medium")
    pet.add_task(later_task)
    pet.add_task(earlier_task)

    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.sort_by_time()

    assert [task.description for task in sorted_tasks[:2]] == ["Morning walk", "Evening walk"]


def test_handle_recurrence_creates_next_day_tasks():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi")
    owner.add_pet(pet)

    recurring_task = Task(description="Medicine", time="21:00", duration=10, priority="high", frequency="daily")
    pet.add_task(recurring_task)

    scheduler = Scheduler(owner)
    generated_tasks = scheduler.handle_recurrence()

    assert len(generated_tasks) == 3
    assert all(task.description.startswith("Medicine") for task in generated_tasks)
    assert all(task.frequency is None for task in generated_tasks)


def test_detect_conflicts_flags_duplicate_times_without_duration():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi")
    owner.add_pet(pet)

    first_task = Task(description="Grooming", time="09:00", duration=None)
    second_task = Task(description="Pill time", time="09:00", duration=None)
    pet.add_task(first_task)
    pet.add_task(second_task)

    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()

    assert len(conflicts) == 1
    assert conflicts[0][0].description == "Grooming"
    assert conflicts[0][1].description == "Pill time"


def test_sort_by_time_keeps_equal_priority_in_order():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi")
    owner.add_pet(pet)

    first = Task(description="Alpha", time="10:00", priority="high")
    second = Task(description="Beta", time="11:00", priority="high")
    pet.add_task(second)
    pet.add_task(first)

    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.sort_by_time()

    assert [task.description for task in sorted_tasks] == ["Alpha", "Beta"]


def test_sort_by_time_handles_tasks_with_no_time():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi")
    owner.add_pet(pet)

    timed_task = Task(description="Timed", time="08:00")
    no_time_task = Task(description="Untimed")
    pet.add_task(no_time_task)
    pet.add_task(timed_task)

    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.sort_by_time()

    assert sorted_tasks[-1].description == "Untimed"


def test_handle_recurrence_creates_new_occurrence_for_recurring_task():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi")
    owner.add_pet(pet)

    recurring_task = Task(description="Medicine", time="21:00", frequency="daily", duration=10)
    pet.add_task(recurring_task)

    scheduler = Scheduler(owner)
    generated_tasks = scheduler.handle_recurrence()

    assert generated_tasks[0].description.startswith("Medicine")
    assert generated_tasks[0].time == "21:00"


def test_handle_recurrence_does_nothing_without_frequency():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi")
    owner.add_pet(pet)

    task = Task(description="Feed", time="07:00", duration=10)
    pet.add_task(task)

    scheduler = Scheduler(owner)
    generated_tasks = scheduler.handle_recurrence()

    assert generated_tasks == []


def test_handle_recurrence_skips_completed_tasks():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi")
    owner.add_pet(pet)

    completed_task = Task(description="Completed", time="20:00", frequency="daily", duration=10)
    completed_task.mark_complete()
    pet.add_task(completed_task)

    scheduler = Scheduler(owner)
    generated_tasks = scheduler.handle_recurrence()

    assert generated_tasks == []


def test_detect_conflicts_flags_overlapping_times():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi")
    owner.add_pet(pet)

    first = Task(description="Walk", time="08:00", duration=30)
    second = Task(description="Brush", time="08:15", duration=20)
    pet.add_task(first)
    pet.add_task(second)

    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()

    assert len(conflicts) == 1


def test_detect_conflicts_returns_no_conflict_for_non_overlapping_times():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi")
    owner.add_pet(pet)

    first = Task(description="Walk", time="08:00", duration=30)
    second = Task(description="Brush", time="09:00", duration=20)
    pet.add_task(first)
    pet.add_task(second)

    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()

    assert conflicts == []


def test_detect_conflicts_handles_tasks_with_no_duration():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi")
    owner.add_pet(pet)

    first = Task(description="Walk", time="08:00", duration=None)
    second = Task(description="Brush", time="08:30", duration=None)
    pet.add_task(first)
    pet.add_task(second)

    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()

    assert conflicts == []


def test_filter_tasks_returns_only_incomplete_tasks():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi")
    owner.add_pet(pet)

    incomplete = Task(description="Pending", time="08:00")
    complete = Task(description="Done", time="09:00")
    complete.mark_complete()
    pet.add_task(incomplete)
    pet.add_task(complete)

    scheduler = Scheduler(owner)
    filtered = scheduler.filter_tasks(tasks=[incomplete, complete], completion_status=False)

    assert [task.description for task in filtered] == ["Pending"]


def test_filter_tasks_returns_empty_when_all_complete():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi")
    owner.add_pet(pet)

    complete = Task(description="Done", time="09:00")
    complete.mark_complete()
    pet.add_task(complete)

    scheduler = Scheduler(owner)
    filtered = scheduler.filter_tasks(tasks=[complete], completion_status=False)

    assert filtered == []


def test_filter_tasks_returns_all_when_all_incomplete():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi")
    owner.add_pet(pet)

    first = Task(description="One", time="08:00")
    second = Task(description="Two", time="09:00")
    pet.add_task(first)
    pet.add_task(second)

    scheduler = Scheduler(owner)
    filtered = scheduler.filter_tasks(tasks=[first, second], completion_status=False)

    assert [task.description for task in filtered] == ["One", "Two"]
