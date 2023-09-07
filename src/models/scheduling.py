# Imports
from random import choices, uniform, randint
from typing import Any, Callable, Tuple, cast
from algorithms.ga import GeneticAlgorithm
from helpers.helpers import load_data, get_choices, get_qualifications
from helpers.types import Genome, Population, Class
from helpers.constants import Constant

## Data
studios, programs, coaches, days = load_data()
qualifications = get_qualifications(programs, coaches)
choices_list = get_choices(programs, coaches)

# Population function
def populate_func(population_size: int) -> Population:
    return [choices(cast(Any, choices_list), k = int(Constant.SLOTS_PER_DAY_NUM) * Constant.DAYS_NUM) for _ in range(population_size)]

# Fitness function
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
def selection_func(population: Population, calc_fitness: Callable[[Genome], int]) -> Tuple[Genome, Genome]:
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

# Mutation function
def mutation_func(genome: Genome) -> Genome:
    for i, _ in enumerate(genome):
        if (uniform(0, 1) > 0.2):
            genome[i] = choices(choices_list, k = 1)[0]
    return genome

# Run model
# GeneticAlgorithm[Class](
#     populate_func,
#     fitness_func,
#     selection_func,
#     crossover_func,
#     mutation_func
# ).run()