"""
Week 03 Autograder: Maze met DFS en Dijkstra.

Test de publieke interface van de oplossingen van de student.
De tests controleren enkel gedrag, niet hoe het geïmplementeerd is.
"""

import contextlib
import importlib
import threading

import pytest

MAZE_MODULE_PATH = "exercises_ai_assisted.week03.maze_start"
DIJKSTRA_MODULE_PATH = "exercises_ai_assisted.week03.dijkstra_start"

# Importeer de maze-module
try:
    _maze_mod = importlib.import_module(MAZE_MODULE_PATH)
    Maze = _maze_mod.Maze
    find_path = _maze_mod.find_path
except Exception as e:
    pytest.skip(f"maze_start.py kon niet geïmporteerd worden: {e}",
                allow_module_level=True)

# Importeer de dijkstra-module
try:
    _dijk_mod = importlib.import_module(DIJKSTRA_MODULE_PATH)
    dijkstra = _dijk_mod.dijkstra
    Problem = _dijk_mod.Problem
    State = _dijk_mod.State
    Node = _dijk_mod.Node
    Edge = _dijk_mod.Edge
    Path = _dijk_mod.Path
except Exception as e:
    pytest.skip(f"dijkstra_start.py kon niet geïmporteerd worden: {e}",
                allow_module_level=True)

WEIGHTS = {
    "test_maze_valid_moves_midden": 2,
    "test_maze_valid_moves_muur": 1,
    "test_maze_valid_moves_rand": 1,
    "test_maze_extract_path": 2,
    "test_maze_find_path_bestaat": 2,
    "test_maze_find_path_onmogelijk": 1,
    "test_dijkstra_basis": 2,
}


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


# ============================================================
# Maze (DFS) tests
# ============================================================

def _maak_maze():
    """Hulpfunctie: maak een simpel 3x3 maze zonder muren."""
    return Maze((3, 3), (0, 0), (2, 2), [])


def test_maze_valid_moves_midden():
    """valid_moves geeft alle 4 buren in open ruimte."""
    with time_limit():
        maze = _maak_maze()
        moves = maze.valid_moves((1, 1))
    assert len(moves) == 4
    assert (0, 1) in moves
    assert (1, 0) in moves
    assert (2, 1) in moves
    assert (1, 2) in moves


def test_maze_valid_moves_muur():
    """valid_moves sluit posities met een muur uit."""
    with time_limit():
        maze = Maze((3, 3), (0, 0), (2, 2), [(1, 0)])
        moves = maze.valid_moves((0, 0))
    assert (1, 0) not in moves


def test_maze_valid_moves_rand():
    """valid_moves geeft enkel buren binnen de grenzen."""
    with time_limit():
        maze = _maak_maze()
        moves = maze.valid_moves((0, 0))
    assert len(moves) == 2
    assert (0, 1) in moves
    assert (1, 0) in moves


def test_maze_extract_path():
    """extract_path haalt een eenvoudig pad uit de stack."""
    with time_limit():
        maze = _maak_maze()
        stack = [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]
        pad = maze.extract_path(stack)
    assert isinstance(pad, list)
    assert pad[0] == (0, 0)
    assert pad[-1] == (2, 2)


def test_maze_find_path_bestaat():
    """find_path vindt een pad in een maze zonder muren."""
    with time_limit():
        maze = _maak_maze()
        resultaat = find_path(maze)
    assert isinstance(resultaat, tuple)
    assert len(resultaat) == 2
    pad, stappen = resultaat
    assert isinstance(pad, list)
    assert len(pad) > 0
    assert pad[0] == (0, 0)
    assert pad[-1] == (2, 2)


def test_maze_find_path_onmogelijk():
    """find_path geeft (None, 0) terug als er geen pad is."""
    with time_limit():
        # 2x2 maze met muren die elk pad blokkeren
        maze = Maze((2, 2), (0, 0), (1, 1), [(0, 1), (1, 0)])
        pad, stappen = find_path(maze)
    assert pad is None or stappen == 0


# ============================================================
# Dijkstra tests
# ============================================================

def _maak_driehoek_graaf():
    """Bouw een graaf: A -> B (2), A -> C (3), B -> C (1)
       Kortste pad A->C: A->B->C = 3, niet rechtstreeks A->C = 3.
       Kortste pad A->B: rechtstreeks = 2.
    """
    a = Node(State("A"))
    b = Node(State("B"))
    c = Node(State("C"))
    a.Actions = [Edge(a, b, 2.0), Edge(a, c, 3.0)]
    b.Actions = [Edge(b, c, 1.0)]
    c.Actions = []
    problem = Problem()
    problem.InitialState = a
    problem.GoalState = c
    return problem


def test_dijkstra_basis():
    """Dijkstra vindt het kortste pad in een eenvoudige graaf."""
    with time_limit():
        problem = _maak_driehoek_graaf()
        pad = dijkstra(problem)
    assert pad is not None
    assert isinstance(pad, Path)
    assert pad.Nodes[-1].State.Name == "C"
    # Kortste pad A->C is A->B->C met kost 3.0
    assert pad.Cost == 3.0