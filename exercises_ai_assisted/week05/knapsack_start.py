"""
Oefening 2: Knapsack Probleem met pygad
=========================================
Los het knapsack probleem op met een genetisch algoritme.
"""
import pygad
import numpy as np

# Data
capaciteit = 10
gewichten = np.array([5, 4, 6, 3])
waarden = np.array([10, 40, 30, 50])
n_voorwerpen = len(gewichten)


def fitness_func(solution, solution_idx):
    # TODO: bereken totale waarde, straf als gewicht > capaciteit
    pass


# TODO: configureer pygad.GA (zie OneMax.py uit de cursus)
# ga_instance = pygad.GA(
#     num_generations=...,
#     num_parents_mating=...,
#     fitness_func=fitness_func,
#     sol_per_pop=...,
#     num_genes=n_voorwerpen,
#     mutation_percent_genes=...,
# )
# ga_instance.run()

# Oplossing tonen
# solution, solution_fitness, _ = ga_instance.best_solution()
# print("Gekozen voorwerpen:", solution)
# print("Totale waarde:", solution_fitness)