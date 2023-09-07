from typing import List, NamedTuple, Union
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
        name: str

## Compounded Type

class Course(NamedTuple):
    programId: Union[str, None]
    coachId: Union[str, None]

class CourseWithSchedule(NamedTuple):
    course: Course
    start_time: int
    end_time: int
    duration: int

class Qualification(NamedTuple):
    programId: str
    coachId: str
    is_qualified: boolean

## Genetic Algorithm Representation

Genome = List[Course]

Population = List[Genome]
