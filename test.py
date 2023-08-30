# """Nurse scheduling problem with shift requests."""
# from ortools.sat.python import cp_model
import csv


# def main():
#     # This program tries to find an optimal assignment of nurses to shifts
#     # (3 shifts per day, for 7 days), subject to some constraints (see below).
#     # Each nurse can request to be assigned to specific shifts.
#     # The optimal assignment maximizes the number of fulfilled shift requests.
#     num_nurses = 5
#     num_shifts = 3
#     num_days = 7
#     all_nurses = range(num_nurses)
#     all_shifts = range(num_shifts)
#     all_days = range(num_days)
#     shift_requests = [
#         [[0, 0, 1], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 0, 1]],
#         [[0, 0, 0], [0, 0, 0], [0, 1, 0], [0, 1, 0], [1, 0, 0], [0, 0, 0], [0, 0, 1]],
#         [[0, 1, 0], [0, 1, 0], [0, 0, 0], [1, 0, 0], [0, 0, 0], [0, 1, 0], [0, 0, 0]],
#         [[0, 0, 1], [0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 0], [1, 0, 0], [0, 0, 0]],
#         [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 0]],
#     ]

#     # Creates the model.
#     model = cp_model.CpModel()

#     # Creates shift variables.
#     # shifts[(n, d, s)]: nurse 'n' works shift 's' on day 'd'.
#     shifts = {}
#     for n in all_nurses:
#         for d in all_days:
#             for s in all_shifts:
#                 shifts[(n, d, s)] = model.NewBoolVar(f"shift_n{n}_d{d}_s{s}")

#     # Each shift is assigned to exactly one nurse in .
#     for d in all_days:
#         for s in all_shifts:
#             model.AddExactlyOne(shifts[(n, d, s)] for n in all_nurses)

#     # Each nurse works at most one shift per day.
#     for n in all_nurses:
#         for d in all_days:
#             model.AddAtMostOne(shifts[(n, d, s)] for s in all_shifts)

#     # Try to distribute the shifts evenly, so that each nurse works
#     # min_shifts_per_nurse shifts. If this is not possible, because the total
#     # number of shifts is not divisible by the number of nurses, some nurses will
#     # be assigned one more shift.
#     min_shifts_per_nurse = (num_shifts * num_days) // num_nurses
#     if num_shifts * num_days % num_nurses == 0:
#         max_shifts_per_nurse = min_shifts_per_nurse
#     else:
#         max_shifts_per_nurse = min_shifts_per_nurse + 1
#     for n in all_nurses:
#         num_shifts_worked = 0
#         for d in all_days:
#             for s in all_shifts:
#                 num_shifts_worked += shifts[(n, d, s)]
#         model.Add(min_shifts_per_nurse <= num_shifts_worked)
#         model.Add(num_shifts_worked <= max_shifts_per_nurse)

#     print(sum(
#             shift_requests[n][d][s] * shifts[(n, d, s)]
#             for n in all_nurses
#             for d in all_days
#             for s in all_shifts
#         ))

#     # pylint: disable=g-complex-comprehension
#     sumx = sum(
#             shift_requests[n][d][s] * shifts[(n, d, s)]
#             for n in all_nurses
#             for d in all_days
#             for s in all_shifts
#         )
#     print(solver.Value(shifts[(n, d, s)]))
#     model.Maximize(
#         sumx
#     )

#     # Creates the solver and solve.
#     solver = cp_model.CpSolver()
#     status = solver.Solve(model)

#     if status == cp_model.OPTIMAL:
#         print("Solution:")
#         for d in all_days:
#             print("Day", d)
#             for n in all_nurses:
#                 for s in all_shifts:
#                     if solver.Value(shifts[(n, d, s)]) == 1:
#                         if shift_requests[n][d][s] == 1:
#                             print("Nurse", n, "works shift", s, "(requested).")
#                         else:
#                             print("Nurse", n, "works shift", s, "(not requested).")
#             print()
#         print(
#             f"Number of shift requests met = {solver.ObjectiveValue()}",
#             f"(out of {num_nurses * min_shifts_per_nurse})",
#         )
#     else:
#         print("No optimal solution found !")

#     # Statistics.
#     print("\nStatistics")
#     print(f"  - conflicts: {solver.NumConflicts()}")
#     print(f"  - branches : {solver.NumBranches()}")
#     print(f"  - wall time: {solver.WallTime()}s")


# if __name__ == "__main__":
#     main()

# print(len([1, 2, 3]))

# dict = {1, 2, 3}

# data = {'S1': {'name': 'Alice'}, 'S2': {'name': 'Wonderland'}}

# print(data['S1']['name'])

# for d in  {'S1': {'name': 'Alice'}, 'S2': {'name': 'Wonderland'}}:
#     print(d['name'])


# print( {'name': 'Alice', 'age': 30})





# Ans

# S1
# |    | T1    |
# |:---|:------|
# | D1 | P1-C2 |
# | D2 | P1-C2 |
# | D3 | P1-C2 |
# S2
# |    | T1    |
# |:---|:------|
# | D1 | P1-C2 |
# | D2 | P1-C2 |
# | D3 | P1-C2 |

# with open('data/studios.csv', 'r') as csv_file:
#     data = csv.DictReader(csv_file)
#     studios = {}
#     for s in data:
#         studios[s['id']] = {'name': s['name']}
#     print(studios)

studios = set()
# print(studios)
for s in [4, 5, 6]:
    studios.add(s)

print(studios)