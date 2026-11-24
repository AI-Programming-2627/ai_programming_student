"""
Week 9: lineair programmeren met OSQP (deel A) en kwadratische kost (deel B).

Opgeloste oefeningen van week 9 (zie opgave_week09_deel_a.md en opgave_week09_deel_b.md).
"""

import numpy as np
import osqp
from scipy.sparse import csc_matrix

POSITIEF = np.inf
NEGATIEF = -np.inf


def _solve(P: np.ndarray, q: np.ndarray, A: np.ndarray, l: np.ndarray, u: np.ndarray) -> np.ndarray:
    """Los een kwadratisch probleem op met OSQP.

    Returns:
        de optimale waarden van x, of None wanneer er geen oplossing is.
    """
    prob = osqp.OSQP()
    prob.setup(P=csc_matrix(P), q=q, A=csc_matrix(A), l=l, u=u, verbose=False)
    prob.settings.eps_abs = 1e-8
    prob.settings.eps_rel = 1e-8
    prob.settings.polishing = True
    prob.settings.max_iter = 10000
    result = prob.solve()
    if result.info.status in ("primal infeasible", "dual infeasible"):
        return None
    return result.x


# =============== Oefening 1: OSQP basis ===============


def solve_qp(P: np.ndarray, q: np.ndarray, A: np.ndarray, l: np.ndarray, u: np.ndarray) -> np.ndarray:
    """Los een kwadratisch probleem op met OSQP.

    Minimaliseer 0.5 * x.T @ P @ x + q.T @ x met l <= A @ x <= u.

    Parameters:
        P: kwadratische kostmatrix.
        q: lineaire kostvector.
        A: constraintmatrix.
        l: ondergrenzen van A @ x.
        u: bovengrenzen van A @ x.

    Returns:
        de optimale waarden van x.
    """
    return _solve(P, q, A, l, u)


# =============== Oefening 2: Gx <= h omzetten ===============


def solve_linear(c: np.ndarray, G: np.ndarray, h: np.ndarray) -> np.ndarray:
    """Los een lineair probleem met bovenlimieten op.

    Minimaliseer c.T @ x met G @ x <= h en x >= 0.

    Parameters:
        c: lineaire kostvector.
        G: constraintmatrix voor de bovenlimieten.
        h: bovenlimieten van G @ x.

    Returns:
        de optimale waarden van x.
    """
    num_vars = G.shape[1]
    P = np.zeros((num_vars, num_vars))

    A = np.vstack([G, np.identity(num_vars)])
    l = np.concatenate([np.full(G.shape[0], NEGATIEF), np.zeros(num_vars)])
    u = np.concatenate([h, np.full(num_vars, POSITIEF)])

    return _solve(P, c, A, l, u)


# =============== Oefening 3: Fabrieksoptimalisatie ===============


class FabriekOptimizer:
    """Bereken het optimale productieplan voor twee producten."""

    def __init__(self, x_limit: float = 100.0, y_limit: float = 90.0,
                 profit_a: float = 5.0, profit_b: float = 8.0):
        self.x_limit = x_limit
        self.y_limit = y_limit
        self.profit_a = profit_a
        self.profit_b = profit_b

    def optimize(self) -> tuple[float, float]:
        """Bereken het aantal AquaSparkles en BioBursts met maximale winst.

        Returns:
            het aantal AquaSparkles en BioBursts.
        """
        q = -np.array([self.profit_a, self.profit_b])
        P = np.zeros((2, 2))

        A_grondstoffen = np.array([[2.0, 1.0], [1.0, 3.0]])
        A = np.vstack([A_grondstoffen, np.identity(2)])

        l = np.array([NEGATIEF, NEGATIEF, 0.0, 0.0])
        u = np.array([self.x_limit, self.y_limit, POSITIEF, POSITIEF])

        x = _solve(P, q, A, l, u)
        return float(x[0]), float(x[1])


# =============== Oefening 4: Macronutriënten ===============


