# Imports
from random import choices, uniform, randint
from typing import Callable, List, Tuple, NamedTuple
from algorithms.ga import GeneticAlgorithm
# from helpers import load_data

# Load data
# studios, programs, coaches, days = load_data()
class Thing(NamedTuple):
        name: str
        value: int
        weight: int

items = [
    Thing('Laptop', 500, 2200),
    Thing('Headphones', 150, 160),
    Thing('Water Bottle', 30, 192),
    Thing('Mints', 5, 25),
    Thing('Socks', 10, 38),
    Thing('Tissues', 15, 80),
    Thing('Phone', 500, 200),
    Thing('Baseball Cap', 100, 70),
    Thing('Coffee Mug', 60, 350),
    Thing('Notepad', 40, 333),
]

Genome = List[int]
Population = List[Genome]
FitnessFunc = Callable[[Genome], int]
    
# A function to generate new solution
def populate_func(population_size: int) -> Population:
    return [choices([0, 1], k = len(items)) for _ in range(population_size)]

# Fitness function
def fitness_func(genome: Genome) -> int:
    value = 0
    weight = 0
    for index, item in enumerate(items):
        value = value + item.value * genome[index]
        weight = weight + item.weight * genome[index]
        if weight > 3000:
            return 0
    return value

# Selection function
def selection_func(population: Population, calc_fitness:  FitnessFunc) -> Tuple[Genome, Genome]:
    selected = choices(
        population=population,
        weights=[calc_fitness(genome) for genome in population],
        k=2
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
    for index, gen in enumerate(genome):
        if (uniform(0, 1) > 0.3):
            genome[index] = abs(gen - 1)
    return genome

# Run model

GeneticAlgorithm[int](
    populate_func,
    fitness_func,
    selection_func,
    crossover_func,
    mutation_func).run()