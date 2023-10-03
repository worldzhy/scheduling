import os
from src.algorithm.Forecasting import forecast
from flask import Flask, jsonify
from dotenv import load_dotenv
from src.algorithm.GeneticAlgorithm import GeneticAlgorithm
from src.entities.Data import Data

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
        # Run model 
        res = forecast()
        # return result
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