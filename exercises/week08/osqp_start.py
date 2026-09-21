"""
Oefening 1: OSQP Basis
=======================
"""
import numpy as np
import osqp
from scipy.sparse import csc_matrix


def solve_qp(P, q, A, l, u):
    prob = osqp.OSQP()
    prob.setup(csc_matrix(P), q, csc_matrix(A), l, u)
    result = prob.solve()
    return result.x


if __name__ == "__main__":
    P = np.array([[4, 1], [1, 2]])
    q = np.array([1, 1])
    A = np.array([[1, 1], [-1, 2], [2, 1]])
    l = np.array([1, 0, 2])
    u = np.array([2, 2, 3])

    x = solve_qp(P, q, A, l, u)
    print("Oplossing:", x)

    # Oefening 2: Fabrieksoptimalisatie
    # TODO: stel matrices op voor het fabrieksprobleem
    # Minimaliseer -(5a + 8b) met constraints: 2a+b <= 100, a+3b <= 90, a,b >= 0