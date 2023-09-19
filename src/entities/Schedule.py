from random import uniform
import sys
from typing import Callable, List
from .Constant import Constant
from .Course import Course

class Schedule:
    def __init__(self, list: List[Course | None]):
        # list of courses that makes up the schedule
        self.list: List[Course | None] = list

    # mutate the schedule
    def mutate(self, gen_course: Callable[[], Course | None], mutation_rate: float = 0.4):
        for i, _ in enumerate(self.list):
            if (uniform(0, 1) > mutation_rate):
                self.list[i] = gen_course()

    # calculate the value of the current schedule
    def get_value(self) -> float:
        sum = self._get_value_conflicts()
        return sum
    
    # get value for 
    def _get_value_conflicts(self) -> float:
        score = 0
        total = sum(1 for s in self.list if s is not None)
        for s1 in self.list:
            if (s1 is None):
                continue
            hasConflict = False
            for s2 in self.list:
                if (s2 is None):
                    continue
                if (s1 != s2 and self._is_overlap(s1, s2)): # Has conflict
                    hasConflict = True
                    break
            if (hasConflict == False):
                score += 1
        return score / total

    # check if two courses overlap
    def _is_overlap(self, course1: Course, course2: Course) -> bool:
        isDaySame = course1.day.id == course2.day.id
        isTimeOverlap = course1.time.num_end >= course2.time.num_start and course2.time.num_end >= course1.time.num_start
        return isDaySame and isTimeOverlap
    
    # get conflicts
    def get_conflicts(self) -> List[int]:
        # initialize list of conflicts
        conflicts: List[int] = []
        # initialize timeslot used to check if schedule is conflict ot not
        timeslots: List[List[int]] = [[False for _ in range(Constant.SLOTS_PER_DAY_NUM)] for _ in range(Constant.DAYS_NUM)]
        # remove blank slots and sort schedule by day and time
        schedule = [s for s in self.list if s is not None]
        schedule = sorted(schedule, key=lambda s: (s.day.value, s.time.num_start))
        # check for conflicts one by one
        for idx, s in enumerate(schedule):
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

    # write schedule to output file
    def save_to_file(self, filename: str = 'output.out'):
        schedule = [c for c in self.list if c is not None]
        schedule = sorted(schedule, key=lambda c: (c.day.value, c.time.num_start))
        with open(filename, 'w') as f:
            sys.stdout = f
            for c in schedule:
                print(f'Day {c.day.value + 1} -- {c.time.clock_start} to {c.time.clock_end} -- {c.program.name} {c.program.duration} mins -- {c.coach.name}')
            sys.stdout = sys.__stdout__
