# import traceback
# from src.algorithm.GeneticAlgorithm import GeneticAlgorithm
# from src.entities.Data import Data

# def main():
#     # Get data
#     data = Data()
#     # Define algorithm to use
#     algo = GeneticAlgorithm(data)
#     # Run algorithm 
#     algo.configure(
#         num_crossover_points=3,
#         max_iteration=10
#     )
#     res = algo.run()
#     return res

# try:
#     main()
# except:
#     traceback.print_exc()