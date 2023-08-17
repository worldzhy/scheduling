from ortools.sat.python import cp_model


# EXAMPLE DATA
num_studios = 3
num_days = 3
num_timeslots = 3
num_programs = 3
num_coaches = 3
all_studios = range(num_studios)
all_days = range(num_days)
all_timeslots = range(num_timeslots)
all_programs = range(num_programs)
all_coaches = range(num_coaches)


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
## For each timeslot, there is only one coach.
for s in all_studios:
    for d in all_days:
        for t in all_timeslots:
            for p in all_programs:
                model.AddExactlyOne(schedule[(s, d, t, p, c)] for c in all_coaches)
## For each timeslot, there is only one program.
for s in all_studios:
    for d in all_days:
        for t in all_timeslots:
            for c in all_coaches:
                model.AddExactlyOne(schedule[(s, d, t, p, c)] for p in all_programs)


# CREATE SOLVER
solver = cp_model.CpSolver()
solver.parameters.linearization_level = 0
solver.parameters.enumerate_all_solutions = True


# REGISTER CALLBACK SOLUTION
class SchedulePartialSolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, schedule, num_studios, num_days, num_timeslots, num_programs, num_coaches, limit):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._schedule = schedule
        self._num_studios = num_studios
        self._num_days = num_days
        self._num_timeslots = num_timeslots
        self._num_programs = num_programs
        self._num_coaches = num_coaches
        self._solution_count = 0
        self._solution_limit = limit

    def on_solution_callback(self):
        self._solution_count += 1
        print(f"Solution {self._solution_count}")
        for s in range(self._num_studios):
            print(f"Studio {s}")
            for d in range(self._num_days):
                print(f"Day {d}")
                for t in range(self._num_timeslots):
                    print(f"Timeslot {t}")
                    for p in range(self._num_programs):
                        for c in range(self._num_coaches):
                            if self.Value(self._schedule[(s, d, t, p, c)]):
                                print(f"  Coach {c} teaches program {p}")
        if self._solution_count >= self._solution_limit:
            print(f"Stop search after {self._solution_limit} solutions")
            self.StopSearch()

    def solution_count(self):
        return self._solution_count


# CONFIGURE SOLUTION DISPLAY
solution_limit = 1
solution_printer = SchedulePartialSolutionPrinter(
    schedule,
    num_studios,
    num_days,
    num_timeslots,
    num_programs,
    num_coaches,
    solution_limit
)


# EXECUTE SOLVE
solver.Solve(model, solution_printer)
