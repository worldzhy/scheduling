import os
from typing import Any, cast
from flask import Request
from .Validator import ForecastSchema
from ..entities.Data import Data
from ..algorithm.GeneticAlgorithm import GeneticAlgorithm
from ..algorithm.Forecasting import Forecast

class Controller():
    def schedule(self):
        # get data
        data = Data()
        # run model and return result
        algo = GeneticAlgorithm(data)
        algo.configure(
            num_crossover_points=3,
            max_iteration=10,
            debug=(os.getenv('APP_DEBUG') == 'True')
        )
        return algo.run()

    def forecast(self, request: Request):
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
