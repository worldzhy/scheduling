from typing import List, NamedTuple
from xmlrpc.client import boolean
from entities.Course import Course

class Qualification(NamedTuple):
    programId: str
    coachId: str
    is_qualified: boolean

## Genetic Algorithm Representation

Genome = List[Course | None]

Population = List[Genome]
