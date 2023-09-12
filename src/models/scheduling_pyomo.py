from typing import List, NamedTuple, cast
import pandas as pd
import pyomo.environ as pe
import pyomo.opt as po
import csv
import sys

class Course(NamedTuple):
    studio: str
    program: str
    coach: str
    day: str
    time: str
    start_time: str
    # end_time: str

## Define Data
def get_set(set_name):
    """
    Constructs set for studios, timeslots, days, programs, and coach.

    Parameters:
    :param set_name: Target set name

    Returns:
    :return: The target sets populated with the correct values.
    """
    if set_name == 'days':
        return {'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'}
    else: 
        ret = set()
        with open(f'data/processed/{set_name}.csv', 'r') as csv_file:
            data = csv.DictReader(csv_file)
            for row in data:
                ret.add(row['id'])
            return ret

def get_qualification(programs, coaches):
    """
    Constructs a dictionary of coach qualifications.

    Parameters:
    :param programs: Set of programs
    :param coaches: Set of coaches

    Returns:
    :return: Dictionary indexed by program and coach, with values of 1 for qualified coaches and 0 for unqualified ones.
    """
    ret = {}
    with open('data/processed/constraints.csv', 'r') as csv_file:
        data = csv.DictReader(csv_file)
        for c in coaches:
            for p in programs:
                ret[(p, c)] = 0
        for row in data:
            for p in row['programs'].split(','):
                if p in programs:
                    ret[(p, row['coach'])] = 1
    return ret

def get_profit(studios, timeslots, days, programs, coaches):
    """
    Constructs a dictionary of projected profit for each possible combination of studio, timeslot, day, program, and coaches.

    Parameters:
    :param studios: Set of studios
    :param timeslots: Set of timeslots
    :param days: Set of days
    :param programs: Set of programs
    :param coaches: Set of coaches

    Returns:
    :return: Dictionary indexed by studios, timeslots, days, programs, and coach, with the value representing the projected profit.
    """
    ret = {}
    for s in studios:
        for t in timeslots:
            for d in days:
                for p in programs:
                    for c in coaches:
                        ret[(s, t, d, p, c)] = 1
    return ret

def get_objective_function(model):
    """
    Constructs the objective function expression to be used on the model.

    Parameters:
    :param model: The model instance

    Returns:
    :return: The objective function expression.
    """
    ret = sum(model.p[s, t, d, p, c] * model.x[s, t, d, p, c]
            for s in model.studios 
            for t in model.timeslots
            for d in model.days
            for p in model.programs
            for c in model.coaches)
    return ret

def add_constraint_concurrency(model):
    """
    Adds class concurrency constraint. Only one program can be scheduled per studio, timeslot, and day, each taught by a single coach.
    
    Parameters:
    :param model: The model instance

    Returns:
    :return: None
    """
    model.concurrency = pe.ConstraintList()
    for s in model.studios:
        for t in model.timeslots:
            for d in model.days:
                lhs = sum(model.x[s, t, d, p, c] for p in model.programs for c in model.coaches)
                rhs = 1
                model.concurrency.add(lhs <= rhs)

def add_constraint_coach_qualifications(model):
    """
    Adds coach qualification constraints. If a coach is unqualified to teach a program, they cannot be assigned to that program.

    Parameters:
    :param model: The model instance

    Returns:
    :return: None
    """
    model.coach_qualifications = pe.ConstraintList()
    for p in model.programs:
        for c in model.coaches:
            if (model.q[p, c] == 0):
                lhs = sum(model.x[s, t, d, p, c] for s in model.studios for t in model.timeslots for d in model.days)
                rhs = 0
                model.coach_qualifications.add(lhs == rhs)

# def add_constraint_program_duration(model):
#     """
#     Adds coach qualification constraints. If a coach is unqualified to teach a program, they cannot be assigned to that program.

#     Parameters:
#     :param model: The model instance

#     Returns:
#     :return: None
#     """
#     model.coach_qualifications = pe.ConstraintList()
#     for p in model.programs:
#         for c in model.coaches:
#             if (model.q[p, c] == 0):
#                 lhs = sum(model.x[s, t, d, p, c] for s in model.studios for t in model.timeslots for d in model.days)
#                 rhs = 0
#                 model.coach_qualifications.add(lhs == rhs)

def convert_to_time(input_value: int):
    if 0 <= input_value <= 203:
        hours = 5 + input_value // 12
        minutes = (input_value % 12) * 5
        period = "AM" if hours < 12 else "PM"
        if hours == 12:
            period = "PM"
        if hours > 12:
            hours -= 12
        return f"{hours:02d}:{minutes:02d} {period}"
    else:
        return "Invalid input"

