from random import uniform
import sys
from typing import Callable, List
from .Result import Result
from .Day import Day
from .Constant import Constant
from .Course import Course

class Schedule:
    def __init__(self, list: List[List[Course]]):
        # list of courses that makes up the schedule
        self.course_list: List[List[Course]] = list

    # mutate the schedule
    def mutate(self, gen_day_courses: Callable[[int], List[Course]], mutation_rate: float = 0.4):
        for i, _ in enumerate(self.course_list):
            if (uniform(0, 1) > mutation_rate):
                self.course_list[i] = gen_day_courses(i)

    # calculate the value of the current schedule
    def get_value(self) -> float:
        sum = self._get_value_no_conflicts()
        return sum
    
    # get value for 
    def _get_value_no_conflicts(self) -> float:
        score = 0
        total = 0
        # loop for each day in list
        for day_course_list in self.course_list:
            # cross reference each courses in the day and check for conflicts
            for c1 in day_course_list:
                total += 1
                hasConflict = False
                for c2 in day_course_list:
                    # if course is different and day and time overlaps, then has conflict
                    if (c1 != c2 and self._is_overlap(c1, c2)):
                        hasConflict = True
                        break
                # if course has no conflict, add one point
                if (hasConflict == False):
                    score += 1
        return score / total

    # check if two courses overlap
    def _is_overlap(self, course1: Course, course2: Course) -> bool:
        is_day_same = course1.day.id == course2.day.id
        is_time_overlap = course1.time.num_end > course2.time.num_start and course2.time.num_end > course1.time.num_start
        return is_day_same and is_time_overlap
    
    # get conflicts
    def get_conflicts(self) -> List[int]:
        # initialize list of conflicts
        conflicts: List[int] = []
        # initialize timeslot used to check if schedule is conflict ot not
        timeslots: List[List[int]] = [[False for _ in range(Constant.SLOTS_PER_DAY_NUM)] for _ in range(Constant.DAYS_NUM)]
        # remove blank slots and sort schedule by day
        course_list = sorted(self.course_list, key=lambda c: c[0].day.value)
        # for each day, check for conflicts one by one
        for day_course_list in course_list:
            # sort by time
            day_course_list_sorted = sorted(day_course_list, key=lambda c: c.time.num_start)
            for idx, s in enumerate(day_course_list_sorted):
                day = s.day.value
                time = s.time.num_start
                duration = s.program.duration
                # ignore courses that is out of bounds
                isOutOfBounds = False
                for time_specific in range(duration // Constant.RESOLUTION_IN_MINUTES):
                    if (time + time_specific >= len(timeslots[day])):
                        isOutOfBounds = True
                        break
                # populate list of conflicts
                if (isOutOfBounds == False):
                    for time_specific in range(duration // Constant.RESOLUTION_IN_MINUTES):
                        if (timeslots[day][time + time_specific] == True):
                            conflicts.append(idx + 1)
                            break
                        if (timeslots[day][time + time_specific] == False):
                            timeslots[day][time + time_specific] = True
        return conflicts

    def repair_days_to_match_index(self, get_day: Callable[[str], Day]) -> None:
        for i, day_course_list in enumerate(self.course_list):
            for c in day_course_list:
                current_day = get_day('D' + str(i))
                c.update_day(current_day)

    # write schedule to output file
    def save_to_file(self, filename: str = 'output.out'):
        with open(filename, 'w') as f:
            sys.stdout = f
            # sort by day
            course_list = sorted(self.course_list, key=lambda c: c[0].day.value)
            for day_course_list in course_list:
                # sort by time
                day_course_list_sorted = sorted(day_course_list, key=lambda c: c.time.num_start)
                for c in day_course_list_sorted:
                    # print
                    print(f'Day {c.day.value + 1} -- {c.time.clock_start} to {c.time.clock_end} -- {c.program.name} {c.program.duration} mins -- {c.coach.name}')
            sys.stdout = sys.__stdout__

    def to_json(self) -> List[Result]:
        result: List[Result] = []
        for day_course_list in self.course_list:
            for c in day_course_list:
                result.append({
                    'studio': '---',
                    'program': c.program.name,
                    'coach': c.coach.name,
                    'time': {
                        'start': c.time.clock_start,
                        'end': c.time.clock_end,
                    },
                    'day': str(c.day.value + 1),
                })
        return result