def maaltijd_matrices(nutriënten: np.ndarray, doelen: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Zet een kostenfunctie om naar de matrices P en q.

    Minimaliseer ||doelen - N x||², met N de nutriëntmatrix.

    Parameters:
        nutriënten: matrix N, één rij per macro en één kolom per ingrediënt.
        doelen: gewenste hoeveelheden per macro.

    Returns:
        de kwadratische matrix P en de lineaire vector q.
    """
    N = np.asarray(nutriënten, dtype=float)
    t = np.asarray(doelen, dtype=float)
    P = 2.0 * (N.T @ N)
    q = -2.0 * (N.T @ t)
    return P, q


def optimize_meal(nutriënten: np.ndarray, doelen: np.ndarray,
                  grenzen: list, totaal: float = 7.0) -> np.ndarray:
    """Bereken de optimale hoeveelheid per ingrediënt.

    Parameters:
        nutriënten: matrix N, één rij per macro en één kolom per ingrediënt.
        doelen: gewenste hoeveelheden per macro.
        grenzen: per ingrediënt een (min, max) paar.
        totaal: de totale som van de hoeveelheden.

    Returns:
        de optimale hoeveelheden per ingrediënt.
    """
    P, q = maaltijd_matrices(nutriënten, doelen)

    num_vars = len(grenzen)
    mins = np.array([g[0] for g in grenzen], dtype=float)
    maxs = np.array([g[1] for g in grenzen], dtype=float)

    A = np.vstack([np.ones((1, num_vars)), np.identity(num_vars)])
    l = np.concatenate([[totaal], mins])
    u = np.concatenate([[totaal], maxs])

    return _solve(P, q, A, l, u)


# =============== Oefening 6: Trainingstijd verdelen ===============


def verdeling_matrices(doelen: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Zet een kostenfunctie om naar de matrices P en q.

    Minimaliseer ||x - doelen||², met evenveel variabelen als doelen.

    Parameters:
        doelen: gewenste waarden per variabele (doelvector t).

    Returns:
        de kwadratische matrix P en de lineaire vector q.
    """
    t = np.asarray(doelen, dtype=float)
    n = t.size
    P = 2.0 * np.identity(n)
    q = -2.0 * t
    return P, q


def optimaliseer_verdeling(doelen: np.ndarray, grenzen: list, totaal: float) -> np.ndarray:
    """Bereken de verdeling die zo dicht mogelijk bij de doelen ligt.

    Minimaliseer ||x - doelen||² met als randvoorwaarden som(x) = totaal en
    grenzen[min_i] <= x_i <= grenzen[max_i].

    Parameters:
        doelen: gewenste waarden per variabele (doelvector t).
        grenzen: per variabele een (min, max) paar.
        totaal: de vereiste totale som van de variabelen.

    Returns:
        de optimale waarden per variabele.
    """
    P, q = verdeling_matrices(doelen)

    num_vars = len(doelen)
    mins = np.array([g[0] for g in grenzen], dtype=float)
    maxs = np.array([g[1] for g in grenzen], dtype=float)

    A = np.vstack([np.ones((1, num_vars)), np.identity(num_vars)])
    l = np.concatenate([[totaal], mins])
    u = np.concatenate([[totaal], maxs])

    return _solve(P, q, A, l, u)


# =============== Oefening 5: Portefeuille-optimalisatie ===============


class PortfolioOptimizer:
    """Minimaliseer het risico van een portefeuille met OSQP."""

    def __init__(self, expected_returns: np.ndarray, covariance_matrix: np.ndarray):
        self.expected_returns = np.asarray(expected_returns, dtype=float)
        self.covariance_matrix = np.asarray(covariance_matrix, dtype=float)
        self.num_assets = len(self.expected_returns)

    def fit(self) -> np.ndarray:
        """Bereken de optimale gewichten van de portefeuille.

        Minimaliseer w.T @ cov @ w met als randvoorwaarden som(w) = 1 en
        0 <= w_i <= 1.

        Returns:
            de optimale gewichten w.
        """
        n = self.num_assets
        P = 2.0 * self.covariance_matrix
        q = np.zeros(n)

        A = np.vstack([np.ones((1, n)), np.identity(n)])
        l = np.concatenate([[1.0], np.zeros(n)])
        u = np.concatenate([[1.0], np.ones(n)])

        return _solve(P, q, A, l, u)


if __name__ == "__main__":
    print("=== Oefening 1: OSQP basis ===")
    x1 = solve_qp(np.array([[4, 1], [1, 2]]), np.array([1, 1]),
                  np.array([[1, 1], [-1, 2], [2, 1]]),
                  np.array([1, 0, 2]), np.array([2, 2, 3]))
    print(np.round(x1, 3))

    print("=== Oefening 3: Fabriek ===")
    a, b = FabriekOptimizer().optimize()
    print(f"a = {a:.1f}, b = {b:.1f}")

    print("=== Oefening 4: Macronutriënten ===")
    N_data = np.array([[2.8, 29, 2], [7, 0, 17], [0.4, 7, 0.1]])
    doelen_data = np.array([37, 41, 20])
    grenzen_data = [(2.0, 3.0), (1.0, 2.0), (2.0, 4.0)]
    x4 = optimize_meal(N_data, doelen_data, grenzen_data)
    print(np.round(x4, 2))

    print("=== Oefening 5: Portefeuille ===")
    cov = np.array([[0.001, 0.0002, 0.0001],
                    [0.0002, 0.002, 0.0003],
                    [0.0001, 0.0003, 0.001]])
    w = PortfolioOptimizer([0.05, 0.08, 0.1], cov).fit()
    print(np.round(w, 3))

    print("=== Oefening 6: Trainingstijd verdelen ===")
    doelen_data = np.array([8, 6, 5, 6, 5])
    grenzen_data6 = [(0.0, 10.0)] * 5
    x6 = optimaliseer_verdeling(doelen_data, grenzen_data6, 25.0)
    print(np.round(x6, 3))
