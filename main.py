from datetime import date, time
from pawpal_system import Pet, Task, Scheduler, PetOwner

# Create owner
owner = PetOwner(id=1, name="Adrian", email="natwange@email.com")

# Create two pets
pet1 = Pet(id=1, owner_id=1, name="Buddy", species="Dog", age=3)
pet2 = Pet(id=2, owner_id=1, name="Miso", species="Cat", age=5)

# Add pets to owner
owner.pets.append(pet1)
owner.pets.append(pet2)

# Create scheduler and link to owner
scheduler = Scheduler(id=1, date=date.today(), status="active")
owner.scheduler = scheduler

# Create three tasks with different times
task1 = Task(id=1, pet_id=1, status="pending", description="Feed Buddy", frequency=2, time=time(8, 0))
task2 = Task(id=2, pet_id=1, status="pending", description="Walk Buddy", frequency=1, time=time(12, 0))
task3 = Task(id=3, pet_id=2, status="pending", description="Clean Miso's litter", frequency=1, time=time(18, 0))

# Add tasks via owner (delegates to scheduler)
owner.add_task(task1)
owner.add_task(task2)
owner.add_task(task3)

# Display
print(f"Owner: {owner.name}")
for pet in owner.pets:
    print(f"  Pet: {pet.name} | Species: {pet.get_species()} | Age: {pet.get_age()}")

print("\n==============================")
print(f"  TODAY'S SCHEDULE - {date.today().strftime('%B %d, %Y')}")
print("==============================")
print(f"  Owner: {owner.name}")
print(f"  Pets:  {', '.join(p.name for p in owner.pets)}")
print("------------------------------")
pet_by_id = {p.id: p.name for p in owner.pets}
for task in owner.get_tasks():
    pet_name = pet_by_id.get(task.pet_id, "Unknown")
    print(f"  {task.time.strftime('%I:%M %p'):<12} {task.description:<30} | {pet_name:<8} | {task.status}")
print("==============================")

# --- Filter by pet ---
print("\n--- Buddy's Tasks ---")
for task in owner.get_tasks_by_pet(pet1.id):
    print(f"  {task.time.strftime('%I:%M %p')}  {task.description}")

print("\n--- Miso's Tasks ---")
for task in owner.get_tasks_by_pet(pet2.id):
    print(f"  {task.time.strftime('%I:%M %p')}  {task.description}")

# --- Recurring slots ---
print("\n--- Recurring Slots (expanded by frequency) ---")
for slot_time, task in scheduler.generate_recurring_slots():
    pet_name = pet_by_id.get(task.pet_id, "Unknown")
    print(f"  {slot_time.strftime('%I:%M %p')}  {task.description} ({pet_name})")

# --- Conflict detection ---
print("\n--- Conflict Detection ---")
try:
    conflict = Task(id=4, pet_id=1, status="pending", description="Brush Buddy", frequency=1, time=time(8, 0))
    owner.add_task(conflict)
except ValueError as e:
    print(f"  Caught conflict: {e}")
