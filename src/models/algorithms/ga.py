# Imports
from typing import Generic, List, Callable, Tuple, TypeVar, Union

T = TypeVar('T') 
class GeneticAlgorithm(Generic[T]):
    def __init__(
        self,
        populate_func: Callable[[int], List[List[T]]],
        fitness_func: Callable[[List[T]], float],
        selection_func: Callable[[List[List[T]], Callable[[List[T]], float]], Tuple[List[T], List[T]]],
        crossover_func: Callable[[Tuple[List[T], List[T]]], Tuple[List[T], List[T]]],
        mutation_func: Callable[[List[T], float], List[T]],
        printer_func: Union[Callable[[List[List[T]], Callable[[List[T]], float], int], None], None] = None,
    ):
        self._populate_func = populate_func
        self._fitness_func = fitness_func
        self._selection_func = selection_func
        self._crossover_func = crossover_func
        self._mutation_func = mutation_func
        self._printer_func = printer_func

    def run(self, max_fitness: int = 1000000, max_iteration: int = 1000, population_size: int = 10, mutation_rate: float = 0.3):
        population: List[List[T]] = self._populate_func(population_size)
        for i in range(max_iteration):
            if (self._printer_func is not None):
                self._printer_func(population, self._fitness_func, i)
            else:
                self._printer_default(population, self._fitness_func, i)
            population = sorted(
                population,
                key=lambda genome: self._fitness_func(genome),
                reverse=True
            )
            if self._fitness_func(population[0]) >= max_fitness:
                break
            next_generation = population[0:2]
            for _ in range(int(population_size / 2 ) - 1):
                parents = self._selection_func(population, self._fitness_func)
                offspring_a, offspring_b = self._crossover_func(parents)
                offspring_a = self._mutation_func(offspring_a, mutation_rate)
                offspring_b = self._mutation_func(offspring_b, mutation_rate)
                next_generation += [offspring_a, offspring_b]
            population = next_generation

    def _printer_default(self, population: List[List[T]], fitness_func: Callable[[List[T]], float], generation_id: int) -> None:
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








