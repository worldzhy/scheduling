from ortools.sat.python import cp_model

from src.entities.Data import Data

# DATA
data = Data()
data.load()
studios = data.studios
# days = data.days Assume one day for now
programs = data.programs
coaches = data.coaches

# PARAMETERS
MAX_DURATION = 204
MAX_PER_DAY = 25
coach_intervals = {c: {} for c in range(len(coaches))}

# CREATE MODEL
model = cp_model.CpModel()

# Schedule tasks such that:
# All tasks of all schedules are tackled
# All tasks have a corresponding operator and machine
# Schedule of studios must not overlap
# Schedule of machine must not overlap


# # DECISION VARIABLES
# ## The schedule array defines the scheduling as follows:
# ## schedule[(s, d, t, p, c)] = 1 means coach c is assigned to teach program p on timeslot t on day d at studio s.
# schedule = {}
# for s in all_studios:
#     for d in all_days:
#         for t in all_timeslots:
#             for p in all_programs:
#                 for c in all_coaches:
#                     schedule[(s, d, t, p, c)] = model.NewBoolVar(f"schedule_s{s}_d{d}_t{t}_p{p}_c{c})")


# # CONSTRAINTS
# ## For each timeslot, there is only one program and one coach.
# for s in all_studios:
#     for d in all_days:
#         for t in all_timeslots:
#             model.AddExactlyOne(schedule[(s, d, t, p, c)] for p in all_programs for c in all_coaches)

# ## Coaches should only be assigned programs they are qualified for
# for s in all_studios:
#     for d in all_days:
#         for t in all_timeslots:
#             for p in all_programs:
#                 for c in all_coaches:
#                     if coaches_skills[(c, p)] == 0:
#                         model.Add(schedule[(s, d, t, p, c)] == 0)

# ## Coaches should only be assigned schedules they are available for
# for s in all_studios:
#     for d in all_days:
#         for t in all_timeslots:
#             for p in all_programs:
#                 for c in all_coaches:
#                     if coaches_availability[(c, s, d, t)] == 0:
#                         model.Add(schedule[(s, d, t, p, c)] == 0)

# # CREATE SOLVER
# solver = cp_model.CpSolver()
# solver.parameters.linearization_level = 0
# solver.parameters.enumerate_all_solutions = True


# # REGISTER CALLBACK SOLUTION
# class SchedulePartialSolutionPrinter(cp_model.CpSolverSolutionCallback):
#     """Print intermediate solutions."""

#     def __init__(self, schedule, all_studios, all_days, all_timeslots, all_programs, all_coaches, limit):
#         cp_model.CpSolverSolutionCallback.__init__(self)
#         self._schedule = schedule
#         self._all_studios = all_studios
#         self._all_days = all_days
#         self._all_timeslots = all_timeslots
#         self._all_programs = all_programs
#         self._all_coaches = all_coaches
#         self._solution_count = 0
#         self._solution_limit = limit

#     def on_solution_callback(self):
#         self._solution_count += 1
#         print(">" * 100)
#         print(f"Solution {self._solution_count}")
#         for s in self._all_studios:
#             print(f"  Studio: {studios[(s, 'name')]}")
#             for d in self._all_days:
#                 print(f"    {d}")
#                 for t in self._all_timeslots:
#                     for p in self._all_programs:
#                         for c in self._all_coaches:
#                             if self.Value(self._schedule[(s, d, t, p, c)]):
#                                 print(f"      {timeslots[(t, 'name')]}: {coaches[(c, 'name')]} to teach {programs[(p, 'name')]}")
#         if self._solution_count >= self._solution_limit:
#             print(f"Stop search after {self._solution_limit} solutions")
#             self.StopSearch()

#     def solution_count(self):
#         return self._solution_count


# # CONFIGURE SOLUTION DISPLAY
# solution_limit = 1
# solution_printer = SchedulePartialSolutionPrinter(
#     schedule,
#     all_studios,
#     all_days,
#     all_timeslots,
#     all_programs,
#     all_coaches,
#     solution_limit
# )


# # EXECUTE SOLVE
# solver.Solve(model, solution_printer)