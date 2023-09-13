from entities.Coach import Coach
from entities.Day import Day
from entities.Program import Program
from entities.Time import Time


class Course():
    # Initializes time
    def __init__(self, program: Program, coach: Coach, day: Day, time: Time):
        self.program = program
        self.coach = coach
        self.day = day
        self.time = time
        # Incoporate end time
        self.time.add_clock_end(self.program.duration)
