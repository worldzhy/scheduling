# Imports
from random import choices
from typing import Tuple, List
from ..entities.Data import Data
from ..entities.Constant import Constant
from ..entities.Course import Course
from ..entities.Schedule import Schedule

class GeneticAlgorithm():
    def __init__(self, data: Data):
        # initialize data
        self._data = data
        self._data.load()
        # current population sorted by fitness in descending order
        self._population: List[Schedule] = []
        # parameters
        self._max_fitness: int = 1000000
        self._max_iteration: int = 1000
        self._population_size: int = 10 
        self._mutation_rate: float = 0.3 
        self._num_crossover_points: int = 2
    
    # generate random population of size _population_size
    def populate_func(self) -> None:
        for _ in range(self._population_size):
            self._population.append(
                Schedule(
                    [self._data.get_rnd_course() for _ in range(Constant.MAX_MONTH_PROGRAM_COUNT)]
                )
            )
        self._sort_population()

    # randomly select parents from the current population, favor those who have higher fitness
    def selection_func(self) -> Tuple[Schedule, Schedule]:
        custom_weights = [s.get_value() for s in self._population]
        selected = choices(
            population = self._population,
            weights = custom_weights if sum(custom_weights) > 0 else None,
            k = 2
        )
        return selected[0], selected[1]

    # generate two offsprings from parents
    def crossover_func(self, parents: Tuple[Schedule, Schedule]) -> Tuple[Schedule, Schedule]:
        parent_a = parents[0].list
        parent_b = parents[1].list
        # generate random crossover points
        crossover_points = sorted(
            choices(range(1, len(parent_a)),
            k = min(self._num_crossover_points, len(parent_a) - 1))
        )
        # initialize offsprings
        offspring_1: List[Course | None] = []
        offspring_2: List[Course | None] = []
        # populate offsprings
        current_parent = 1
        for i in range(len(parent_a)):
            if i in crossover_points:
                # switch to the other parent
                current_parent = 1 - current_parent 
            if current_parent == 0:
                offspring_1.append(parent_a[i])
                offspring_2.append(parent_b[i])
            else:
                offspring_1.append(parent_b[i])
                offspring_2.append(parent_a[i])
        return Schedule(offspring_1), Schedule(offspring_2)
    
    # configure parameters of the algorithm
    def configure(
        self,
        max_fitness: None | int = None,
        max_iteration: None | int = None,
        population_size: None | int = None,
        mutation_rate: None | float = None,
        num_crossover_points: None | int = None
    ) -> None:
        self._max_fitness = max_fitness if max_fitness is not None else self._max_fitness
        self._max_iteration = max_iteration if max_iteration is not None else self._max_iteration
        self._population_size = population_size if population_size is not None else self._population_size 
        self._mutation_rate = mutation_rate if mutation_rate is not None else self._mutation_rate
        self._num_crossover_points = num_crossover_points if num_crossover_points is not None else self._num_crossover_points

    # printer function
    def _printer_default(self, population: List[Schedule], generation_id: int) -> None:
        sorted_population = sorted(population, key=lambda s: s.get_value(), reverse=True)
        avg_fitness = sum([genome.get_value() for genome in population]) / len(population)
        best_fitness = sorted_population[0].get_value()
        worst_fitness = sorted_population[-1].get_value()
        print(f'GENERATION {generation_id}')
        print("=================")
        print(f'Avg. Fitness: {avg_fitness}')
        print(f'Best. Fitness: {best_fitness}, conflicts: {len(sorted_population[0].get_conflicts())}')
        print(f'Worst. Fitness: {worst_fitness}')
        print("")

    def _sort_population(self) -> None:
        self._population = sorted(
            self._population,
            key=lambda s: s.get_value(),
            reverse=True
        )

    # run algorithm
    def run(self) -> None:
        self.populate_func()
        for i in range(self._max_iteration):
            # print current population
            self._printer_default(self._population, i)
            # exit if max fitness is achieved
            if self._population[0].get_value() >= self._max_fitness:
                break
            # auto carryover two best schedules to next generation
            next_generation = self._population[0:2]
            # populate next generation
            for _ in range(int(self._population_size / 2 ) - 1):
                parents = self.selection_func()
                offspring_a, offspring_b = self.crossover_func(parents)
                offspring_a.mutate(self._data.get_rnd_course)
                offspring_b.mutate(self._data.get_rnd_course)
                next_generation += [offspring_a, offspring_b]
            self._population = next_generation
            self._sort_population()
        # get best schedule and save output
        self._population[0].save_to_file()