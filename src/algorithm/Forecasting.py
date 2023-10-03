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

def forecast():
    ## import data
    data = pd.read_csv('data/processed/capacity.csv')

    # Use only one group for now
    groups = data['group'].unique()

    # Process by group
    forecasts = []   
    for group in groups:
        # Filter data by group
        data_temp = data[data['group'] == group]

        ## Preprocess
        # Date as datetime
        data_temp = data_temp[['date', 'demand']]
        data_temp.columns = ['ds', 'y']
        data_temp['ds'] = pd.to_datetime(data_temp['ds'])

        # Generate future dates
        start_date = datetime(2023, 9, 1)
        end_date = datetime(2023, 9, 30)
        future_dates = generate_future_dates(start_date, end_date)

        # Call prophet
        m = Prophet()
        m.fit(data_temp)
        forecast = m.predict(future_dates)

        # Get only needed columns
        forecast = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

        # Append to forecasts object
        for index, row in forecast.iterrows():
            forecasts.append({
                'date': row['ds'],
                'studio': '---',
                'location': group.split('-')[1],
                'program': group.split('-')[0],
                'capacity': row['yhat'],
                'capacity_lower': row['yhat_lower'],
                'capacity_upper': row['yhat_upper'],
            })

    # Return forecasts
    return forecasts
