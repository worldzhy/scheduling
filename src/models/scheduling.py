# Imports
from random import choices, uniform
from typing import Callable, Tuple, List
from algorithms.ga import GeneticAlgorithm
from helpers.helpers import load_data, get_qualifications
from helpers.Type import Genome, Population, Program, Course
from helpers.constants import Constant
import sys

## Data
studios, programs, coaches, days, times = load_data()
qualifications = get_qualifications(programs, coaches)

## Helpers
def get_program_by_id (programId: str) -> Program | None:
    targetProgram: Program | None = None
    for program in programs:
        if program.id == programId:
            targetProgram = program
            break
    return targetProgram

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

def generate_rnd_course():
    if (uniform(0, 1) > 0.2):
        program = choices(programs, k = 1)[0]
        coach = choices(coaches, k = 1)[0]
        day = choices(days, k = 1)[0]
        time = choices(times, k = 1)[0]
        start_time = convert_to_time(time.value)
        end_time = convert_to_time(time.value + program.duration // 5)
        return Course(program, coach, day, time, start_time, end_time)
    else:
        return None

def get_similarity_score(target: int, actual: int):
    absolute_difference = abs(target - actual)
    if absolute_difference == 0:
        return 1.0  
    similarity_score = 1.0 - (absolute_difference / max(target, actual))
    return max(0, similarity_score) 

def count_conflicts(genome: Genome) -> List[int]:
    genome = [g for g in genome if g is not None]
    genome = sorted(genome, key=lambda g: (g.day.value, g.time.value) if g is not None else (0, 0))
    conflicts: List[int] = []
    timeslots: List[List[int]] = [[False for _ in range(Constant.SLOTS_PER_DAY_NUM)] for _ in range(Constant.DAYS_NUM)]
    for idx, course in enumerate(genome):
        if course is not None:
            day = course.day.value
            time = course.time.value
            duration = course.program.duration
            isSkip = False
            for time_specific in range(duration // Constant.RESOLUTION_IN_MINUTES):
                if (time + time_specific >= len(timeslots[day])):
                    isSkip = True
                    break
            if (isSkip == False):
                for time_specific in range(duration // Constant.RESOLUTION_IN_MINUTES):
                    if (timeslots[day][time + time_specific] == True):
                        conflicts.append(idx + 1)
                        break
                    if (timeslots[day][time + time_specific] == False):
                        timeslots[day][time + time_specific] = True
    print(f'Number of conflicts is {len(conflicts)}: ${conflicts}')
    return conflicts

def pipe_to_output(genome: Genome):
    genome = [g for g in genome if g is not None]
    genome = sorted(genome, key=lambda g: (g.day.value, g.time.value) if g is not None else (0, 0))
    with open('output.out', 'w') as f:
        sys.stdout = f
        for g in genome:
            if g is not None:
                print(f'Day {g.day.value + 1} -- {g.start_time} to {g.end_time} -- {g.program.name} -- {g.coach.name}')


# Population function
def populate_func(population_size: int) -> Population:
    population: Population = []
    for _ in range(population_size):
        genome: Genome = []
        for _ in range(Constant.MAX_MONTH_PROGRAM_COUNT):
            genome.append(generate_rnd_course())
        population.append(genome)
    return population

# Fitness function
def fitness_func(genome: Genome) -> float:
    timeslots: List[List[int]] = [[0 for _ in range(Constant.SLOTS_PER_DAY_NUM)] for _ in range(Constant.DAYS_NUM)]
    for course in genome:
        if course is not None:
            day = course.day.value
            time = course.time.value
            duration = course.program.duration
            isSkip = False
            for time_specific in range(duration // Constant.RESOLUTION_IN_MINUTES):
                if (time + time_specific >= len(timeslots[day])):
                    isSkip = True
                    break
            if isSkip == False:
                for time_specific in range(duration // Constant.RESOLUTION_IN_MINUTES):
                    timeslots[day][time + time_specific] += 1
    sum = 0
    for day in timeslots:
        for freq in day:
            if (freq == 0):
                sum += 0
            if (freq == 1):
                sum += 10
            else: 
                sum += -freq
    return sum

# Selection function
def selection_func(population: Population, calc_fitness: Callable[[Genome], float]) -> Tuple[Genome, Genome]:
    custom_weights = [calc_fitness(genome) for genome in population]
    selected = choices(
        population = population,
        weights = custom_weights if sum(custom_weights) > 0 else None,
        k = 2
    )
    return selected[0], selected[1]

# Crossover function
def crossover_func(parents: Tuple[Genome, Genome], num_crossover_points: int) -> Tuple[Genome, Genome]:
    genome1 = parents[0]
    genome2 = parents[1]
    
    # Ensure the number of crossover points does not exceed the genome length
    num_crossover_points = min(num_crossover_points, len(genome1) - 1)
    
    # Generate random crossover points
    crossover_points = sorted(choices(range(1, len(genome1)), k = num_crossover_points))

    # Initialize lists to store offspring genomes
    offspring1: Genome = []
    offspring2: Genome = []
    
    # Iterate through the crossover points and alternate between parents
    current_parent = 1
    for i in range(len(genome1)):
        if i in crossover_points:
            current_parent = 1 - current_parent  # Switch to the other parent
        if current_parent == 0:
            offspring1.append(genome1[i])
            offspring2.append(genome2[i])
        else:
            offspring1.append(genome2[i])
            offspring2.append(genome1[i])
    
    return offspring1, offspring2

# # Mutation function
def mutation_func(genome: Genome, mutation_rate: float) -> Genome:
    for i, _ in enumerate(genome):
        if (uniform(0, 1) > mutation_rate):
            genome[i] = generate_rnd_course()
    return genome

# Run model
result = GeneticAlgorithm[Course | None](
    populate_func,
    fitness_func,
    selection_func,
    crossover_func,
    mutation_func
).run(
    mutation_rate=0.4,
    population_size=50,
    max_iteration=1000,
    num_crossover=5
)

count_conflicts(result)
pipe_to_output(result)

