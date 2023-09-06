# Imports
from random import choices, uniform, randint
from typing import Any, Tuple, List, cast
from algorithms.ga import run_ga, Genome, Population, FitnessFunc
from helpers.helpers import load_data

## Constants
# Time granularity
RESOLUTION_IN_MINUTES = 5
# Number of working time in minutes (17 hours from 5AM to 10PM)
MINUTES_PER_DAY_NUM = 17 * 60
# Number of slots per day
SLOTS_PER_DAY_NUM = MINUTES_PER_DAY_NUM / RESOLUTION_IN_MINUTES
# Number of days to consider
DAYS_NUM = 30

## Data
studios, programs, coaches, days = load_data()
choices_list: List[str] = []
for p in programs:
    for c in coaches:
        choices_list.append("{}-{}".format(p.id, c.id))

# A function to generate new solution
def populate_func(population_size: int) -> Population:
    return [choices(cast(Any, choices_list), k = int(SLOTS_PER_DAY_NUM) * DAYS_NUM) for _ in range(population_size)]

# # Fitness function
# def fitness_func(genome: Genome) -> int:
#     value = 0
#     weight = 0
#     for index, item in enumerate(items):
#         value = value + item.value * genome[index]
#         weight = weight + item.weight * genome[index]
#         if weight > 3000:
#             return 0
#     return value

# Selection function
def selection_func(population: Population, calc_fitness: FitnessFunc) -> Tuple[Genome, Genome]:
    selected = choices(
        population = population,
        weights = [calc_fitness(genome) for genome in population],
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
def mutation_func(genome: Genome) -> Genome:
    for index, _ in enumerate(genome):
        if (uniform(0, 1) > 0.2):
            genome[index] = choices(choices_list, k = 1)[0]
    return genome

# Run model
run_ga(
    populate_func,
    fitness_func,
    selection_func,
    crossover_func,
    mutation_func,
)
