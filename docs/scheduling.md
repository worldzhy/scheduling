# Scheduling

Given a list of studios, locations, programs, coaches, and data about the coaches’ availability and expertise, the model will try to generate a per-studio schedule that fits some predefined constraints.

## Constraints

- Do not schedule a coach that is not available on the specific time and day
- Do not assign assign a coach that is not qualified to lead a specific program
- A studio can only cater one program on a specific time and day.

## Dataset

Data (in csv) needed are:

- List of locations for the target studio
- List of programs for the target studio
- List of coaches for the target studio, along with their availability and expertise

## Algorithm

### Preprocessing

Series of steps were taken to transform data into a format that the scheduling model requires. The following are sample of the expected data format:

- List of locations for the target studio

  ```
  id,name
  s1,Culver City
  s2,Hollywood
  s3,Pasedena
  ```

- List of programs for the target studio

  ```
  id,name,duration
  p1,fullbody,50
  p2,30minexpress,30
  p3,buns+abs,50
  ```

- List of coaches for the target studio

  ```
  id,name
  c1,Taylor T.
  c2,Cianna P.
  c3,Maya D.
  ```

- Constraints related to coach availability and expertise

  TODO: Change time format

  ```
  coach,studios,programs,monday,tuesday,wednesday,thursday,friday,saturday,sunday
  c1,"s1,s2,s3","p2",t1,t1,t1,t1,t1,t1,t1
  c2,"s1,s2,s3","p2",t1,t1,t1,t1,t1,t1,t1
  c3,"s1,s2,s3",p2,t1,t1,t1,t1,t1,t1,t1
  ```

### Forecasting model

The forecasting model makes use of the [Genetic Algorithm](https://en.wikipedia.org/wiki/Genetic_algorithm) to cater with the complexity of the problem. The scheduling algorithm is composed of the following:

#### A genome

Genome here is described as one feasible solution to the problem. In this case, the solution is the schedule describing what program to schedule on specific time and day with who coach on a given location in a studio. The structure of this genome is an array of [courses](./terminologies.md#course).

Each schedule has a corresponding fitness value which is used to quantify how good the schedule is. This numeric value is also used to decide how much better one schedule is compared to other. The genetic algorithm will try to find the schedule with the highest fitness value.

In this problem, the fitness value is calculated in the basis of the number of conflicts on the schedule. The more courses without conflict is, the higher would be the value.
TODO: Add documentation for fitness value to include coach schedule and expertise.

#### Crossover function

This is a function where given two genomes (i.e. two schedules), it will give two offsprings. The function tries to inherit to their offspring parts of themeselves. In this problem, crossover is done using n-point crossover. Here, the value of `n` is one parameter of the model which is set to two by default.

#### Mutation

This is a function where given one genome, it will randomly try to change one course into a completely different course as long as the timeslot still fits.

#### Parameters

The model has few parameters responsible for tuning it:

- `max_fitness` (int)
  - default value: 1000000
  - The maximum fitness value of the model. If a genome is found with this fitness value, the algorithm will stop and return this genome as the solution.
- `max_iteration` (int)
  - default value: 1000
  - The maximum iteration that the model will perform. If this number of iteration is reached, the algorithm will stop regardless of the fitness value. The genome with the highest fitness value in the current population is returned sa the solution.
- `population_size` (int)
  - default value: 10
  - The size of population per iteration (a.k.a. generation).
- `mutation_rate` (float)
  - default value: 0.3
  - The probability that a course of a schedule will change.
- `num_crossover_points` (int)
  - default value: 2
  - The number of crossover points to include in crossover function.
- `visualize_fitness` (bool)
  - default value: False
  - If true, while algorithm is running, there will be a graph visualizing the average fitness value of the population per iteration. Useful for investigating model performance.
- `debug` (bool)
  - default value: False
  - If true, will enable logging. Useful for investigating model performance and debugging issues.

#### Process

The algorithm runs as follows:

1. Generate intial population where size depends on the value of `population_size`.
2. From the current population, choose two genomes with the highes fitness value. Add these two as members of the next generation of population.
3. Using the two best genomes, use crossover function to produce offspring genomes that will fill the next generation of population until it reaches the size set by the `population_size`.
4. For every offspring, use mutation function to attempt mutation.
5. Replace current population with the nex generation of population and repeat step 2.

These steps will be repeated and it will only stop if one of these two stopping critera is reached:

- The number of iteration exceeds `max_iteration`
- A genome in the current population has a fitness value equal or greater than the `max_fitness`.

### Usage

#### Input

TODO: Change API to accept parameters

- `studio_id`: the id corresponding to a studio
- `location_id`: the id corresponding to a location
- `program_id`: the id corresponding to a program
- `month`: the number of the month (ex: 1 - January, 2 - February, ..., 12 - December)
- `year`: target year

#### Output

TODO: studio should be location and there should be another field for the actual studio

```
[
    {
        "coach": "Maya D.",
        "day": "1",
        "program": "fullbody",
        "studio": "s1"
        "time": {
            "end": "06:15 AM",
            "start": "05:00 AM"
        }
    },
    {
        "coach": "Maya D.",
        "day": "1",
        "program": "fullbody",
        "studio": "s1"
        "time": {
            "end": "07:30 AM",
            "start": "06:15 AM"
        }
    },
    ...,
       {
        "coach": "Taylor T.",
        "day": "30",
        "program": "Full Body (hamstrings & biceps)",
        "studio": "s1",
        "time": {
            "end": "09:10 PM",
            "start": "08:10 PM"
        }
    },
    {
        "coach": "Taylor T.",
        "day": "30",
        "program": "Buns + Abs",
        "studio": "s1",
        "time": {
            "end": "09:50 PM",
            "start": "09:10 PM"
        }
    }
]
```
