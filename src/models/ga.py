# Imports
from typing import List, Callable, Tuple

# Genome
Genome = List[int]
# Population
Population = List[Genome]
# Creates initial population
PopulateFunc = Callable[[int], Population]
# Calculates the fitness of a genome
FitnessFunc = Callable[[Genome], int]
# Chooses the parents for the next generation
SelectionFunc = Callable[[Population, FitnessFunc], Tuple[Genome, Genome]]
# Generates offsprings from parents
CrossoverFunc = Callable[[Tuple[Genome, Genome]], Tuple[Genome, Genome]]
# Applys mutation to the genome
MutationFunc = Callable[[Genome], Genome]
# Function for printing purposes
PrinterFunc = Callable[[Population, FitnessFunc, int], None]

# Default printing function
def print_stats(population: Population, fitness_func: FitnessFunc, generation_id: int) -> None:
    sorted_population = sorted(population, key=fitness_func, reverse=True)
    avg_fitness = sum([fitness_func(genome) for genome in population]) / len(population)
    best_fitness = fitness_func(sorted_population[0])
    worst_fitness = fitness_func(sorted_population[-1])
    print(f'GENERATION {generation_id}')
    print("=================")
    print(f'Avg. Fitness: {avg_fitness}')
    print(f'Best. Fitness: {best_fitness}')
    print(f'Worst. Fitness: {worst_fitness}')
    print("")

# Genetic Algorithm Model
def run_ga(
    populate_func: PopulateFunc,
    fitness_func: FitnessFunc,
    selection_func: SelectionFunc,
    crossover_func: CrossoverFunc,
    mutation_func: MutationFunc,
    printer_func: PrinterFunc = print_stats,
    max_fitness: int = 1000000,
    max_iteration: int = 1000,
    population_size: int = 10
):
    population: Population = populate_func(population_size)
    for i in range(max_iteration):
        printer_func(population, fitness_func, i)
        population = sorted(
            population,
            key=lambda genome: fitness_func(genome),
            reverse=True
        )
        if fitness_func(population[0]) >= max_fitness:
            break
        next_generation = population[0:2]
        for _ in range(int(population_size / 2 ) - 1):
            parents = selection_func(population, fitness_func)
            offspring_a, offspring_b = crossover_func(parents)
            offspring_a = mutation_func(offspring_a)
            offspring_b = mutation_func(offspring_b)
            next_generation += [offspring_a, offspring_b]
        population = next_generation