from typing import List, NamedTuple, Union
from xmlrpc.client import boolean

## Basic Entities

class Studio(NamedTuple):
        id: str
        name: str

class Program(NamedTuple):
        id: str
        name: str

class Coach(NamedTuple):
        id: str
        name: str

class Day(NamedTuple):
        id: str
        name: str

## Compounded Type

class Class(NamedTuple):
    programId: Union[str, None]
    coachId: Union[str, None]

class Qualification(NamedTuple):
    programId: str
    coachId: str
    is_qualified: boolean

## Genetic Algorithm Representation

Genome = List[Class]

Population = List[Genome]
