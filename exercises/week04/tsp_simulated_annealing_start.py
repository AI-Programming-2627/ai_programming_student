"""
Oefening: TSP met Simulated Annealing
======================================
"""
import math
import random

import numpy as np


class TSPSolver:
    def __init__(self, distance_matrix, initial_temperature=1000,
                 cooling_rate=0.995, num_iterations=10000):
        self.distance_matrix = distance_matrix
        self.num_cities = len(distance_matrix)
        self.initial_temperature = initial_temperature
        self.cooling_rate = cooling_rate
        self.num_iterations = num_iterations

    def total_distance(self, tour):
        # TODO: bereken totale afstand van de tour (heen en terug)
        pass

    def simulated_annealing(self):
        # TODO: implementeer simulated annealing
        # 1. genereeer starttour
        # 2. loop over iteraties
        # 3. verwissel 2 steden, bereken Δ
        # 4. aanvaar beter of aanvaar slechter met kans exp(-Δ/T)
        # 5. update temperatuur, onthoud beste
        pass


if __name__ == "__main__":
    distance_matrix = np.array([
        [0, 29, 20, 21],
        [29, 0, 15, 18],
        [20, 15, 0, 25],
        [21, 18, 25, 0]
    ])

    tsp_solver = TSPSolver(distance_matrix)
    best_tour, best_distance = tsp_solver.simulated_annealing()

    print("Best Tour:", best_tour)
    print("Best Distance:", best_distance)