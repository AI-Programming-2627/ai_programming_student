"""
Week 08 Autograder: Lineair Programmeren met OSQP (portefeuille).

Test de publieke interface van de oplossing van de student:
- PortfolioOptimizer: __init__, fit

De tests controleren enkel gedrag, niet hoe het geïmplementeerd is.
De verwachte oplossing wordt berekend via de KKT-voorwaarden van het
probleem 'minimaliseer wᵀ Σ w met som(w) = 1'.
"""

import contextlib
import importlib
import threading

import numpy as np
import pytest

MODULE_PATH = "exercises.week08.portfolio_start"

try:
    _mod = importlib.import_module(MODULE_PATH)
    PortfolioOptimizer = _mod.PortfolioOptimizer
except Exception as import_error:
    pytest.skip(
        f"portfolio_start.py kon niet geïmporteerd worden: {import_error}",
        allow_module_level=True,
    )

WEIGHTS = {
    "test_fit_geeft_gewichten": 1,
    "test_fit_som_gewichten": 2,
    "test_fit_minimaal_risico": 3,
    "test_fit_twee_assets": 2,
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


def min_variance_weights(covariance: np.ndarray) -> np.ndarray:
    """Analytisch minimum-variantie-portefeuille (KKT) als referentie.

    Loss 2 Σ w = λ 1 met 1ᵀ w = 1, met lichte reguliering tegen
    singuliere matrices.
    """
    cov = np.array(covariance, dtype=float)
    n = cov.shape[0]
    cov_reg = cov + 1e-9 * np.eye(n)
    ones = np.ones(n)
    w = np.linalg.solve(cov_reg, ones)
    return w / np.sum(w)


COV_3 = np.array([
    [0.001, 0.0002, 0.0001],
    [0.0002, 0.002, 0.0003],
    [0.0001, 0.0003, 0.001],
])
RET_3 = [0.05, 0.08, 0.1]


def test_fit_geeft_gewichten():
    """fit geeft een vector met één gewicht per asset terug."""
    optimizer = PortfolioOptimizer(RET_3, COV_3)
    with time_limit():
        gewichten = optimizer.fit()
    assert gewichten is not None, "fit mag None niet teruggeven"
    gewichten = np.asarray(gewichten, dtype=float).ravel()
    assert len(gewichten) == 3, (
        f"fit moet één gewicht per asset geven (3), kreeg {len(gewichten)}"
    )


def test_fit_som_gewichten():
    """De som van de gewichten is 1 (alles beleggen)."""
    optimizer = PortfolioOptimizer(RET_3, COV_3)
    with time_limit():
        gewichten = np.asarray(optimizer.fit(), dtype=float).ravel()
    assert abs(np.sum(gewichten) - 1.0) < 1e-3, (
        f"som van de gewichten moet 1 zijn, kreeg {np.sum(gewichten)}"
    )


def test_fit_minimaal_risico():
    """De gevonden portefeuille heeft (bijna) het laagst mogelijke risico."""
    optimizer = PortfolioOptimizer(RET_3, COV_3)
    with time_limit():
        gewichten = np.asarray(optimizer.fit(), dtype=float).ravel()

    cov = COV_3
    risico_student = float(gewichten @ cov @ gewichten)
    risico_ref = float(min_variance_weights(cov) @ cov @ min_variance_weights(cov))
    # Eén gelijke-verdeling-portefeuille als extra ijkpunt
    w_gelijk = np.ones(3) / 3
    risico_gelijk = float(w_gelijk @ cov @ w_gelijk)

    assert risico_student <= risico_gelijk + 1e-9, (
        "risico mag niet slechter zijn dan een gelijke verdeling"
    )
    assert risico_student <= risico_ref + 1e-5, (
        f"risico {risico_student} is hoger dan het optimum {risico_ref}"
    )


def test_fit_twee_assets():
    """Met twee assets worden geldige, risicominaliserende gewichten gegeven."""
    cov_2 = np.array([[0.01, 0.002], [0.002, 0.04]])
    ret_2 = [0.03, 0.07]
    optimizer = PortfolioOptimizer(ret_2, cov_2)
    with time_limit():
        gewichten = np.asarray(optimizer.fit(), dtype=float).ravel()

    assert len(gewichten) == 2, "één gewicht per asset verwacht"
    assert abs(np.sum(gewichten) - 1.0) < 1e-3, "som van de gewichten moet 1 zijn"
    assert np.all(gewichten >= -1e-6), "gewichten mogen niet sterk negatief zijn"

    ref = min_variance_weights(cov_2)
    assert np.allclose(gewichten, ref, atol=1e-3), (
        f"verwacht {ref}, kreeg {gewichten}"
    )
