"""
Week 10 Autograder: Q-learning (Taxi-v3 en CartPole met discretisatie).

Test de publieke interface van de oplossing van de student:
- train_taxi: geeft per episode een total reward terug
- discretize_state: zet continue states om naar discrete indices
- train_cartpole: loopt af binnen een redelijke tijd

De tests controleren enkel gedrag, niet hoe het geïmplementeerd is.
"""

import contextlib
import importlib
import multiprocessing
import threading

import numpy as np
import pytest

TAXI_PATH = "exercises_ai_assisted.week10.qlearning_taxi_start"
CARTPOLE_PATH = "exercises_ai_assisted.week10.qlearning_cartpole_start"

try:
    _taxi_mod = importlib.import_module(TAXI_PATH)
    train_taxi = _taxi_mod.train_taxi
except Exception as import_error:
    pytest.skip(
        f"qlearning_taxi_start.py kon niet geïmporteerd worden: {import_error}",
        allow_module_level=True,
    )

try:
    _cart_mod = importlib.import_module(CARTPOLE_PATH)
    discretize_state = _cart_mod.discretize_state
    train_cartpole = _cart_mod.train_cartpole
except Exception as import_error:
    pytest.skip(
        f"qlearning_cartpole_start.py kon niet geïmporteerd worden: {import_error}",
        allow_module_level=True,
    )

WEIGHTS = {
    "test_train_taxi_rewards_lengte": 2,
    "test_train_taxi_leert": 3,
    "test_discretize_state_vorm": 2,
    "test_discretize_state_monotoon": 1,
    "test_train_cartpole_loopt_af": 3,
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


def _cartpole_doel(episodes: int):
    """Doelfunctie voor de subprocess-test van train_cartpole."""
    module = importlib.import_module(CARTPOLE_PATH)
    module.train_cartpole(episodes=episodes)


# --- Oefening 1: Taxi-v3 ---


def test_train_taxi_rewards_lengte():
    """train_taxi geeft één total reward per episode terug."""
    episodes = 20
    with time_limit():
        rewards = train_taxi(episodes=episodes)
    assert rewards is not None, "train_taxi mag None niet teruggeven"
    assert len(rewards) == episodes, (
        f"rewards moet één waarde per episode bevatten ({episodes}), "
        f"kreeg {len(rewards)}"
    )
    for waarde in rewards:
        assert np.isfinite(float(waarde)), (
            "elke reward is een geldig getal"
        )


def test_train_taxi_leert():
    """Na voldoende episodes stijgt de gemiddelde reward."""
    with time_limit(60):
        rewards = train_taxi(episodes=300)
    eerste = float(np.mean(rewards[:100]))
    laatste = float(np.mean(rewards[-100:]))
    assert laatste > eerste, (
        f"de gemiddelde reward stijgt door training "
        f"(eerste 100: {eerste:.1f}, laatste 100: {laatste:.1f})"
    )


# --- Oefening 2: CartPole ---


def test_discretize_state_vorm():
    """discretize_state geeft een tuple van 4 indices binnen de bins."""
    state = [0.5, -1.0, 0.1, 2.0]
    num_bins = 10
    bins = [
        np.linspace(-4.8, 4.8, num_bins),
        np.linspace(-4, 4, num_bins),
        np.linspace(-0.418, 0.418, num_bins),
        np.linspace(-4, 4, num_bins),
    ]
    with time_limit():
        idx = discretize_state(state, bins)
    assert isinstance(idx, tuple), (
        f"discretize_state geeft een tuple terug, kreeg {type(idx).__name__}"
    )
    assert len(idx) == 4, (
        f"elke dimensie krijgt één index (4), kreeg {len(idx)}"
    )
    for i, waarde in enumerate(idx):
        assert float(waarde) == int(waarde), (
            f"index {i} is een geheel getal, kreeg {waarde}"
        )
        assert 0 <= int(waarde) < num_bins, (
            f"index {i} = {waarde} valt buiten [0, {num_bins})"
        )


def test_discretize_state_monotoon():
    """Hogere invoerwaarden geven niet-lagere indices."""
    num_bins = 10
    bins = [np.linspace(-4.8, 4.8, num_bins)]
    with time_limit():
        laag = discretize_state([-3.0], bins)
        hoog = discretize_state([3.0], bins)
    assert int(hoog[0]) >= int(laag[0]), (
        f"een grotere waarde geeft een niet-lagere index "
        f"({hoog[0]} vs {laag[0]})"
    )


def test_train_cartpole_loopt_af():
    """train_cartpole beëindigt binnen een redelijke tijd (geen infinite loop)."""
    ctx = multiprocessing.get_context("fork")
    proces = ctx.Process(target=_cartpole_doel, args=(60,))
    proces.start()
    proces.join(timeout=120)
    if proces.is_alive():
        proces.terminate()
        proces.join()
        pytest.fail("train_cartpole was na 120 s nog niet klaar")
    assert proces.exitcode == 0, (
        f"train_cartpole eindigde met exitcode {proces.exitcode}"
    )
