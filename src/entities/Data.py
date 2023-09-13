import csv
from typing import List
from entities.Coach import Coach
from entities.Configuration import Configuration
from entities.Day import Day
from entities.Program import Program
from entities.Studio import Studio
from entities.Time import Time

class Data:
    def __init__(self, config: Configuration):
        # config
        self.config = config
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

    def _parse_studio(self):
        with open(self.config.studio_csv, 'r') as csv_file:
            for row in csv.DictReader(csv_file):
               self.studios.append(Studio(row['id'], row['name']))

    def _parse_time(self):
        for time in range(205):
            self.times.append(Time('T' + str(time), int(time)))

    def _parse_day(self):
        for time in range(30):
            self.days.append(Day('D' + str(time), int(time)))

    def _parse_program(self):
        with open(self.config.program_csv, 'r') as csv_file:
            for row in csv.DictReader(csv_file):
                self.programs.append(Program(row['id'], row['name'], int(row['duration'])))

    def _parse_coach(self):
        with open(self.config.coach_csv, 'r') as csv_file:
            for row in csv.DictReader(csv_file):
               self.coaches.append(Coach(row['id'], row['name']))

    def _add_coach_qualification(self):
        with open('data/processed/constraints.csv', 'r') as csv_file:
            for row in csv.DictReader(csv_file):
                # Find coach in coaches array
                coach: None | Coach = None
                for c in self.coaches:
                    if (c.id == row['coach']):
                        coach = c
                        break
                if coach is None:
                    continue
                # Add programs to coach
                for p in self.programs:
                    if (p.id in row['programs'].split(',')):
                        coach.add_program(p)

    def load(self):
        # Load data
        self._parse_studio()
        self._parse_time()
        self._parse_day()
        self._parse_program()
        self._parse_coach()

        # Add coach qualification
        self._add_coach_qualification()
        
        # Return values
        return self.studios, self.programs, self.coaches, self.days, self.times
