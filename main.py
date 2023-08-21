from ortools.sat.python import cp_model
import csv

# DATA
## Array of data (manually list for now)
all_studios = ['s1', 's2', 's3']
all_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
all_timeslots = ['t1', 't2', 't3', 't4', 't5']
all_programs = ['p1', 'p2', 'p3']
all_coaches = ['c1', 'c2', 'c3']

## Coach skills
coaches_skills = {}
for c in all_coaches:
    for p in all_programs:
        coaches_skills[(c, p)] = 0
with open('data/constraints.csv', 'r') as csv_file:
    coach_data = csv.DictReader(csv_file)
    for coach in coach_data:
        for p in coach['programs'].split(','):
            if p in all_programs:
                coaches_skills[(coach['coach'], p)] = 1

## Coach availability (manually list for now)
coaches_availability = {}
for c in all_coaches:
    for s in all_studios:
        for d in all_days:
            for t in all_timeslots:
                coaches_availability[(c, s, d, t)] = 0
with open('data/constraints.csv', 'r') as csv_file:
    coach_data = csv.DictReader(csv_file)
    for coach in coach_data:
        for s in coach['studios'].split(','):
            for d in all_days:
                for t in coach[d].split(','):
                    if s in all_studios and t in all_timeslots:
                        coaches_availability[(coach['coach'], s, d, t)] = 1



# CREATE MODEL
model = cp_model.CpModel()


# DECISION VARIABLES
## The schedule array defines the scheduling as follows:
## schedule[(s, d, t, p, c)] = 1 means coach c is assigned to teach program p on timeslot t on day d at studio s.
schedule = {}
for s in all_studios:
    for d in all_days:
        for t in all_timeslots:
            for p in all_programs:
                for c in all_coaches:
                    schedule[(s, d, t, p, c)] = model.NewBoolVar(f"schedule_s{s}_d{d}_t{t}_p{p}_c{c})")


# CONSTRAINTS
## For each timeslot, there is only one program and one coach.
for s in all_studios:
    for d in all_days:
        for t in all_timeslots:
            model.AddExactlyOne(schedule[(s, d, t, p, c)] for p in all_programs for c in all_coaches)

## Coaches should only be assigned programs they are qualified for
for s in all_studios:
    for d in all_days:
        for t in all_timeslots:
            for p in all_programs:
                for c in all_coaches:
                    if coaches_skills[(c, p)] == 0:
                        model.Add(schedule[(s, d, t, p, c)] == 0)

## Coaches should only be assigned schedules they are available for
for s in all_studios:
    for d in all_days:
        for t in all_timeslots:
            for p in all_programs:
                for c in all_coaches:
                    if coaches_availability[(c, s, d, t)] == 0:
                        model.Add(schedule[(s, d, t, p, c)] == 0)

# CREATE SOLVER
solver = cp_model.CpSolver()
solver.parameters.linearization_level = 0
solver.parameters.enumerate_all_solutions = True


# REGISTER CALLBACK SOLUTION
class SchedulePartialSolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, schedule, all_studios, all_days, all_timeslots, all_programs, all_coaches, limit):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._schedule = schedule
        self._all_studios = all_studios
        self._all_days = all_days
        self._all_timeslots = all_timeslots
        self._all_programs = all_programs
        self._all_coaches = all_coaches
        self._solution_count = 0
        self._solution_limit = limit

    def on_solution_callback(self):
        self._solution_count += 1
        print(">" * 100)
        print(f"Solution {self._solution_count}")
        for s in self._all_studios:
            print(f"  Studio: {s}")
            for d in self._all_days:
                print(f"    {d}")
                for t in self._all_timeslots:
                    for p in self._all_programs:
                        for c in self._all_coaches:
                            if self.Value(self._schedule[(s, d, t, p, c)]):
                                print(f"      {t}: {c} to teach {p}")
        if self._solution_count >= self._solution_limit:
            print(f"Stop search after {self._solution_limit} solutions")
            self.StopSearch()

    def solution_count(self):
        return self._solution_count


# CONFIGURE SOLUTION DISPLAY
solution_limit = 1
solution_printer = SchedulePartialSolutionPrinter(
    schedule,
    all_studios,
    all_days,
    all_timeslots,
    all_programs,
    all_coaches,
    solution_limit
)


# EXECUTE SOLVE
solver.Solve(model, solution_printer)
