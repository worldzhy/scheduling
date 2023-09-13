from typing import List, NamedTuple
from xmlrpc.client import boolean
from entities.Coach import Coach
from entities.Day import Day
from entities.Time import Time
from entities.Program import Program

## Compounded Type

class Course(NamedTuple):
    program: Program
    coach: Coach
    day: Day
    time: Time
    start_time: str
    end_time: str

# class CourseWithSchedule(NamedTuple):
#     course: Course
#     start_time: int
#     end_time: int
#     duration: int

class Qualification(NamedTuple):
    programId: str
    coachId: str
    is_qualified: boolean

## Genetic Algorithm Representation

Genome = List[Course | None]

Population = List[Genome]
