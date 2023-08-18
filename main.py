from ortools.sat.python import cp_model


# EXAMPLE DATA
## Array of data
all_studios = ['Culver City', 'Hollywood', 'Pasedena']
all_days = [1, 2]
all_timeslots = ['6:00am - 6:50am', '7:00am - 7:50am', '8:00am - 8:50am', '9:00am - 9:50am', '10:00am - 10:50am']
all_programs = ['Full Body (center glutes & triceps)', 'Full Body (hamstrings & biceps)', 'Buns + Abs']
all_coaches = ['Taylor T.', 'Cianna P.', 'Maya D.']

## Coach skills (manually list for now)
coaches_skills = {}
for c in all_coaches:
    for p in all_programs:
        coaches_skills[(c, p)] = 0
coaches_skills[('Taylor T.', 'Full Body (center glutes & triceps)')] = 1
coaches_skills[('Taylor T.', 'Buns + Abs')] = 1
coaches_skills[('Cianna P.', 'Full Body (hamstrings & biceps)')] = 1
coaches_skills[('Cianna P.', 'Full Body (center glutes & triceps)')] = 1
coaches_skills[('Maya D.', 'Buns + Abs')] = 1


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
                print(f"    Day {d}")
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
solution_limit = 2
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
