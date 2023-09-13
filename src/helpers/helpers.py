import csv
from typing import List, Type, TypeVar
from entities.Coach import Coach
from entities.Day import Day
from entities.Program import Program
from entities.Studio import Studio
from entities.Time import Time
from entities.Qualification import Qualification

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
    return get_data(Studio, 'studios'), get_data(Program, 'programs'), get_data(Coach, 'coaches'), get_data(Day, 'days'), get_data(Time, 'times')

# def get_choices(programs: List[Program], coaches: List[Coach]) -> List[Course]:
#     choices: List[Course] = []
#     choices.append(Course(None, None))
#     for p in programs:
#         for c in coaches:
#             choices.append(Course(p.id, c.id))
#     return choices

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

# def create_schedule(course: Course, start_time: int, end_time: int, resolution: int) -> CourseWithSchedule:
#         duration = (end_time - start_time) * resolution
#         return CourseWithSchedule(course, start_time, end_time, duration)

# def schedulize(courses: List[Course], resolution: int) -> List[CourseWithSchedule]:
#     results: List[CourseWithSchedule] = []
#     prev_course: Course = courses[0] 
#     start_time: int = 0

#     for i, current_course in enumerate(courses):
#         if i != 0 and (prev_course.programId != current_course.programId or prev_course.coachId != current_course.coachId):
#              results.append(create_schedule(prev_course, start_time, i, resolution))
#              start_time = i
#              prev_course = current_course
    
#     # Add last interval
#     results.append(create_schedule(prev_course, start_time, len(courses), resolution))

#     return results
