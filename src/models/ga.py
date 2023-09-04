# Imports
from random import choices, uniform, randint
from collections import namedtuple

# Define items
Thing = namedtuple('Thing', ['name', 'value', 'weight'])
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

# Genetic representation of solution
def generate_genome():
    return choices([0, 1], k = len(items))
    
# A function to generate new solution
def generate_population(pop_size):
    return [generate_genome() for _ in range(pop_size)]

# Fitness function
def calculate_fitness(genome):
    value = 0
    weight = 0
    for index, item in enumerate(items):
        value = value + item.value * genome[index]
        weight = weight + item.weight * genome[index]
        if weight > 3000:
            return 0
    return value

# Selection function
def selection(population):
    return choices(
        population=population,
        weights=[calculate_fitness(genome) for genome in population],
        k=2
    )

# Crossover function
def crossover(parents):
    genome1 = parents[0]
    genome2 = parents[1]
    point = randint(0, len(genome1))
    genome1A = genome1[:point]
    genome1B = genome1[point:]
    genome2A = genome2[:point]
    genome2B = genome2[point:]
    return genome1A + genome2B, genome1B + genome2A


# Mutation function
def mutation(genome):
    for index, gen in enumerate(genome):
        if (uniform(0, 1) > 0.3):
            genome[index] = abs(gen - 1)
    return genome

# Elitism
def get_elites(pop, k=2):
    return sorted(
        pop,
        key=lambda genome: calculate_fitness(genome),
        reverse=True
    )[:k]

def main():
    # Parameters
    NUM_ITER = 1000
    POPULATION_NUM = 10

    # Initialize
    population = generate_population(POPULATION_NUM)

    # Run
    for iter in range(NUM_ITER):
        ### Print
        best = get_elites(population, 1)
        print(f'Iteration #: {iter} (fitness: {calculate_fitness(best[0])})')

        ### Begin next iteration
        # Prepare to generate population
        current_population = []
        # Add elites in population
        current_population += get_elites(population)
        # Select parents
        parents = selection(population)
        # Perform crossover
        for _ in range(int(POPULATION_NUM / 2 ) - 1):
            a, b = crossover(parents)
            a = mutation(a)
            b = mutation(b)
            current_population += [a, b]
        # Replace old population
        population = current_population

    best = get_elites(population, 1)
    total_w = 0
    total_v = 0
    for index,item in enumerate(best[0]):
        if item == 1:
            print(items[index].name)
            total_w = total_w + items[index].weight
            total_v = total_v + items[index].value
    print(f'weight: {total_w}; value: {total_v}; fitness: {calculate_fitness(best[0])}')
main()