def model_to_array(model) -> List[Course]:
    res: List[Course] = []
    # Extract results
    df = pd.DataFrame(index=pd.MultiIndex.from_tuples(model.x, names=['s', 't', 'd', 'p', 'c']))
    df['x'] = [pe.value(model.x[key]) for key in df.index]
    df['p'] = [model.p[key] for key in df.index]

    for (s, t, d, p, c), values in df.iterrows():
        if (values.x == 1):
            res.append(Course(cast(str, s), cast(str, p), cast(str, c), cast(str, d), cast(str, t), convert_to_time(int(cast(str, t[1:])))))
    return res

class AggregateCourse(NamedTuple):
    studio: str
    program: str
    coach: str
    day: str
    time_start: str
    time_end: str

def create_end_times(course: List[Course]) -> List[AggregateCourse]:
    aggregate_course: List[AggregateCourse] = []
    
    course = sorted(course, key=lambda g: (g.studio, g.day, int(g.time[1:])))
    def transform(c: Course):
        return AggregateCourse(c.studio, c.program, c.coach, c.day, c.time, c.time)
    courses_agg = list(map(transform, course))

    current_aggregate = courses_agg[0]

    for next_course in courses_agg[1:]:
        print(current_aggregate.time_start[1:], next_course.time_start[1:])
        if (
            current_aggregate.studio == next_course.studio and
            current_aggregate.program == next_course.program and
            current_aggregate.coach == next_course.coach and
            current_aggregate.day == next_course.day and
            int(current_aggregate.time_end[1:]) + 1 == int(next_course.time_start[1:])
        ):
            current_aggregate = current_aggregate._replace(time_end=next_course.time_start)
        else:
            aggregate_course.append(current_aggregate)
            current_aggregate = next_course

    aggregate_course.append(current_aggregate)
    
    return aggregate_course

def pipe_to_output(course: List[AggregateCourse]):
    course = sorted(course, key=lambda g: (g.studio, g.day, int(g.time_start[1:])))
    with open('output.out', 'w') as f:
        sys.stdout = f
        for g in course:
            print(f'Studio {g.studio} Day {g.day} -- {g.time_start} to {g.time_end} -- {g.program} -- {g.coach}')

def print_results(model):
    """
    Prints the optimal solution found by the model. For each studio, it prints a timeslot by days table where each value is 'No schedule' if nothing is scheduled or {program}-{coach} to say that coach is scheduled to teach program.

    Parameters:
    :param model: The model instance
    :param studios: Set of studios
    :param timeslots: Set of timeslots
    :param days: Set of days

    Returns:
    :return: None
    """
    # Extract results
    # df = pd.DataFrame(index=pd.MultiIndex.from_tuples(model.x, names=['s', 't', 'd', 'p', 'c']))
    # df['x'] = [pe.value(model.x[key]) for key in df.index]
    # df['p'] = [model.p[key] for key in df.index]

    # TO DO: Print should be ascending order
    # Print schedule of each studio (timeslot by day)
    # for studio in model.studios:
    #     t_by_d = pd.DataFrame.from_dict({t: {d: 'No schedule' for d in model.days} for t in model.timeslots}, orient='index')
    #     for (s, t, d, p, c), values in df.iterrows():
    #         if s == studio and values.x == 1:
    #             t_by_d.loc[(t, d)] = f'{p}-{c}'
        # Create a list of all 't' values from 't1' to 't204'
        # all_t_values = [f't{i}' for i in range(1, 205)]
        # Reindex the DataFrame with all 't' values
        # t_by_d = t_by_d.reindex(all_t_values, fill_value='')
        # print(studio)
        # print(t_by_d.to_markdown())
    pipe_to_output(create_end_times((model_to_array(model))))


def main():
    # Get sets
    studios = get_set('studios')
    timeslots = get_set('timeslots')
    days = get_set('days')
    programs = get_set('programs')
    coaches = get_set('coaches')

    # Get parameters
    q = get_qualification(programs, coaches)
    p = get_profit(studios, timeslots, days, programs, coaches)

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
    expr = get_objective_function(model)
    model.objective = pe.Objective(sense=pe.maximize, expr=expr)

    # Constraints
    add_constraint_concurrency(model)
    add_constraint_coach_qualifications(model)

    # Execute solver
    solver = po.SolverFactory('glpk', executable='/opt/homebrew/bin/glpsol')
    solver.solve(model)

    # Print solution
    print_results(model)

main()