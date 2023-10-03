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

def forecast(studio, program, location):
    ## import data
    data = pd.read_csv('data/processed/capacity.csv')

    # Filter by studio
    data = data[data['studio'] == int(studio)]
    if (len(data) == 0):
        raise Exception(f'No data found for studio "{studio}"')

    # Filter by group
    data = data[data['group'] == str(f'{program}-{location}')]
    if (len(data) == 0):
        raise Exception(f'No data found for program "{program}" in location "{location}"')

    # Process group
    forecasts = []   

    ## Preprocess
    # Date as datetime
    data = data[['date', 'demand']]
    data.columns = ['ds', 'y']
    data['ds'] = pd.to_datetime(data['ds'])

    # Generate future dates
    start_date = datetime(2023, 9, 1)
    end_date = datetime(2023, 9, 30)
    future_dates = generate_future_dates(start_date, end_date)

    # Call prophet
    m = Prophet()
    m.fit(data)
    forecast = m.predict(future_dates)

    # Get only needed columns
    forecast = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

    # Append to forecasts object
    for _, row in forecast.iterrows():
        forecasts.append({
            'date': row['ds'],
            'studio': studio,
            'location': location,
            'program': program,
            'capacity': row['yhat'],
            'capacity_lower': row['yhat_lower'],
            'capacity_upper': row['yhat_upper'],
        })

    # Return forecasts
    return forecasts
