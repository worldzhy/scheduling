# Imports
from random import choices
import sys
from typing import Tuple, List
from ..entities.Data import Data
from ..entities.Constant import Constant
from ..entities.Course import Course
from ..entities.Schedule import Schedule

class GeneticAlgorithm():
    def __init__(self, data: Data):
        # Initialize data
        self.data = data
        self.data.load()
        # Current population
        self.population: List[Schedule] = []
    
    def populate_func(self, population_size: int):
        for _ in range(population_size):
            self.population.append(
                Schedule(
                    [self.data.get_rnd_course() for _ in range(Constant.MAX_MONTH_PROGRAM_COUNT)]
                )
            )

    def selection_func(self):
        custom_weights = [genome.get_value() for genome in self.population]
        selected = choices(
            population = self.population,
            weights = custom_weights if sum(custom_weights) > 0 else None,
            k = 2
        )
        return selected[0], selected[1]

    def crossover_func(self, parents: Tuple[Schedule, Schedule], num_crossover_points: int):
        genome1 = parents[0].list
        genome2 = parents[1].list
        # Ensure the number of crossover points does not exceed the genome length
        num_crossover_points = min(num_crossover_points, len(genome1) - 1)
        # Generate random crossover points
        crossover_points = sorted(choices(range(1, len(genome1)), k = num_crossover_points))
        # Initialize lists to store offspring genomes
        offspring1: List[Course | None] = []
        offspring2: List[Course | None] = []
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
        return Schedule(offspring1), Schedule(offspring2)

    def mutation_func(self, schedule: Schedule):
        return schedule.mutate(self.data.get_rnd_course)
    
    def run(
        self,
        max_fitness: int = 1000000,
        max_iteration: int = 1000,
        population_size: int = 10, 
        mutation_rate: float = 0.3, 
        num_crossover: int = 2
    ) -> None:
        self.populate_func(population_size)
        for i in range(max_iteration):
            self._printer_default(self.population, i)
            population = sorted(
                self.population,
                key=lambda g: g.get_value(),
                reverse=True
            )
            if population[0].get_value() >= max_fitness:
                break
            next_generation = population[0:2]
            for _ in range(int(population_size / 2 ) - 1):
                parents = self.selection_func()
                offspring_a, offspring_b = self.crossover_func(parents, num_crossover)
                offspring_a = self.mutation_func(offspring_a)
                offspring_b = self.mutation_func(offspring_b)
                next_generation += [offspring_a, offspring_b]
            population = next_generation
        best = sorted(
            self.population,
            key=lambda genome: genome.get_value(),
            reverse=True
        )[0]
        best.get_conflicts()
        self.pipe_to_output(best)

    def _printer_default(self, population: List[Schedule], generation_id: int) -> None:
        sorted_population = sorted(population, key=lambda g: g.get_value(), reverse=True)
        avg_fitness = sum([genome.get_value() for genome in population]) / len(population)
        best_fitness = sorted_population[0].get_value()
        worst_fitness = sorted_population[-1].get_value()
        print(f'GENERATION {generation_id}')
        print("=================")
        print(f'Avg. Fitness: {avg_fitness}')
        print(f'Best. Fitness: {best_fitness}')
        print(f'Worst. Fitness: {worst_fitness}')
        print("")

    def pipe_to_output(self, genome: Schedule):
        schedule = [g for g in genome.list if g is not None]
        schedule = sorted(schedule, key=lambda g: (g.day.value, g.time.value))
        with open('output.out', 'w') as f:
            sys.stdout = f
            for g in schedule:
                print(f'Day {g.day.value + 1} -- {g.time.clock_start} to {g.time.clock_end} -- {g.program.name} -- {g.coach.name}')