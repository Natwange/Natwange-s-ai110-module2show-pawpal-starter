from dataclasses import dataclass
from datetime import date
from typing import List

@dataclass
class Pet:
    id: int
    name: str
    species: str
    age: int
    
    def get_age(self) -> int:
        return self.age
    
    def get_species(self) -> str:
        return self.species


@dataclass
class Task:
    id: int
    status: str
    category: str
    
    def add_task(self) -> None:
        pass
    
    def edit_task(self) -> None:
        pass


@dataclass
class PlanGenerator:
    id: int
    date: date
    status: str
    tasks: List[Task] = None
    
    def create_plan(self) -> None:
        pass
    
    def list_plan(self) -> List[Task]:
        return self.tasks or []


@dataclass
class PetOwner:
    id: int
    name: str
    email: str
    pets: List[Pet] = None
    tasks: List[Task] = None
    plan_generator: PlanGenerator = None
    
    def login(self) -> None:
        pass
    
    def perform_task(self) -> None:
        pass