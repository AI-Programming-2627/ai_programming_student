"""
Week 03 Autograder: Maze met DFS en Dijkstra.

Test de publieke interface van de oplossingen van de student.
De tests controleren enkel gedrag, niet hoe het geïmplementeerd is.
"""

import contextlib
import importlib
import threading

import pytest

MAZE_MODULE_PATH = "exercises.week03.solution"
DIJKSTRA_MODULE_PATH = "exercises.week03.solution"

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

# Importeer de oplossing (BFS + sliding puzzle)
try:
    _sol_mod = importlib.import_module("exercises.week03.solution")
    SlidingPuzzle = _sol_mod.SlidingPuzzle
    solve_puzzle = _sol_mod.solve_puzzle
    State = _sol_mod.State
    Node = _sol_mod.Node
    breadth_first_search = _sol_mod.breadth_first_search
    print_path = _sol_mod.print_path
except Exception as e:
    pytest.skip(f"solution.py kon niet geïmporteerd worden: {e}",
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


# =============== Oefening 3: Sliding Puzzle ===============


def _puzzle_from_list(values):
    """Maak een SlidingPuzzle van een 2D lijst."""
    return SlidingPuzzle(values)


def test_sliding_possible_moves_center():
    """Leeg vakje in het midden geeft 4 mogelijke configuraties."""
    puzzle = _puzzle_from_list([
        [1, 2, 3],
        [4, 0, 5],
        [6, 7, 8],
    ])
    with time_limit():
        configs = puzzle.possible_new_configurations()
    assert len(configs) == 4, "middenpositie moet 4 moves geven"


def test_sliding_possible_moves_corner():
    """Leeg vakje in de hoek geeft 2 mogelijke configuraties."""
    puzzle = _puzzle_from_list([
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
    ])
    with time_limit():
        configs = puzzle.possible_new_configurations()
    assert len(configs) == 2, "hoekpositie moet 2 moves geven"


def test_sliding_possible_moves_edge():
    """Leeg vakje aan de rand (niet hoek) geeft 3 mogelijke configuraties."""
    puzzle = _puzzle_from_list([
        [1, 0, 2],
        [3, 4, 5],
        [6, 7, 8],
    ])
    with time_limit():
        configs = puzzle.possible_new_configurations()
    assert len(configs) == 3, "randpositie moet 3 moves geven"


def test_sliding_manhattan_distance():
    """Manhattan-afstand wordt correct berekend."""
    # 1 stap van goal: leeg vakje (0) en 6 verwisseld
    puzzle = _puzzle_from_list([
        [1, 2, 3],
        [4, 5, 0],
        [7, 8, 6],
    ])
    with time_limit():
        dist = puzzle.manhattan_distance()
    # 6 staat op (2,2), hoort op (2,1) -> |2-2| + |2-1| = 1
    assert dist == 1, f"verwacht 1, kreeg {dist}"

    # goal zelf
    goal_puzzle = _puzzle_from_list([
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0],
    ])
    with time_limit():
        dist = goal_puzzle.manhattan_distance()
    assert dist == 0, "goal moet Manhattan-afstand 0 hebben"


def test_sliding_is_goal():
    """is_goal herkent de doelconfiguratie correct."""
    goal = _puzzle_from_list([
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0],
    ])
    assert goal.is_goal() is True, "goal moet True geven"

    niet_goal = _puzzle_from_list([
        [1, 2, 3],
        [4, 5, 0],
        [7, 8, 6],
    ])
    assert niet_goal.is_goal() is False, "niet-goal moet False geven"


def test_sliding_solve_one_step():
    """solve_puzzle lost een puzzel op die 1 zet van goal is."""
    puzzle = _puzzle_from_list([
        [1, 2, 3],
        [4, 5, 0],
        [7, 8, 6],
    ])
    with time_limit(10):
        oplossing = solve_puzzle(puzzle)
    assert oplossing is not None, "er moet een oplossing zijn"
    assert len(oplossing) == 2, (
        f"verwacht 2 configuraties (start + goal), kreeg {len(oplossing)}"
    )
    assert oplossing[-1].is_goal(), "laatste configuratie moet goal zijn"


def test_sliding_solve_multiple_steps():
    """solve_puzzle lost een puzzel op die meerdere zetten van goal is."""
    puzzle = _puzzle_from_list([
        [1, 2, 3],
        [4, 0, 5],
        [7, 8, 6],
    ])
    with time_limit(30):
        oplossing = solve_puzzle(puzzle)
    assert oplossing is not None, "er moet een oplossing zijn"
    assert oplossing[-1].is_goal(), "laatste configuratie moet goal zijn"
    # De lege plek moet verschoven zijn, minstens een paar stappen
    assert len(oplossing) >= 3, "er zijn minstens 2 zetten nodig"


def test_bfs_print_path():
    """print_path geeft een nette string terug."""
    pad = [State("A"), State("B"), State("C")]
    with time_limit():
        resultaat = print_path(pad)
    assert isinstance(resultaat, str)
    assert "A" in resultaat and "B" in resultaat and "C" in resultaat

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