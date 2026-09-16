"""
Week 11 Autograder: tool-using agents (Oefening 3).

Test de publieke interface van de oplossing van de student:
- bfs / dfs / astar: lossen een getallenpuzzel op naar een geldig pad
- ToolAgent: kiest epsilon-greedy een tool en leert uit beloningen

De tests controleren enkel gedrag, niet hoe het geïmplementeerd is.
"""

import contextlib
import importlib
import random
import threading

import pytest

MODULE_PATH = "exercises_ai_assisted.week11.solution"

try:
    _mod = importlib.import_module(MODULE_PATH)
    bfs = _mod.bfs
    dfs = _mod.dfs
    astar = _mod.astar
    ToolAgent = _mod.ToolAgent
except Exception as e:
    pytest.skip(
        f"solution.py kon niet geïmporteerd worden: {e}",
        allow_module_level=True,
    )

WEIGHTS = {
    "test_tools_geldig_pad": 2,
    "test_bfs_optimaal": 2,
    "test_choose_tool_geldige_tool": 2,
    "test_epsilon_nul_kiest_beste": 2,
    "test_learn_bijwerkt_waarde": 1,
    "test_agent_leert_beste_tool": 3,
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


def _controleer_pad(pad, start: int, goal: int = 1) -> None:
    """Controleer dat een pad geldige stappen gebruikt en op het doel eindigt."""
    assert isinstance(pad, (list, tuple)), (
        f"pad is een lijst, kreeg {type(pad).__name__}"
    )
    assert pad[0] == start, f"pad begint bij {start}, kreeg {pad[0]}"
    assert pad[-1] == goal, f"pad eindigt bij {goal}, kreeg {pad[-1]}"
    for a, b in zip(pad, pad[1:]):
        geldig = (b == a - 1) or (a >= 3 and b == a - 3) or (a % 2 == 0 and b == a // 2)
        assert geldig, f"ongeldige stap {a} -> {b} in pad {list(pad)}"


# --- Puzzeltools ---


def test_tools_geldig_pad():
    """Elke tool geeft een geldig pad van start naar doel."""
    with time_limit():
        for start in (7, 10, 15):
            for tool in (bfs, dfs, astar):
                pad = tool({"start": start, "goal": 1})
                _controleer_pad(pad, start)


def test_bfs_optimaal():
    """bfs geeft een kortst mogelijk pad (bekende optima voor kleine startwaarden)."""
    optimaal = {7: 2, 10: 3, 15: 4}  # minimale aantal stappen naar 1
    with time_limit():
        for start, verwacht in optimaal.items():
            pad = bfs({"start": start, "goal": 1})
            _controleer_pad(pad, start)
            assert len(pad) - 1 == verwacht, (
                f"bfs vanaf {start} gebruikt {len(pad) - 1} stappen, "
                f"optimaal is {verwacht}"
            )


# --- ToolAgent ---


def test_choose_tool_geldige_tool():
    """choose_tool geeft altijd de naam van een beschikbare tool."""
    agent = ToolAgent(epsilon=0.5)
    random.seed(42)
    with time_limit():
        for _ in range(20):
            keuze = agent.choose_tool({"start": 10, "goal": 1})
    assert keuze in agent.tools, (
        f"keuze {keuze!r} zit niet in de beschikbare tools {sorted(agent.tools)}"
    )


def test_epsilon_nul_kiest_beste():
    """Met epsilon 0 kiest de agent telkens de tool met de hoogste waarde."""
    agent = ToolAgent(epsilon=0.0, alpha=0.5)
    with time_limit():
        for _ in range(4):
            agent.learn("astar", 4.0)
        agent.learn("bfs", 1.0)
        agent.learn("dfs", 0.0)
        keuzes = {agent.choose_tool({"start": 10, "goal": 1}) for _ in range(10)}
    assert keuzes == {"astar"}, (
        f"bij epsilon 0 wordt telkens de best gewaardeerde tool gekozen, "
        f"kreeg {sorted(keuzes)}"
    )


def test_learn_bijwerkt_waarde():
    """learn verhoogt de waarde van een tool richting de ontvangen reward."""
    agent = ToolAgent(epsilon=0.0, alpha=0.5)
    with time_limit():
        nieuwe_waarde = agent.learn("bfs", 4.0)
    assert agent.counts["bfs"] == 1, "learn telt het gebruik van de tool"
    assert 0.0 < nieuwe_waarde <= 4.0, (
        "de waarde beweegt richting de reward"
    )


def test_agent_leert_beste_tool():
    """Na voldoende beloningen wijst best_tool de best presterende tool aan."""
    agent = ToolAgent(epsilon=0.2, alpha=0.5)
    random.seed(7)
    rewards = {"bfs": 1.0, "dfs": 0.0, "astar": 3.0}
    with time_limit():
        for _ in range(200):
            keuze = agent.choose_tool({"start": 10, "goal": 1})
            agent.learn(keuze, rewards[keuze])
        beste = agent.best_tool()
    assert beste == "astar", (
        f"best_tool wijst de best presterende tool aan, kreeg {beste!r}"
    )
