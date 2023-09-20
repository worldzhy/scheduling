from .Constant import Constant
from .Coach import Coach
from .Day import Day
from .Program import Program
from .Time import Time


class Course():
    def __init__(self, program: Program, coach: Coach, day: Day, time: Time):
        self.program = program
        self.coach = coach
        self.day = day
        self.time = time
        # incoporate end time
        self.time.add_clock_end(self.program.duration)

    # checks if end time is beyond timeslot
    def isOutOfBound(self) -> bool:
        return self.time.num_end > Constant.SLOTS_PER_DAY_NUM

    # change the day of the course
    def update_day(self, day: Day) -> None:
        self.day = day