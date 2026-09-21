"""
Week 02 Autograder: Self-Driving Car, BFS en Sliding Puzzle.

Test de publieke interface van de oplossing van de student:
- SelfDrivingCar: process() met remlogica
- breadth_first_search / print_path
- SlidingPuzzle: possible_new_configurations, manhattan_distance, solve_puzzle

De tests controleren enkel gedrag, niet hoe het geimplementeerd is.
"""

import contextlib
import importlib
import threading

import pytest

MODULE_PATH = "exercises.week02.solution"

try:
    _mod = importlib.import_module(MODULE_PATH)
    SelfDrivingCar = _mod.SelfDrivingCar
    LidarSensorInput = _mod.LidarSensorInput
    Brake = _mod.Brake
    Nothing = _mod.Nothing
    breadth_first_search = _mod.breadth_first_search
    print_path = _mod.print_path
    State = _mod.State
    Node = _mod.Node
    SlidingPuzzle = _mod.SlidingPuzzle
    solve_puzzle = _mod.solve_puzzle
except Exception as import_error:
    pytest.skip(
        f"solution.py kon niet geimporteerd worden: {import_error}",
        allow_module_level=True,
    )

WEIGHTS = {
    # Self-Driving Car
    "test_selfdriving_initial": 1,
    "test_selfdriving_brake": 2,
    "test_selfdriving_no_brake": 1,
    # BFS
    "test_bfs_start_is_goal": 1,
    "test_bfs_simple_path": 2,
    "test_bfs_graph_path": 2,
    "test_bfs_no_path": 1,
    "test_bfs_print_path": 1,
    # Sliding Puzzle
    "test_sliding_possible_moves_center": 1,
    "test_sliding_possible_moves_corner": 1,
    "test_sliding_possible_moves_edge": 1,
    "test_sliding_manhattan_distance": 1,
    "test_sliding_is_goal": 1,
    "test_sliding_solve_one_step": 2,
    "test_sliding_solve_multiple_steps": 2,
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


# =============== Oefening 1: Self-Driving Car ===============


def test_selfdriving_initial():
    """Bij de eerste meting wordt er nog niet geremd."""
    car = SelfDrivingCar()
    sensor = LidarSensorInput(10)
    with time_limit():
        action = car.process(sensor)
    assert isinstance(action, Nothing), (
        "eerste meting moet Nothing teruggeven"
    )


def test_selfdriving_brake():
    """Remmen wanneer de voorligger snel dichterbij komt."""
    car = SelfDrivingCar()
    sensor = LidarSensorInput(10)
    # eerste meting (initialisatie)
    car.process(sensor)

    # voorligger komt snel dichter: 10m -> 4m in 1 stap
    sensor.DistanceTo = 4
    with time_limit():
        action = car.process(sensor)
    assert isinstance(action, Brake), (
        "moet remmen bij tijd tot botsing < 5s"
    )


def test_selfdriving_no_brake():
    """Niet remmen wanneer de voorligger veilig veraf blijft."""
    car = SelfDrivingCar()
    sensor = LidarSensorInput(10)
    car.process(sensor)

# =============== Oefening 2: BFS ===============


def _maak_graaf():
    """Bouw een eenvoudige graaf:
      A -> B -> C
      A -> C (rechtstreeks)
    """
    a = Node(State("A"))
    b = Node(State("B"))
    c = Node(State("C"))
    a.Actions = [b, c]
    b.Actions = [c]
    return a


def test_bfs_start_is_goal():
    """Als start de goal is, is het pad [start]."""
    with time_limit():
        pad = breadth_first_search(_maak_graaf(), State("A"))
    assert pad == [State("A")], (
        f"verwacht [State('A')], kreeg {pad}"
    )


def test_bfs_simple_path():
    """BFS vindt het korste pad A->B->C."""
    with time_limit():
        pad = breadth_first_search(_maak_graaf(), State("C"))
    # zowel A->B->C als A->C zijn geldig; check dat het eindigt op C
    assert pad[-1].Name == "C", "pad moet eindigen op C"
    assert pad[0].Name == "A", "pad moet beginnen bij A"


def test_bfs_graph_path():
    """BFS op een iets grotere graaf."""
    # A -> B -> D
    # A -> C -> D
    a = Node(State("A"))
    b = Node(State("B"))
    c = Node(State("C"))
    d = Node(State("D"))
    a.Actions = [b, c]
    b.Actions = [d]
    c.Actions = [d]
    with time_limit():
        pad = breadth_first_search(a, State("D"))
    assert len(pad) == 3, "korste pad moet 3 nodes bevatten"
    assert pad[-1].Name == "D"


def test_bfs_no_path():
    """BFS geeft None als er geen pad is."""
    a = Node(State("A"))
    b = Node(State("B"))
    c = Node(State("C"))
    a.Actions = [b]
    # C is onbereikbaar
    with time_limit():
        pad = breadth_first_search(a, State("C"))
    assert pad is None, "onbereikbare goal moet None geven"
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
    # voorligger rijdt weg: 10m -> 20m
    sensor.DistanceTo = 20
    with time_limit():
        action = car.process(sensor)
    assert isinstance(action, Brake) is False, (
        "mag niet remmen bij veilige afstand"
    )