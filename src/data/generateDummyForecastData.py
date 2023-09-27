from typing import List
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

np.random.seed(42)  # For reproducibility

# Generate 2022 dates
start_date = datetime(2022, 1, 1)
end_date = datetime(2022, 12, 31)
date_list: List[datetime] = []
current_date = start_date
while current_date <= end_date:
    date_list.append(current_date)
    current_date += timedelta(days=1)

# Lists
program_list = ['p1', 'p2', 'p3', 'p4']
coach_list = ['c1', 'c2', 'c3', 'c4']
studio_list = ['s1', 's2', 's3', 's4']

# Generate capacities
capacities = [(i ** 2 + 2 * i + 1) for i in range(len(date_list))]
programs = np.random.choice(program_list, len(date_list))
coaches = np.random.choice(coach_list, len(date_list))
studios = np.random.choice(studio_list, len(date_list))

random_data = {
    'date': date_list,
    'capacity': capacities,
    'program': programs,
    'coach': coaches,
    'studio': studios
}

# Create a DataFrame
test_data_df = pd.DataFrame(random_data)

# Save the random test data to a CSV file
test_data_df.to_csv('data/processed/forecast.csv', index=False)
