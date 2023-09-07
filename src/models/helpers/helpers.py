import csv
from typing import List, Type, TypeVar
from helpers.types import Studio, Program, Coach, Day, Class, Qualification

# Helper functions
def load_data():
    T = TypeVar('T')
    def get_data(set_type: Type[T], set_name: str) -> List[T]:
        ret: List[T] = []
        if set_name == 'days':
            for day in range(30):
                ret.append(set_type('D' + str(day), day))
        else: 
            with open(f'data/processed/{set_name}.csv', 'r') as csv_file:
                data = csv.DictReader(csv_file)
                for row in data:
                    ret.append(set_type(row['id'], row['name']))
        return ret
    return get_data(Studio, 'studios'), get_data(Program, 'programs'), get_data(Coach, 'coaches'), get_data(Day, 'days')

def get_choices(programs: List[Program], coaches: List[Coach]) -> List[Class]:
    choices: List[Class] = []
    choices.append(Class(None, None))
    for p in programs:
        for c in coaches:
            choices.append(Class(p.id, c.id))
    return choices

def get_qualifications(programs: List[Program], coaches: List[Coach]) -> List[Qualification]:
    ret: List[Qualification] = []
    with open('data/processed/constraints.csv', 'r') as csv_file:
        data = csv.DictReader(csv_file)
        coachIds = [coach.id for coach in coaches]
        programIds = [program.id for program in programs]
        for c in coachIds:
            for p in programIds:
                ret.append(Qualification(p, c, False))
        for row in data:
            if row['coach'] in coachIds:
                for p in row['programs'].split(','):
                        if p in programIds:
                                ret.append(Qualification(p, row['coach'], True))
    return ret