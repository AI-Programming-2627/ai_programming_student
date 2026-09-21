"""
Week 04 Autograder: TSP met Simulated Annealing.

Test de publieke interface van de oplossing van de student:
- TSPSolver: total_distance(tour), simulated_annealing()

De tests controleren enkel gedrag, niet hoe het geïmplementeerd is.
"""

import contextlib
import importlib
import threading

import numpy as np
import pytest

MODULE_PATH = "exercises.week04.tsp_simulated_annealing_start"

try:
    _mod = importlib.import_module(MODULE_PATH)
    TSPSolver = _mod.TSPSolver
except Exception as e:
    pytest.skip(
        f"tsp_simulated_annealing_start.py kon niet geïmporteerd worden: {e}",
        allow_module_level=True,
    )

WEIGHTS = {
    "test_total_distance_basic": 2,
    "test_total_distance_edge_cases": 1,
    "test_simulated_annealing_returns_valid_tour": 2,
    "test_simulated_annealing_vindt_kortere_route": 2,
    "test_simulated_annealing_vier_steden": 2,
}

# --------------------- hulpdata ---------------------

AFSTAND_4 = np.array([
    [0, 29, 20, 21],
    [29, 0, 15, 18],
    [20, 15, 0, 25],
    [21, 18, 25, 0],
])

AFSTAND_3 = np.array([
    [0, 10, 20],
    [10, 0, 15],
    [20, 15, 0],
])


@contextlib.contextmanager
def time_limit(seconds: int = 5):
    """Beperk de duur van een blok code (tegen infinite loops)."""
    timeout_triggered = False

    def _raise():
        nonlocal timeout_triggered
        timeout_triggered = True

    timer = threading.Timer(seconds, _raise)
    timer.start()
    try:
        yield
        if timeout_triggered:
            raise TimeoutError(f"code duurde te lang (>{seconds}s)")
    finally:
        timer.cancel()


# =============== Oefening: total_distance ===============


def test_total_distance_basic():
    """total_distance berekent de totale afstand correct (heen en terug)."""
    solver = TSPSolver(AFSTAND_4)

    with time_limit():
        afstand = solver.total_distance([0, 1, 2, 3])

    # 0->1: 29, 1->2: 15, 2->3: 25, 3->0: 21  =>  90
    assert afstand == 90, f"verwacht 90, kreeg {afstand}"

    with time_limit():
        afstand2 = solver.total_distance([0, 2, 1, 3])

    # 0->2: 20, 2->1: 15, 1->3: 18, 3->0: 21  =>  74
    assert afstand2 == 74, f"verwacht 74, kreeg {afstand2}"


def test_total_distance_edge_cases():
    """total_distance werkt correct met 2 en 3 steden."""
    matrix_2 = np.array([[0, 5], [5, 0]])
    solver = TSPSolver(matrix_2)

    with time_limit():
        afstand = solver.total_distance([0, 1])
    # 0->1: 5, 1->0: 5  =>  10
    assert afstand == 10, f"verwacht 10, kreeg {afstand}"

    solver3 = TSPSolver(AFSTAND_3)
    with time_limit():
        afstand3 = solver3.total_distance([0, 1, 2])
    # 0->1: 10, 1->2: 15, 2->0: 20  =>  45
    assert afstand3 == 45, f"verwacht 45, kreeg {afstand3}"


# =============== Oefening: simulated_annealing ===============


def test_simulated_annealing_returns_valid_tour():
    """simulated_annealing retourneert (best_tour, best_distance)
    met een geldige permutatie van alle steden."""
    solver = TSPSolver(AFSTAND_4)

    with time_limit(10):
        resultaat = solver.simulated_annealing()

    assert isinstance(resultaat, tuple), (
        f"verwacht tuple, kreeg {type(resultaat)}"
    )
    assert len(resultaat) == 2, (
        f"verwacht 2 elementen, kreeg {len(resultaat)}"
    )

    best_tour, best_distance = resultaat

    assert isinstance(best_tour, list), (
        f"best_tour moet een list zijn, kreeg {type(best_tour)}"
    )
    assert len(best_tour) == 4, (
        f"best_tour moet 4 steden bevatten, kreeg {len(best_tour)}"
    )

    # Controleer dat alle steden in de tour voorkomen (permutatie)
    assert sorted(best_tour) == [0, 1, 2, 3], (
        f"best_tour is geen geldige permutatie: {best_tour}"
    )

    assert isinstance(best_distance, (int, float)), (
        f"best_distance moet een getal zijn, kreeg {type(best_distance)}"
    )
    assert best_distance > 0, (
        f"best_distance moet positief zijn, kreeg {best_distance}"
    )


def test_simulated_annealing_vindt_kortere_route():
    """simulated_annealing vindt een kortere route dan een willekeurige
    starttour."""
    solver = TSPSolver(AFSTAND_4)

    with time_limit(10):
        best_tour, best_distance = solver.simulated_annealing()

    # Een willekeurige starttour heeft gemiddeld ~83 als afstand.
    # De optimale is 74. We testen dat de gevonden route <= 83 is,
    # wat aantoont dat het algoritme een verbetering zoekt.
    assert best_distance <= 83, (
        f"SA vond route met afstand {best_distance}, "
        f"verwacht <= 83 (beter dan gemiddeld random)"
    )


def test_simulated_annealing_vier_steden():
    """simulated_annealing vindt de optimale of bijna-optimale route
    voor 4 steden (optimum = 74)."""
    solver = TSPSolver(
        AFSTAND_4,
        initial_temperature=1000,
        cooling_rate=0.995,
        num_iterations=5000,
    )

    with time_limit(10):
        best_tour, best_distance = solver.simulated_annealing()

    # Voor 4 steden moet SA het optimum 74 kunnen vinden met voldoende
    # iteraties. We accepteren een kleine afwijking vanwege de
    # random factor.
    assert best_distance <= 76, (
        f"SA vond afstand {best_distance}, verwacht <= 76 "
        f"(optimum = 74)"
    )
    # Controleer of het optimum effectief gevonden werd
    assert best_tour in ([0, 2, 1, 3], [0, 3, 1, 2]), (
        f"SA vond tour {best_tour}, verwacht een optimale tour "
        f"zoals [0, 2, 1, 3] of [0, 3, 1, 2]"
    )