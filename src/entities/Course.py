from entities.Coach import Coach
from entities.Day import Day
from entities.Program import Program
from entities.Time import Time


class Course():
    # Initializes time
    def __init__(self, program: Program, coach: Coach, day: Day, time: Time, start_time: str, end_time: str):
        self.program = program
        self.coach = coach
        self.day = day
        self.time = time
        self.start_time = start_time
        self.end_time = end_time
