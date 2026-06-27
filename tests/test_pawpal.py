import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pawpal_system import Pet, Task


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
