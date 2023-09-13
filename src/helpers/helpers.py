import csv
from typing import List, Type, TypeVar
from entities.Coach import Coach
from entities.Day import Day
from entities.Program import Program
from entities.Studio import Studio
from entities.Time import Time

# Helper functions
def load_data():
    T = TypeVar('T')
    def get_data(set_type: Type[T], set_name: str) -> List[T]:
        ret: List[T] = []
        if set_name == 'days':
            for day in range(30):
                ret.append(set_type('D' + str(day), int(day)))
        elif set_name == 'times':
            for time in range(205):
                ret.append(set_type('T' + str(time), int(time)))
        elif set_name == 'programs':
            with open(f'data/processed/programs.csv', 'r') as csv_file:
                data = csv.DictReader(csv_file)
                for row in data:
                    ret.append(set_type(row['id'], row['name'], int(row['duration'])))
        else: 
            with open(f'data/processed/{set_name}.csv', 'r') as csv_file:
                data = csv.DictReader(csv_file)
                for row in data:
                    ret.append(set_type(row['id'], row['name']))
        return ret
    # Load data
    studios = get_data(Studio, 'studios')
    programs = get_data(Program, 'programs')
    coaches = get_data(Coach, 'coaches')
    days = get_data(Day, 'days')
    times  = get_data(Time, 'times')
    # Add coach qualification
    add_coach_qualification(programs, coaches)
    # Return values
    return studios, programs, coaches, days, times

def add_coach_qualification(programs: List[Program], coaches: List[Coach]):
    with open('data/processed/constraints.csv', 'r') as csv_file:
        for row in csv.DictReader(csv_file):
            # Find coach in coaches array
            coach: None | Coach = None
            for c in coaches:
                if (c.id == row['coach']):
                    coach = c
                    break
            if coach is None:
                continue
            # Add programs to coach
            for p in programs:
                if (p.id in row['programs'].split(',')):
                    coach.add_program(p)
