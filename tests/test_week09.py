"""
Week 09 Autograder: Explore vs Exploit (epsilon-greedy en Gittins-index).

Test de publieke interface van de oplossing van de student:
- epsilon_greedy: average_rewards en true_rewards
- calculate_gittins_index: index op basis van n, X, t en gamma
- GittinsAgent: __init__, select_arm, update

De tests controleren enkel gedrag, niet hoe het geïmplementeerd is.
"""

import contextlib
import importlib
import math
import threading

import numpy as np
import pytest

EPSILON_PATH = "exercises_ai_assisted.week09.epsilon_greedy_start"
GITTINS_PATH = "exercises_ai_assisted.week09.gittins_start"

try:
    _eps_mod = importlib.import_module(EPSILON_PATH)
    epsilon_greedy = _eps_mod.epsilon_greedy
except Exception as import_error:
    pytest.skip(
        f"epsilon_greedy_start.py kon niet geïmporteerd worden: {import_error}",
        allow_module_level=True,
    )

try:
    _git_mod = importlib.import_module(GITTINS_PATH)
    calculate_gittins_index = _git_mod.calculate_gittins_index
    GittinsAgent = _git_mod.GittinsAgent
except Exception as import_error:
    pytest.skip(
        f"gittins_start.py kon niet geïmporteerd worden: {import_error}",
        allow_module_level=True,
    )

WEIGHTS = {
    "test_epsilon_greedy_vorm": 1,
    "test_epsilon_greedy_bereik": 1,
    "test_epsilon_greedy_exploit_convergeert": 2,
    "test_gittins_nul_is_inf": 1,
    "test_gittins_formule": 2,
    "test_gittins_gamma_default": 1,
    "test_gittins_hoge_reward_hogere_index": 1,
    "test_agent_initiele_toestand": 1,
    "test_agent_update": 1,
    "test_select_arm_geldige_arm": 1,
    "test_select_arm_verkiest_niet_geprobeerde_arm": 2,
    "test_select_arm_kiest_bestste_arm": 2,
}


@contextlib.contextmanager
def time_limit(seconds: int = 10):
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


# --- Oefening 1: epsilon-greedy ---


def test_epsilon_greedy_vorm():
    """epsilon_greedy geeft average_rewards en true_rewards met juiste lengtes."""
    with time_limit():
        resultaat = epsilon_greedy(arms=4, epsilon=0.1, num_iterations=50)
    assert resultaat is not None, "epsilon_greedy mag None niet teruggeven"
    assert len(resultaat) == 2, "epsilon_greedy geeft twee resultaten terug"
    average_rewards, true_rewards = resultaat
    assert len(average_rewards) == 50, (
        f"average_rewards moet per iteratie één waarde bevatten (50), "
        f"kreeg {len(average_rewards)}"
    )
    assert len(true_rewards) == 4, (
        f"true_rewards moet één waarde per arm bevatten (4), kreeg {len(true_rewards)}"
    )
    for waarde in average_rewards:
        assert np.isfinite(float(waarde)), "average_rewards bevatten geldige getallen"
    for waarde in true_rewards:
        assert np.isfinite(float(waarde)), "true_rewards bevatten geldige getallen"


def test_epsilon_greedy_bereik():
    """De gemiddelde rewards blijven binnen een redelijke band rond de true rewards."""
    np.random.seed(123)
    with time_limit():
        average_rewards, true_rewards = epsilon_greedy(
            arms=5, epsilon=0.1, num_iterations=200
        )
    ondergrens = float(np.min(true_rewards)) - 4.0
    bovengrens = float(np.max(true_rewards)) + 4.0
    for waarde in average_rewards:
        assert ondergrens <= float(waarde) <= bovengrens, (
            f"average_rewards {waarde} valt buiten de band "
            f"[{ondergrens:.2f}, {bovengrens:.2f}]"
        )


def test_epsilon_greedy_exploit_convergeert():
    """Met lichte exploratie komt de gemiddelde reward dicht bij de beste arm."""
    np.random.seed(42)
    epsilon = 0.1
    with time_limit():
        average_rewards, true_rewards = epsilon_greedy(
            arms=5, epsilon=epsilon, num_iterations=3000
        )
    beste = float(np.max(true_rewards))
    gem_true = float(np.mean(true_rewards))
    # verwacht evenwicht: (1 - epsilon) keer de beste arm plus epsilon keer
    # een willekeurige arm, met marge voor ruis tijdens de opstart
    verwacht = (1 - epsilon) * beste + epsilon * gem_true - 0.5
    laatste = float(average_rewards[-1])
    assert laatste >= verwacht, (
        f"met epsilon = {epsilon} moet de gemiddelde reward dicht bij de beste arm "
        f"({beste:.2f}) uitkomen, verwacht minstens {verwacht:.2f}, kreeg {laatste:.2f}"
    )


