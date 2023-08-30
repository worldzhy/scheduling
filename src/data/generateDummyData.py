import pandas as pd
import numpy as np

np.random.seed(42)  # For reproducibility

# Generate random test data
num_samples = 100000
days = ['d1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7']
programs = [f'p{i}' for i in range(101, 108)]
coaches = [f'c{i}' for i in range(201, 208)]
studios = [f's{i}' for i in range(1, 8)]
timeslots = [f't{i}' for i in range(301, 308)]
capacities = np.random.randint(20, 100, num_samples)

random_data = {
    'studio': np.random.choice(studios, num_samples),
    'day': np.random.choice(days, num_samples),
    'program': np.random.choice(programs, num_samples),
    'coach': np.random.choice(coaches, num_samples),
    'timeslot': np.random.choice(timeslots, num_samples),
    'capacity': capacities
}

# Create a DataFrame
test_data_df = pd.DataFrame(random_data)

# Save the random test data to a CSV file
test_data_df.to_csv('data/capacity.csv', index=False)
