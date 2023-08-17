from ortools.sat.python import cp_model

# Define variables
num_nurses = 4
num_shifts = 3
num_days = 3
all_nurses = range(num_nurses)
all_shifts = range(num_shifts)
all_days = range(num_days)

model = cp_model.CpModel()

# Decision variable
shifts = {}
for n in all_nurses:
    for d in all_days:
        for s in all_shifts:
            shifts[(n, d, s)] = model.NewBoolVar(f"shift_n{n}_d{d}_s{s}")

# Constraints
for d in all_days:
    for s in all_shifts:
        model.AddExactlyOne(shifts[(n, d, s)] for n in all_nurses)

for n in all_nurses:
    for d in all_days:
        model.AddAtMostOne(shifts[(n, d, s)] for s in all_shifts)

# Try to distribute the shifts evenly, so that each nurse works
# min_shifts_per_nurse shifts. If this is not possible, because the total
# number of shifts is not divisible by the number of nurses, some nurses will
# be assigned one more shift.
min_shifts_per_nurse = (num_shifts * num_days) // num_nurses
if num_shifts * num_days % num_nurses == 0:
    max_shifts_per_nurse = min_shifts_per_nurse
else:
    max_shifts_per_nurse = min_shifts_per_nurse + 1
for n in all_nurses:
    shifts_worked = []
    for d in all_days:
        for s in all_shifts:
            shifts_worked.append(shifts[(n, d, s)])
    model.Add(min_shifts_per_nurse <= sum(shifts_worked))
    model.Add(sum(shifts_worked) <= max_shifts_per_nurse)


# Update solver parameters
solver = cp_model.CpSolver()
solver.parameters.linearization_level = 0
# Enumerate all solutions.
solver.parameters.enumerate_all_solutions = True


# Register solutions callback
class NursesPartialSolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, shifts, num_nurses, num_days, num_shifts, limit):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._shifts = shifts
        self._num_nurses = num_nurses
        self._num_days = num_days
        self._num_shifts = num_shifts
        self._solution_count = 0
        self._solution_limit = limit

    def on_solution_callback(self):
        self._solution_count += 1
        print(f"Solution {self._solution_count}")
        for d in range(self._num_days):
            print(f"Day {d}")
            for n in range(self._num_nurses):
                is_working = False
                for s in range(self._num_shifts):
                    if self.Value(self._shifts[(n, d, s)]):
                        is_working = True
                        print(f"  Nurse {n} works shift {s}")
                if not is_working:
                    print(f"  Nurse {n} does not work")
        if self._solution_count >= self._solution_limit:
            print(f"Stop search after {self._solution_limit} solutions")
            self.StopSearch()

    def solution_count(self):
        return self._solution_count

# Display the first five solutions.
solution_limit = 5
solution_printer = NursesPartialSolutionPrinter(
    shifts, num_nurses, num_days, num_shifts, solution_limit
)

# Execute solve
solver.Solve(model, solution_printer)

# Solution 1
# Day 0
#   Nurse 0 does not work
#   Nurse 1 works shift 0
#   Nurse 2 works shift 1
#   Nurse 3 works shift 2
# Day 1
#   Nurse 0 works shift 2
#   Nurse 1 does not work
#   Nurse 2 works shift 1
#   Nurse 3 works shift 0
# Day 2
#   Nurse 0 works shift 2
#   Nurse 1 works shift 1
#   Nurse 2 works shift 0
#   Nurse 3 does not work
# Solution 2
# Day 0
#   Nurse 0 works shift 0
#   Nurse 1 does not work
#   Nurse 2 works shift 1
#   Nurse 3 works shift 2
# Day 1
#   Nurse 0 does not work
#   Nurse 1 works shift 2
#   Nurse 2 works shift 1
#   Nurse 3 works shift 0
# Day 2
#   Nurse 0 works shift 2
#   Nurse 1 works shift 1
#   Nurse 2 works shift 0
#   Nurse 3 does not work
# Solution 3
# Day 0
#   Nurse 0 works shift 0
#   Nurse 1 does not work
#   Nurse 2 works shift 1
#   Nurse 3 works shift 2
# Day 1
#   Nurse 0 works shift 1
#   Nurse 1 works shift 2
#   Nurse 2 does not work
#   Nurse 3 works shift 0
# Day 2
#   Nurse 0 works shift 2
#   Nurse 1 works shift 1
#   Nurse 2 works shift 0
#   Nurse 3 does not work
# Solution 4
# Day 0
#   Nurse 0 works shift 0
#   Nurse 1 does not work
#   Nurse 2 works shift 1
#   Nurse 3 works shift 2
# Day 1
#   Nurse 0 works shift 2
#   Nurse 1 works shift 1
#   Nurse 2 does not work
#   Nurse 3 works shift 0
# Day 2
#   Nurse 0 works shift 2
#   Nurse 1 works shift 1
#   Nurse 2 works shift 0
#   Nurse 3 does not work
# Solution 5
# Day 0
#   Nurse 0 does not work
#   Nurse 1 works shift 0
#   Nurse 2 works shift 1
#   Nurse 3 works shift 2
# Day 1
#   Nurse 0 works shift 2
#   Nurse 1 works shift 1
#   Nurse 2 does not work
#   Nurse 3 works shift 0
# Day 2
#   Nurse 0 works shift 2
#   Nurse 1 works shift 1
#   Nurse 2 works shift 0
#   Nurse 3 does not work
# Stop search after 5 solutions