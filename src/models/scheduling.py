import pandas as pd
import pyomo.environ as pe
import pyomo.opt as po
import csv

## Define Data
def getSetFromPath(path):
    data = set()
    with open(path, 'r') as csv_file:
        res = csv.DictReader(csv_file)
        for r in res:
            data.add(r['id'])
        return data

studios = getSetFromPath('data/studios.csv')
timeslots = getSetFromPath('data/timeslots.csv')
days = {'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'}
programs = getSetFromPath('data/programs.csv')
coaches = getSetFromPath('data/coaches.csv')

q = {}
with open('data/constraints.csv', 'r') as csv_file:
    data = csv.DictReader(csv_file)
    # Create qualification dictionary
    for c in coaches:
        for p in programs:
            q[(p, c)] = 0
    for d in data:
        for p in d['programs'].split(','):
            if p in programs:
                q[(p, d['coach'])] = 1

p = {}
for s in studios:
    for t in timeslots:
        for d in days:
            for pr in programs:
                for c in coaches:
                    p[(s, t, d, pr, c)] = 1

# Model
model = pe.ConcreteModel()

# Sets
model.studios = pe.Set(initialize=studios)
model.timeslots = pe.Set(initialize=timeslots)
model.days = pe.Set(initialize=days)
model.programs = pe.Set(initialize=programs)
model.coaches = pe.Set(initialize=coaches)

# Parameters
model.q = pe.Param(model.programs, model.coaches, initialize=q, default=-1000)
model.p = pe.Param(model.studios, model.timeslots, model.days, model.programs, model.coaches, initialize=p, default=-1000)

# Decision variables
model.x = pe.Var(model.studios, model.timeslots, model.days, model.programs, model.coaches, domain=pe.Boolean)

# Objective function
expr = sum(model.p[s, t, d, p, c] * model.x[s, t, d, p, c]
        for s in model.studios 
        for t in model.timeslots
        for d in model.days
        for p in model.programs
        for c in model.coaches)
model.objective = pe.Objective(sense=pe.maximize, expr=expr)

# Constraint 1: Concurrency
model.concurrency = pe.ConstraintList()
for s in model.studios:
    for t in model.timeslots:
        for d in model.days:
            lhs = sum(model.x[s, t, d, p, c] for p in model.programs for c in model.coaches)
            rhs = 1
            model.concurrency.add(lhs == rhs)

# Constraint 2: Coach Qualification
model.coach_qualifications = pe.ConstraintList()
for p in model.programs:
    for c in model.coaches:
        if (q[p, c] == 0):
            lhs = sum(model.x[s, t, d, p, c] for s in model.studios for t in model.timeslots for d in model.days)
            rhs = 0
            model.coach_qualifications.add(lhs == rhs)

# Execute solver
solver = po.SolverFactory('glpk', executable='/opt/homebrew/bin/glpsol')
results = solver.solve(model)

# Extract results
df = pd.DataFrame(index=pd.MultiIndex.from_tuples(model.x, names=['s', 't', 'd', 'p', 'c']))
df['x'] = [pe.value(model.x[key]) for key in df.index]
df['p'] = [model.p[key] for key in df.index]

# Print schedule of each studio (day by timeslot)
for studio in studios:
    d_by_t = pd.DataFrame.from_dict({d: {t: 'No schedule' for t in timeslots} for d in days}, orient='index')
    for (s, t, d, p, c), values in df.iterrows():
        if studio == s and values.x == 1:
            d_by_t.loc[(d, t)] = f'{p}-{c}'
    print(studio)
    print(d_by_t.to_markdown())
