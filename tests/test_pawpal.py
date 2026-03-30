import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
from datetime import date
from pawpal_system import Pet, Task, Scheduler, PetOwner


def make_task(id=1, pet_id=1):
    return Task(id=id, pet_id=pet_id, status="pending", description="Feed pet", frequency=1, time="08:00 AM")


def make_owner_with_scheduler():
    owner = PetOwner(id=1, name="Natwange", email="natwange@email.com")
    scheduler = Scheduler(id=1, pet_id=1, date=date.today(), status="active")
    owner.scheduler = scheduler
    return owner


# Test 1: mark_complete() changes task status to "completed"
def test_mark_complete_changes_status():
    task = make_task()
    assert task.status == "pending"
    task.mark_complete()
    assert task.status == "completed"


# Test 2: adding a task via owner increases the task count
def test_add_task_increases_count():
    owner = make_owner_with_scheduler()
    assert len(owner.get_tasks()) == 0

    owner.add_task(make_task(id=1))
    assert len(owner.get_tasks()) == 1

    owner.add_task(make_task(id=2))
    assert len(owner.get_tasks()) == 2
