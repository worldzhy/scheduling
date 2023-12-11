import pandas as pd
from typing import Any, List, cast
from flask import Request
from .Validator import ForecastSchema
from .ValidatorV2 import ForecastSchema as ForecastSchemaV2
from ..entities.Config import Config
from ..entities.Data import Data
from ..entities.Constant import Constant
from ..entities.Result import MappingResult
from ..entities.Helper import Helper
from ..algorithm.GeneticAlgorithm import GeneticAlgorithm
from ..algorithm.Forecasting import Forecast
from ..algorithm.ForecastingV2 import Forecast as ForecastV2
from ..data.DataStudio import DataStudio
from ..data.DataLocation import DataLocation

class Controller():
    def __init__(self):
        # params
        self._helper = Helper()

    def post_schedule(self):
        # get data
        data = Data()
        # run model and return result
        algo = GeneticAlgorithm(data)
        algo.configure(
            num_crossover_points=3,
            max_iteration=10,
            debug=(Config.APP_DEBUG == 'True')
        )
        return algo.run()

    def post_v1_forecast(self, request: Request):
        # validate request
        schema = ForecastSchema()
        body = cast(Any, schema.load(request.json))
        # get parameters
        studio = cast(int, body['params']['studio_id'])
        program = cast(int, body['params']['program_id'])
        location = cast(int, body['params']['location_id'])
        year = cast(int, body['params']['year'])
        month = cast(int, body['params']['month'])
        # get configs
        force_fetch = cast(bool, body['config']['force_fetch']) if body['config'] and body['config']['force_fetch'] else None
        # configure model
        algo = Forecast(studio, program, location, year, month)
        algo.configure(
            force_fetch = force_fetch
        )
        # run model and return result
        return algo.run()

    def post_v2_forecast(self, request: Request):
        # validate request
        schema = ForecastSchemaV2()
        body = cast(Any, schema.load(request.json))
        # get parameters
        studio = cast(int, body['params']['studio_id'])
        program = cast(int, body['params']['program_id'])
        location = cast(int, body['params']['location_id'])
        timeslot_start_id = cast(int, body['params']['timeslot_start_id'])
        timeslot_end_id = cast(int, body['params']['timeslot_end_id'])
        year = cast(int, body['params']['year'])
        month = cast(int, body['params']['month'])
        # get configs
        force_fetch = cast(bool, body['config']['force_fetch']) if body['config'] and body['config']['force_fetch'] else None
        # configure model
        print(timeslot_start_id, timeslot_end_id)
        algo = ForecastV2(studio, program, location, year, month, timeslot_start_id, timeslot_end_id)
        algo.configure(
            force_fetch = force_fetch
        )
        # run model and return result
        return algo.run()

    def get_studio(self):
        # download and read data
        DataStudio().preprocess(True)
        data = pd.read_csv(Constant.PATH_CSV_STUDIO)
        # populate mapping
        mapping: List[MappingResult] = []
        for _, row in data.iterrows():
            mapping.append({
                'id': row['id'],
                'value': row['name']
            })
        return sorted(mapping, key=lambda x: x["id"])

    def get_location(self, request: Request):
        # validation
        studio_id = request.args.get('studio_id')
        if studio_id is None:
            raise Exception('Value of studio_id missing in the query parameter.')
        # download and read data
        DataLocation().preprocess(True)
        data = pd.read_csv(Constant.PATH_CSV_LOCATION)
        # filter data
        data = data[data['studio_id'] == int(studio_id)]
        if (len(data) == 0):
            raise Exception(f'No data found for studio_id {studio_id}.')
        # populate mapping
        mapping: List[MappingResult] = []
        for _, row in data.iterrows():
            mapping.append({
                'id': row['id'],
                'value': row['name']
            })
        return sorted(mapping, key=lambda x: x["id"])

    def get_program(self):
        mapping: List[MappingResult] = []
        for ind, program in enumerate(Constant.PROGRAM_LIST):
            mapping.append({
                'id': ind,
                'value': program
            })
        return sorted(mapping, key=lambda x: x["id"])
    
    def get_month(self):
        mapping: List[MappingResult] = []
        for ind, month in enumerate(Constant.MONTH_LIST):
            mapping.append({
                'id': ind + 1,
                'value': month
            })
        return sorted(mapping, key=lambda x: x["id"])
    
    def get_weekday(self):
        mapping: List[MappingResult] = []
        for ind, weekday in enumerate(Constant.WEEKDAY_LIST):
            mapping.append({
                'id': ind,
                'value': weekday
            })
        return sorted(mapping, key=lambda x: x["id"])
    
    def get_coach_tier(self):
        mapping: List[MappingResult] = []
        for ind, coach_tier in enumerate(Constant.COACH_TIER_LIST):
            mapping.append({
                'id': ind,
                'value': coach_tier
            })
        return sorted(mapping, key=lambda x: x["id"])
    
    def get_timeslot_list(self):
        mapping: List[MappingResult] = []
        for ind, timeslot in enumerate(Constant.TIMESLOT_LIST):
            mapping.append({
                'id': ind,
                'value': timeslot
            })
        return sorted(mapping, key=lambda x: x["id"])