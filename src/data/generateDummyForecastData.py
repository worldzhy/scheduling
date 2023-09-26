from typing import List
import pandas as pd
from datetime import datetime, timedelta

# Generate 2022 dates
start_date = datetime(2022, 1, 1)
end_date = datetime(2022, 12, 31)
date_list: List[datetime] = []
current_date = start_date
while current_date <= end_date:
    date_list.append(current_date)
    current_date += timedelta(days=1)

# Generate capacities
capacities = [(i ** 2 + 2 * i + 1) for i in range(len(date_list))]

random_data = {
    'date': date_list,
    'capacity': capacities
}

# Create a DataFrame
test_data_df = pd.DataFrame(random_data)

# Save the random test data to a CSV file
test_data_df.to_csv('data/processed/forecast.csv', index=False)
