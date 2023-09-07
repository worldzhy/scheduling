# Imports
from random import choices, uniform, randint
from typing import Any, Callable, Tuple, cast
from algorithms.ga import GeneticAlgorithm
from helpers.helpers import load_data, get_choices, get_qualifications, schedulize
from helpers.Type import Genome, Population, Program, Course
from helpers.constants import Constant

## Data
studios, programs, coaches, days = load_data()
qualifications = get_qualifications(programs, coaches)
choices_list = get_choices(programs, coaches)

## Helpers
def get_program_by_id (programId: str) -> Program | None:
    targetProgram: Program | None = None
    for program in programs:
        if program.id == programId:
            targetProgram = program
            break
    return targetProgram

def get_similarity_score(target: int, actual: int):
    absolute_difference = abs(target - actual)
    if absolute_difference == 0:
        return 1.0  
    similarity_score = 1.0 - (absolute_difference / max(target, actual))
    return max(0, similarity_score) 

# Population function
def populate_func(population_size: int) -> Population:
    return [choices(cast(Any, choices_list), k = int(Constant.SLOTS_PER_DAY_NUM) * Constant.DAYS_NUM) for _ in range(population_size)]

# Fitness function
def fitness_func(genome: Genome) -> float:
    schedule = schedulize(genome, Constant.RESOLUTION_IN_MINUTES)
    value = 0
    for _, course in enumerate(schedule):
        if course.course.programId is not None:
            program = get_program_by_id(course.course.programId)
            if program is not None:
                value = value + get_similarity_score(program.duration, course.duration)
    return value

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

# Mutation function
def mutation_func(genome: Genome, mutation_rate: float) -> Genome:
    for i, _ in enumerate(genome):
        if (uniform(0, 1) > mutation_rate):
            genome[i] = choices(choices_list, k = 1)[0]
    return genome

# Run model
GeneticAlgorithm[Course](
    populate_func,
    fitness_func,
    selection_func,
    crossover_func,
    mutation_func
).run(mutation_rate=0.4, population_size=20)

# print(selection_func(populate_func(5), fitness_func))