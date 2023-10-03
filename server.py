import os
from src.algorithm.Forecasting import forecast
from flask import Flask, jsonify, request
from dotenv import load_dotenv
from src.algorithm.GeneticAlgorithm import GeneticAlgorithm
from src.entities.Data import Data
from marshmallow import Schema, fields, validates, ValidationError

load_dotenv()
app = Flask(__name__)

# TO DO: Make the route accept specific params
@app.route('/schedule', methods=['POST'])
def post_schedule():
    try:
        # Get data
        data = Data()
        # Define algorithm to use
        algo = GeneticAlgorithm(data)
        # Run algorithm 
        algo.configure(
            num_crossover_points=3,
            max_iteration=10,
            debug=(os.getenv('APP_DEBUG') == 'True')
        )
        res = algo.run()
        # return result
        return jsonify(res), 200
    except Exception as e:
        # Catch any exception and access its error message
        error_message = str(e)
        if error_message:
            return jsonify({'message': f'An error occurred: {error_message}'})
        else:
            return jsonify({'message': 'An unknown error occurred.'})
        
# TO DO: Make the route accept specific params
@app.route('/forecast', methods=['POST'])
def post_forecast():
    try:
        # Schema of the body
        class BodySchema(Schema):
            studio = fields.String(required=True)
            program = fields.String(required=True)
            location = fields.String(required=True)
            month = fields.Integer(required=True)
            year = fields.Integer(required=True)

            @validates('studio')
            def validate_studio(self, value):
                if not value.strip():
                    raise ValidationError('studio cannot be an empty string')

            @validates('program')
            def validate_program(self, value):
                if not value.strip():
                    raise ValidationError('program cannot be an empty string')
                
            @validates('location')
            def validate_location(self, value):
                if not value.strip():
                    raise ValidationError('location cannot be an empty string')
        
        # Parse and validate the request body
        schema = BodySchema()
        data = schema.load(request.json)

        # Get request body
        studio = data['studio']
        program = data['program']
        location = data['location']
        year = data['year']
        month = data['month']

        # Run model 
        res = forecast(studio, program, location, year, month)

        # Return result
        return jsonify(res), 200
    except Exception as e:
        # Catch any exception and access its error message
        error_message = str(e)
        if error_message:
            return jsonify({'message': f'An error occurred: {error_message}'})
        else:
            return jsonify({'message': 'An unknown error occurred.'})

if __name__ == '__main__':
    from waitress import serve
    port = 8080
    serve(app, port=port)