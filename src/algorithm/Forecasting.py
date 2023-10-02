# type: ignore
import pandas as pd
from datetime import datetime, timedelta
from prophet import Prophet

def generate_future_dates(start_date, end_date):
    # Generate a list of dates for September 2023
    date_list = []
    current_date = start_date
    while current_date <= end_date:
        date_list.append(pd.to_datetime(current_date.strftime('%Y-%m-%d')))
        current_date += timedelta(days = 1)

    # Create a dictionary with the list of dates
    date_dict = {'ds': date_list}

    # Return the dictionary
    return pd.DataFrame(date_dict)

## import data
data = pd.read_csv('data/processed/capacity.csv')

# Use only one group for now
data = data[data['group'] == 'fullbody-4']

## preprocess
# date as datetime
data = data[['date', 'demand']]
data.columns = ['ds', 'y']
data['ds'] = pd.to_datetime(data['ds'])

# Generate future dates
start_date = datetime(2023, 9, 1)
end_date = datetime(2023, 9, 30)
future_dates = generate_future_dates(start_date, end_date)

# call prophet
m = Prophet()
m.fit(data)
forecast = m.predict(future_dates)

print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']])
