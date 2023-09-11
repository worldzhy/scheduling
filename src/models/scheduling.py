# Imports
from random import choices, uniform, randint
from typing import Callable, Tuple
from algorithms.ga import GeneticAlgorithm
from helpers.helpers import load_data, get_qualifications
from helpers.Type import Genome, Population, Program, Course
from helpers.constants import Constant

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

def generate_rnd_course():
    if (uniform(0, 1) > 0.2):
        program = choices(programs, k = 1)[0]
        coach = choices(coaches, k = 1)[0]
        day = choices(days, k = 1)[0]
        time = choices(times, k = 1)[0]
        return Course(program, coach, day, time)
    else:
        return None

def get_similarity_score(target: int, actual: int):
    absolute_difference = abs(target - actual)
    if absolute_difference == 0:
        return 1.0  
    similarity_score = 1.0 - (absolute_difference / max(target, actual))
    return max(0, similarity_score) 

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
    timeslots = [[False for _ in range(Constant.SLOTS_PER_DAY_NUM)] for _ in range(Constant.DAYS_NUM)]
    value = 0
    for course in genome:
        if course is not None:
            day = course.day.value
            time = course.time.value
            duration = course.program.duration
            for time_specific in range(duration // Constant.RESOLUTION_IN_MINUTES):
                if (time + time_specific >= len(timeslots[day])):
                    value = value - 2
                elif timeslots[day][time + time_specific] == False:
                    value = value + 1
                else:
                    value = value - 2
                    timeslots[day][time + time_specific] = True
    return value + Constant.FITNESS_ADJ

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
def crossover_func(parents: Tuple[Genome, Genome]) -> Tuple[Genome, Genome]:
    genome1 = parents[0]
    genome2 = parents[1]
    point = randint(0, len(genome1))
    genome1A = genome1[:point]
    genome1B = genome1[point:]
    genome2A = genome2[:point]
    genome2B = genome2[point:]
    return genome1A + genome2B, genome1B + genome2A

# # Mutation function
def mutation_func(genome: Genome, mutation_rate: float) -> Genome:
    for i, _ in enumerate(genome):
        if (uniform(0, 1) > mutation_rate):
            genome[i] = generate_rnd_course()
    return genome

# Run model
GeneticAlgorithm[Course | None](
    populate_func,
    fitness_func,
    selection_func,
    crossover_func,
    mutation_func
).run(mutation_rate=0.4, population_size=40)