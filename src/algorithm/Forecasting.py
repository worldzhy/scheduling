from typing import List
from datetime import datetime, timedelta
from src.entities.Result import ForecastResult
from prophet import Prophet
import pandas as pd
import calendar

class Forecast():
    def __init__(self, studio_id: int, program_id: int, location_id: int, year: int, month: int):
        self._studio_id = studio_id
        self._program_id = program_id
        self._location_id = location_id
        self._year = year
        self._month = month
        self._program_list = ['30minexpress', 'advanced', 'armsabs', 'beginner', 'bunsabs', 'bunsguns', 'training', 'foundations', 'fullbody']

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
        # generate a list of dates and days
        date_list: List[datetime] = []
        day_list: List[int] = []
        # start loop
        current_date = start_date
        while current_date <= end_date:
            date_list.append(pd.to_datetime(current_date.strftime('%Y-%m-%d')))
            day_list.append(current_date.isoweekday())
            current_date += timedelta(days = 1)
        # return list of dates
        return pd.DataFrame({'ds': date_list, 'day': day_list})

    def _get_program_by_id(self, id: int) -> str:
        if id >= len(self._program_list):
            raise Exception(f'Invalid program id, should only be 0 to {len(self._program_list) - 1}')
        return self._program_list[id]

    def run(self) -> List[ForecastResult]:
        # import data
        data = pd.read_csv('data/processed/capacity.csv')
        # filter by studio
        data = data[data['studio'] == int(self._studio_id)]
        if (len(data) == 0):
            raise Exception(f'No data found for studio "{self._studio_id}"')
        # filter by group
        data = data[data['group'] == str(f'{self._get_program_by_id(self._program_id)}-{self._location_id}')]
        if (len(data) == 0):
            raise Exception(f'No data found for program "{self._program_id}" in location "{self._location_id}"')
        # generate forecasts
        forecasts: List[ForecastResult] = []   
        # preprocess data
        data = data[['date', 'demand', 'day']]
        data.columns = ['ds', 'y', 'day']
        data['ds'] = pd.to_datetime(data['ds'])
        # call prophet
        m = Prophet()
        m.add_regressor('day')
        m.add_country_holidays(country_name = 'US')
        m.fit(data)
        # generate future dates
        future_dates = self._generate_future_dates()
        forecast = m.predict(future_dates)

        # get only needed columns
        forecast = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

        # append to forecasts object
        for _, row in forecast.iterrows():
            forecasts.append({
                'date': row['ds'],
                'studio_id': self._studio_id,
                'location_id': self._location_id,
                'program_id': self._program_id,
                'capacity': row['yhat'],
                'capacity_lower': row['yhat_lower'],
                'capacity_upper': row['yhat_upper'],
            })

        # Return forecasts
        return forecasts