# --- Oefening 2: Gittins index ---


def test_gittins_nul_is_inf():
    """Een nooit geprobeerde arm krijgt een oneindige index."""
    with time_limit():
        index = calculate_gittins_index(0, 0, 1)
    assert index == float("inf"), (
        f"een arm met n = 0 krijgt inf, kreeg {index}"
    )


def test_gittins_formule():
    """De index volgt X/n plus de exploratiebonus met gamma = 0.9."""
    n, X, t = 10, 5.0, 100
    with time_limit():
        index = calculate_gittins_index(n, X, t)
    verwacht = X / n + math.sqrt((0.9 * math.log(t)) / (2 * n))
    assert math.isclose(index, verwacht, rel_tol=1e-9), (
        f"verwacht {verwacht}, kreeg {index}"
    )


def test_gittins_gamma_default():
    """Zonder gamma wordt 0.9 gebruikt, met een andere gamma verandert de index."""
    n, X, t = 4, 3.0, 50
    with time_limit():
        index_default = calculate_gittins_index(n, X, t)
        index_ander = calculate_gittins_index(n, X, t, gamma=0.5)
    verwacht_default = X / n + math.sqrt((0.9 * math.log(t)) / (2 * n))
    verwacht_ander = X / n + math.sqrt((0.5 * math.log(t)) / (2 * n))
    assert math.isclose(index_default, verwacht_default, rel_tol=1e-9), (
        f"standaard gamma: verwacht {verwacht_default}, kreeg {index_default}"
    )
    assert math.isclose(index_ander, verwacht_ander, rel_tol=1e-9), (
        f"gamma = 0.5: verwacht {verwacht_ander}, kreeg {index_ander}"
    )


def test_gittins_hoge_reward_hogere_index():
    """Bij dezelfde n en t geeft een hogere som X een hogere index."""
    with time_limit():
        laag = calculate_gittins_index(5, 2.0, 30)
        hoog = calculate_gittins_index(5, 8.0, 30)
    assert hoog > laag, (
        f"meer totaalbeloning geeft een hogere index ({hoog} vs {laag})"
    )


# --- GittinsAgent ---


def test_agent_initiele_toestand():
    """Een nieuwe agent start met nul tellingen, nul rewards en t = 1."""
    with time_limit():
        agent = GittinsAgent(3)
    assert agent.num_arms == 3, f"num_arms moet 3 zijn, kreeg {agent.num_arms}"
    assert list(agent.counts) == [0, 0, 0], (
        f"counts starten op nul, kreeg {list(agent.counts)}"
    )
    assert list(agent.rewards) == [0, 0, 0], (
        f"rewards starten op nul, kreeg {list(agent.rewards)}"
    )
    assert agent.t == 1, f"t start op 1, kreeg {agent.t}"


def test_agent_update():
    """update verhoogt counts, rewards en t correct."""
    with time_limit():
        agent = GittinsAgent(2)
        agent.update(1, 2.5)
    assert list(agent.counts) == [0, 1], (
        f"na één update voor arm 1: kreeg {list(agent.counts)}"
    )
    assert list(agent.rewards) == [0, 2.5], (
        f"na één update met reward 2.5: kreeg {list(agent.rewards)}"
    )
    assert agent.t == 2, f"t verhoogt met één per update, kreeg {agent.t}"


def test_select_arm_geldige_arm():
    """select_arm geeft een bestaand armnummer terug (int in [0, num_arms))."""
    with time_limit():
        agent = GittinsAgent(4)
        keuze = agent.select_arm()
    assert isinstance(keuze, (int, np.integer)), (
        f"select_arm geeft een geheel getal terug, kreeg {type(keuze).__name__}"
    )
    assert 0 <= int(keuze) < 4, f"keuze {keuze} valt buiten de arms [0, 4)"


def test_select_arm_verkiest_niet_geprobeerde_arm():
    """Een nooit geprobeerde arm (index = inf) wint van een slecht gesamplede arm."""
    with time_limit():
        agent = GittinsAgent(3)
        agent.update(0, -5.0)
        keuze = agent.select_arm()
    assert int(keuze) != 0, (
        "een nog niet geprobeerde arm heeft voorrang, maar er werd arm 0 gekozen"
    )
    assert int(keuze) in (1, 2), f"de keuze {keuze} is een geldige arm"


def test_select_arm_kiest_bestste_arm():
    """De arm met de hoogste Gittins index wordt gekozen."""
    with time_limit():
        agent = GittinsAgent(2)
        agent.update(0, 10.0)
        agent.update(0, 10.0)
        agent.update(1, 0.0)
        agent.update(1, 0.0)
        keuze = agent.select_arm()
    assert int(keuze) == 0, f"arm 0 heeft de hoogste index, kreeg arm {keuze}"
