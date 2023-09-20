import copy
import csv
from random import choices
from typing import List
from .Constant import Constant
from .Coach import Coach
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
        self._no_sched_probability: float = 0.2
        self._gen_random_course_max_attempt: int = 100
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

    # get studio randomly or by id
    def get_studio(self, id: str | None = None) -> Studio:
        if id is None:
            # return random studio
            return copy.deepcopy(choices(self.studios, k = 1)[0])
        else:
            for s in self.studios:
                # return studio with matching id if found
                if (s.id == id):
                    return copy.deepcopy(s)
            # if no matching id found, raise exception
            raise Exception(f'Studio {id} not found')

    # populates time
    def _parse_time(self):
        """
        Example:
        0 - 5:00 AM to 5:05 AM
        1 - 5:05 AM to 5:10 AM
        ...
        203 - 9:55 PM to 10:00 PM
        """
        for time in range(Constant.SLOTS_PER_DAY_NUM):
            self.times.append(Time('T' + str(time), int(time)))

    # get time randomly or by id
    def get_time(self, id: str | None = None) -> Time:
        if id is None:
            # return random time
            return copy.deepcopy(choices(self.times, k = 1)[0])
        else:
            for t in self.times:
                # return time with matching id if found
                if (t.id == id):
                    return copy.deepcopy(t)
            # if no matching id found, raise exception
            raise Exception(f'Time {id} not found')

    # populates day
    def _parse_day(self):
        """
        Example:
        0 - Day 1
        1 - Day 2
        ...
        29 - Day 30 
        """
        for day in range(Constant.DAYS_NUM):
            self.days.append(Day('D' + str(day), int(day)))

    # get day randomly or by id
    def get_day(self, id: str | None = None) -> Day:
        if id is None:
            # return random day
            return copy.deepcopy(choices(self.days, k = 1)[0])
        else:
            for d in self.days:
                # return day with matching id if found
                if (d.id == id):
                    return copy.deepcopy(d)
            # if no matching id found, raise exception
            raise Exception(f'Day {id} not found')

    # populates program
    def _parse_program(self):
        with open(self._program_csv, 'r') as csv_file:
            for row in csv.DictReader(csv_file):
                self.programs.append(Program(row['id'], row['name'], int(row['duration'])))

    # get program randomly or by id
    def get_program(self, id: str | None = None) -> Program:
        if id is None:
            # return random program
            return copy.deepcopy(choices(self.programs, k = 1)[0])
        else:
            for p in self.programs:
                # return program with matching id if found
                if (p.id == id):
                    return copy.deepcopy(p)
            # if no matching id found, raise exception
            raise Exception(f'Program {id} not found')

    # populates coach
    def _parse_coach(self):
        with open(self._coach_csv, 'r') as csv_file:
            for row in csv.DictReader(csv_file):
               self.coaches.append(Coach(row['id'], row['name']))

    # get coach randomly or by id
    def get_coach(self, id: str | None = None) -> Coach:
        if id is None:
            # return random coach
            return copy.deepcopy(choices(self.coaches, k = 1)[0])
        else:
            for c in self.coaches:
                # return coach with matching id if found
                if (c.id == id):
                    return copy.deepcopy(c)
            # if no matching id found, raise exception
            raise Exception(f'Coach {id} not found')

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
        no_sched_probability: None | float = None,
        gen_random_course_max_attempt: None | int = None
    ) -> None:
        self._studio_csv = studio_csv if studio_csv is not None else self._studio_csv
        self._program_csv = program_csv if program_csv is not None else self._program_csv
        self._coach_csv = coach_csv if coach_csv is not None else self._coach_csv
        self._no_sched_probability = no_sched_probability if no_sched_probability is not None else self._no_sched_probability
        self._gen_random_course_max_attempt = gen_random_course_max_attempt if gen_random_course_max_attempt is not None else self._gen_random_course_max_attempt

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
        