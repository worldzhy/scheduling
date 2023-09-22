from flask import Flask, jsonify
from src.algorithm.GeneticAlgorithm import GeneticAlgorithm
from src.entities.Data import Data

app = Flask(__name__)

# Route to get endpoint
# TO DO: Make the route accept specific params
@app.route('/schedule', methods=['POST'])
def index():
    # Get data
    data = Data()
    # Define algorithm to use
    algo = GeneticAlgorithm(data)
    # Run algorithm 
    algo.configure(
        num_crossover_points=3,
        max_iteration=10,
    )
    res = algo.run()
    # return res
    return jsonify(res)

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=3002)