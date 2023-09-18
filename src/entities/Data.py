import csv
from random import choices, uniform
from typing import List
from .Coach import Coach
from .Course import Course
from .Day import Day
from .Program import Program
from .Studio import Studio
from .Time import Time

class Data:
    def __init__(self):
        # configuration
        self._studio_csv: str = 'data/processed/studios.csv'
        self._program_csv: str = 'data/processed/programs.csv'
        self._coach_csv: str = 'data/processed/coaches.csv'
        self._none_probability: float = 0.2
        # parsed studios
        self.studios: List[Studio] = []
        # parsed times
        self.times: List[Time] = []
        # parsed days
        self.days: List[Day] = []
        # parsed programs
        self.programs: List[Program] = []
        # parsed coaches
        self.coaches: List[Coach] = []

    # populates studio
    def _parse_studio(self):
        with open(self._studio_csv, 'r') as csv_file:
            for row in csv.DictReader(csv_file):
               self.studios.append(Studio(row['id'], row['name']))

    # populates time
    def _parse_time(self):
        for time in range(205):
            self.times.append(Time('T' + str(time), int(time)))

    # populates day
    def _parse_day(self):
        for day in range(30):
            self.days.append(Day('D' + str(day), int(day)))

    # populates program
    def _parse_program(self):
        with open(self._program_csv, 'r') as csv_file:
            for row in csv.DictReader(csv_file):
                self.programs.append(Program(row['id'], row['name'], int(row['duration'])))

    # populates coach
    def _parse_coach(self):
        with open(self._coach_csv, 'r') as csv_file:
            for row in csv.DictReader(csv_file):
               self.coaches.append(Coach(row['id'], row['name']))

    # populates coach qualification
    def _add_coach_qualification(self):
        with open('data/processed/constraints.csv', 'r') as csv_file:
            for row in csv.DictReader(csv_file):
                # find coach in coaches array
                coach: None | Coach = None
                for c in self.coaches:
                    if (c.id == row['coach']):
                        coach = c
                        break
                if coach is None:
                    continue
                # add programs to coach
                for p in self.programs:
                    if (p.id in row['programs'].split(',')):
                        coach.add_program(p)

    # configure data arguments
    def configure(
        self,
        studio_csv: None | str = None,
        program_csv: None | str = None,
        coach_csv: None | str = None,
        none_probability: None | float = None,
    ) -> None:
        self._studio_csv = studio_csv if studio_csv is not None else self._studio_csv
        self._program_csv = program_csv if program_csv is not None else self._program_csv
        self._coach_csv = coach_csv if coach_csv is not None else self._coach_csv
        self._none_probability = none_probability if none_probability is not None else self._none_probability

    # loads data
    def load(self):
        # load data
        self._parse_studio()
        self._parse_time()
        self._parse_day()
        self._parse_program()
        self._parse_coach()
        # add coach qualification
        self._add_coach_qualification()
        
    # randomly generates a course    
    def get_rnd_course(self):
        if (uniform(0, 1) > self._none_probability):
            return Course(
                choices(self.programs, k = 1)[0],
                choices(self.coaches, k = 1)[0],
                choices(self.days, k = 1)[0],
                choices(self.times, k = 1)[0]
            )
        else:
            return None