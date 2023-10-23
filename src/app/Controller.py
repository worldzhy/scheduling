import os
from typing import Any, List, cast
from flask import Request
import pandas as pd
from .Validator import ForecastSchema
from ..entities.Config import Config
from ..entities.Data import Data
from ..entities.Constant import Constant
from ..entities.Result import MappingResult
from ..entities.Helper import Helper
from ..algorithm.GeneticAlgorithm import GeneticAlgorithm
from ..algorithm.Forecasting import Forecast

class Controller():
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

    def post_forecast(self, request: Request):
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

    def get_studio(self):
        # download file
        helper = Helper()
        s3_studio_prefix = 'unloaded-from-snowflake/studios'
        try:
            helper.delete_file('data/raw/' + s3_studio_prefix.replace('/', '_') + '.csv')
        except:
            # Ignore
            pass
        helper.download_files_as_one(Config.AWS_S3_BUCKET_DATALAKE, s3_studio_prefix)
        # read file
        data = pd.read_csv(
            'data/raw/' + s3_studio_prefix.replace('/', '_') + '.csv',
            usecols = ['STUDIOID','STUDIONAME'],
            index_col = False
        )
        data = data[data['STUDIOID'] > 0]
        # populate mapping
        mapping: List[MappingResult] = []
        for _, row in data.iterrows():
            mapping.append({
                'id': row['STUDIOID'],
                'value': row['STUDIONAME']
            })
        return sorted(mapping, key=lambda x: x["id"])

    def get_location(self, request: Request):
        # validation
        studio_id = request.args.get('studio_id')
        if studio_id is None:
            raise Exception('Value of studio_id missing in the query parameter.')
        # download file
        helper = Helper()
        s3_location_prefix = 'unloaded-from-snowflake/location'
        try:
            helper.delete_file('data/raw/' + s3_location_prefix.replace('/', '_') + '.csv')
        except:
            # Ignore
            pass
        helper.download_files_as_one(Config.AWS_S3_BUCKET_DATALAKE, s3_location_prefix)
        # read file
        data = pd.read_csv(
            'data/raw/' + s3_location_prefix.replace('/', '_') + '.csv',
            usecols = ['STUDIOID', 'LOCATIONID', 'LOCATIONNAME'],
            index_col = False
        )
        data = data[data['STUDIOID'] > 0]
        data = data[data['STUDIOID'] == int(studio_id)]
        if (len(data) == 0):
            raise Exception(f'No data found for studio_id {studio_id}.')
        # populate mapping
        mapping: List[MappingResult] = []
        for _, row in data.iterrows():
            mapping.append({
                'id': row['LOCATIONID'],
                'value': row['LOCATIONNAME']
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
        for ind, program in enumerate(Constant.MONTH_LIST):
            mapping.append({
                'id': ind + 1,
                'value': program
            })
        return sorted(mapping, key=lambda x: x["id"])