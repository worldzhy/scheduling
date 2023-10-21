from typing import List
from datetime import datetime, timedelta
from src.data.DataForecast import DataForecast
from src.entities.Result import ForecastResult
from src.entities.Constant import Constant
from prophet import Prophet
import pandas as pd
import calendar

class Forecast():
    def __init__(self, studio_id: int, program_id: int, location_id: int, year: int, month: int):
        # params
        self._studio_id = studio_id
        self._program_id = program_id
        self._location_id = location_id
        self._year = year
        self._month = month
        self._program_list = Constant.PROGRAM_LIST
        # configs
        self._force_fetch: bool = False

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
            raise Exception(f'Invalid program id, should only be 0 to {len(self._program_list) - 1}.')
        return self._program_list[id]

    def _get_data(self) -> pd.DataFrame:
        # fetch and preprocess data
        # TO DO: Cache this
        DataForecast().preprocess(self._force_fetch)
        # import data
        data = pd.read_csv('data/processed/demand.csv')
        # filter by studio
        data = data[data['studio'] == int(self._studio_id)]
        if (len(data) == 0):
            raise Exception(f'No data found for studio "{self._studio_id}".')
        # filter by program and location
        data = data[data['group'] == str(f'{self._get_program_by_id(self._program_id)}-{self._location_id}')]
        if (len(data) == 0):
            raise Exception(f'No data found for program "{self._program_id}" in location "{self._location_id}".')
        # get only required columns
        data = data[['date', 'demand', 'day']]
        data.columns = ['ds', 'y', 'day']
        # date as datetime
        data['ds'] = pd.to_datetime(data['ds'])
        # return data
        return data
    
    def configure(
        self,
        force_fetch: None | bool = None,
    ) -> None:
        self._force_fetch = force_fetch if force_fetch is not None else self._force_fetch

    def run(self) -> List[ForecastResult]:
        # get data
        data = self._get_data()
        if (len(data) < 1000):
            raise Exception(f'Not enough data to produce forecast result. Data length is {len(data)}, needs atleast 1000.')
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
        forecasts: List[ForecastResult] = [] 
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
        # return forecasts
        return forecasts
