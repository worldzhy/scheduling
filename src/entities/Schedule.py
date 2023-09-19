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
        timeslots: List[List[int]] = [[0 for _ in range(Constant.SLOTS_PER_DAY_NUM)] for _ in range(Constant.DAYS_NUM)]
        for s in self.list:
            if s is not None:
                day = s.day.value
                time = s.time.num_start
                duration = s.program.duration
                isOutOfBounds = False
                for time_specific in range(duration // Constant.RESOLUTION_IN_MINUTES):
                    if (time + time_specific >= len(timeslots[day])):
                        isOutOfBounds = True
                        break
                if isOutOfBounds == False:
                    for time_specific in range(duration // Constant.RESOLUTION_IN_MINUTES):
                        timeslots[day][time + time_specific] += 1
        sum = 0
        for day in timeslots:
            for freq in day:
                if (freq == 0):
                    sum += 0
                if (freq == 1):
                    sum += 10
                else: 
                    sum += -freq
        return sum

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
