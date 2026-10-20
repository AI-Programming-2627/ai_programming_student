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

    def total_distance(self, tour: list[int]) -> float:
        """Bereken de totale afstand van een tour, inclusief terugkeer
        naar de startstad.

        Args:
            tour: permutatie van steden (lijst van indices).

        Returns:
            De totale afstand: som van de afstanden tussen opeenvolgende
            steden, plus de afstand van de laatste stad terug naar de eerste.
        """
        #TODO

    @staticmethod
    def _canonical(tour: list[int]) -> list[int]:
        """Draai de tour zodat stad 0 vooraan staat (richting blijft gelijk).

        De totale afstand is invariant onder rotatie, dus dit verandert niets
        aan de kwaliteit van de tour maar maakt het resultaat eenduidig.

        Args:
            tour: een geldige tour (permutatie van steden).

        Returns:
            Dezelfde tour als lijst, beginnend bij stad 0.
        """
        start = tour.index(0)
        return tour[start:] + tour[:start]

    def simulated_annealing(self) -> tuple[list[int], float]:
        """Simulated annealing voor TSP.

        Het algoritme start van de natuurlijke tour [0, 1, ..., n-1] en
        zoekt stap voor stap verbeteringen: elke iteratie worden twee
        willekeurige steden verwisseld. Een betere tour wordt altijd
        aanvaard; een slechtere tour wordt aanvaard met kans
        exp(-Δ / T), waarbij de temperatuur T exponential afkoelt.

        Returns:
            Een tuple (best_tour, best_distance): de beste gevonden tour
            (beginnend bij stad 0) en de bijhorende totale afstand.
        """
        #TODO


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