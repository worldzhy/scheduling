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
        params = cast(Any, schema.load(request.json))
        # get parameters
        studio = cast(int, params['studio_id'])
        program = cast(int, params['program_id'])
        location = cast(int, params['location_id'])
        year = cast(int, params['year'])
        month = cast(int, params['month'])
        # run model and return result
        algo = Forecast(studio, program, location, year, month)
        return algo.run()
