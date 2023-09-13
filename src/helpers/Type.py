from typing import List, NamedTuple
from xmlrpc.client import boolean

## Basic Entities

class Studio(NamedTuple):
        id: str
        name: str

class Program(NamedTuple):
        id: str
        name: str
        duration: int

class Coach(NamedTuple):
        id: str
        name: str

class Day(NamedTuple):
        id: str
        value: int

class Time(NamedTuple):
        id: str
        value: int

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
