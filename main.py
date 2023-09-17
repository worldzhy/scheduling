import traceback
from src.algorithm.GeneticAlgorithm import GeneticAlgorithm
from src.entities.Data import Data

def main():
    # Get data - Data loader
    data = Data()
    # Define algorithm to use
    algo = GeneticAlgorithm(data)
    # Run algorithm 
    algo.run(
        max_iteration = 10,
    )


try:
    main()
except:
    traceback.print_exc()