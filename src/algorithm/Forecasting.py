from typing import List, TypedDict
from datetime import datetime, timedelta
from src.entities.Result import ForecastResult
from prophet import Prophet
import pandas as pd
import calendar

class Forecast():
    def __init__(self, studio: str, program: str, location: str, year: int, month: int):
        self._studio = studio
        self._program = program
        self._location = location
        self._year = year
        self._month = month

    def _get_days_in_month(self) -> int:
        try:
            # get the number of days in the given month and year
            _, num_days = calendar.monthrange(self._year, self._month)
            return num_days
        except ValueError as e:
            raise Exception(e)

    def _generate_future_dates(self) -> pd.DataFrame:
        start_date = datetime(self._year, self._month, 1)
        end_date = datetime(self._year, self._month, self._get_days_in_month())
        # generate a list of dates
        date_list: List[datetime] = []
        # start loop
        current_date = start_date
        while current_date <= end_date:
            date_list.append(pd.to_datetime(current_date.strftime('%Y-%m-%d')))
            current_date += timedelta(days = 1)
        # return list of dates
        return pd.DataFrame({'ds': date_list})

    def run(self) -> List[ForecastResult]:
        # import data
        data = pd.read_csv('data/processed/capacity.csv')
        # filter by studio
        data = data[data['studio'] == int(self._studio)]
        if (len(data) == 0):
            raise Exception(f'No data found for studio "{self._studio}"')
        # filter by group
        data = data[data['group'] == str(f'{self._program}-{self._location}')]
        if (len(data) == 0):
            raise Exception(f'No data found for program "{self._program}" in location "{self._location}"')
        # generate forecasts
        forecasts: List[ForecastResult] = []   
        # preprocess data
        data = data[['date', 'demand']]
        data.columns = ['ds', 'y']
        data['ds'] = pd.to_datetime(data['ds'])
        # generate future dates
        future_dates = self._generate_future_dates()
        # call prophet
        m = Prophet()
        m.fit(data)
        forecast = m.predict(future_dates)

        # get only needed columns
        forecast = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

        # append to forecasts object
        for _, row in forecast.iterrows():
            forecasts.append({
                'date': row['ds'],
                'studio': self._studio,
                'location': self._location,
                'program': self._program,
                'capacity': row['yhat'],
                'capacity_lower': row['yhat_lower'],
                'capacity_upper': row['yhat_upper'],
            })

        # Return forecasts
        return forecasts
