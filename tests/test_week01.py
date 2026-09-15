"""
Week 01 Autograder: Insertion Sort + Floor Cleaning Agent.

Test de publieke interface van de oplossing van de student:
- insertion_sort(sequence)
- FloorCleaningAgent: move_*, clean_tile, move_to, clean_room

De tests controleren enkel gedrag, niet hoe het geimplementeerd is.
Studentencode die crasht of infinite loopt wordt netjes afgehandeld.
"""

import contextlib
import importlib
import random
import threading

import pytest

MODULE_PATH = "exercises_ai_assisted.week01.solution"

# Import van de studentcode in een beveiligde zone: als de import
# crasht (syntaxfout, fout bij import-tijd, ...) skippen alle tests
# in plaats van de hele run te breken.
try:
    _mod = importlib.import_module(MODULE_PATH)
    insertion_sort = _mod.insertion_sort
    FloorCleaningAgent = _mod.FloorCleaningAgent
except Exception as import_error:  # noqa: BLE001
    pytest.skip(
        f"solution.py kon niet geimporteerd worden: {import_error}",
        allow_module_level=True,
    )

WEIGHTS = {
    "test_insertion_sort_basic": 2,
    "test_insertion_sort_edge_cases": 2,
    "test_insertion_sort_random": 2,
    "test_agent_initial_position": 1,
    "test_agent_moves_and_walls": 2,
    "test_agent_clean_tile": 1,
    "test_agent_clean_room": 1,
}


@contextlib.contextmanager
def time_limit(seconds: int = 5):
    """Beperk de duur van een blok code (tegen infinite loops).

    Gebruikt threading.Timer omdat SIGALRM niet werkt op Windows.
    """
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


# ---------------- Oefening 1: Insertion Sort ----------------


def test_insertion_sort_basic():
    """Gewone lijsten worden gesorteerd van klein naar groot."""
    cases = [
        ([5, 2, 4, 6, 1, 3], [1, 2, 3, 4, 5, 6]),
        ([5, 4, 3, 2, 1], [1, 2, 3, 4, 5]),
        ([2.5, 1.5, 2.5], [1.5, 2.5, 2.5]),
    ]
    for invoer, verwacht in cases:
        kopie = list(invoer)
        with time_limit():
            resultaat = insertion_sort(kopie)
        assert resultaat == verwacht, f"{invoer} -> {resultaat}"


def test_insertion_sort_edge_cases():
    """Randgevallen: lege lijst, 1 element, duplicaten."""
    with time_limit():
        assert insertion_sort([]) == []
        assert insertion_sort([42]) == [42]
        assert insertion_sort([3, 1, 2, 1, 3]) == [1, 1, 2, 3, 3]


def test_insertion_sort_random():
    """Op willekeurige lijsten geeft hetzelfde resultaat als sorted()."""
    random.seed(2026)
    for _ in range(20):
        invoer = [random.randint(-50, 50) for _ in range(random.randint(0, 30))]
        with time_limit():
            resultaat = insertion_sort(list(invoer))
        assert resultaat == sorted(invoer), f"faalde voor {invoer}"


# ---------------- Oefening 2: Floor Cleaning Agent ----------------


def _maak_robot():
    """Maak een agent met de standaard kamer (10x5)."""
    try:
        return FloorCleaningAgent()
    except TypeError:
        # constructor zonder defaults: roep met defaults aan
        return FloorCleaningAgent(5, 10)


def test_agent_initial_position():
    """De agent start linksboven in de kamer."""
    robot = _maak_robot()
    assert (robot.row, robot.col) == (0, 0)


def test_agent_moves_and_walls():
    """Bewegingen werken en stoppen aan de rand van de kamer."""
    robot = _maak_robot()
    with time_limit():
        robot.move_right()
        assert (robot.row, robot.col) == (0, 1)
        robot.move_down()
        assert (robot.row, robot.col) == (1, 1)
        robot.move_left()
        robot.move_up()
        assert (robot.row, robot.col) == (0, 0)
        # aan de rand: positie mag niet veranderen en mag niet crashen
        robot.move_up()
        robot.move_left()
        assert (robot.row, robot.col) == (0, 0)


def test_agent_clean_tile():
    """clean_tile() markeert de huidige tegel als proper."""
    robot = _maak_robot()
    with time_limit():
        robot.clean_tile()
    assert robot.grid[0][0] is True, "tegel (0,0) zou proper moeten zijn"
    andere_vuil = any(
        robot.grid[r][c] is not True
        for r in range(robot.rows)
        for c in range(robot.cols)
        if (r, c) != (0, 0)
    )
    assert andere_vuil, "andere tegels moeten nog vuil zijn"


def test_agent_clean_room():
    """Na clean_room() is elke tegel van de kamer proper."""
    robot = _maak_robot()
    with time_limit(10):
        robot.clean_room()
    proper = [
        (r, c)
        for r in range(robot.rows)
        for c in range(robot.cols)
        if robot.grid[r][c] is True
    ]
    totaal = robot.rows * robot.cols
    assert len(proper) == totaal, (
        f"niet alle tegels zijn proper: {len(proper)}/{totaal}"
    )