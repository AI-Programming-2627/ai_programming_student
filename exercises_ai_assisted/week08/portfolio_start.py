"""
Oefening 3: Portefeuille-optimalisatie ('dichtste bij')
=========================================================
"""
import numpy as np
import osqp
from scipy.sparse import csc_matrix


class PortfolioOptimizer:
    def __init__(self, expected_returns, covariance_matrix):
        self.expected_returns = np.array(expected_returns)
        self.covariance_matrix = np.array(covariance_matrix)
        self.num_assets = len(expected_returns)

    def fit(self):
        # TODO: stel P, q, A, l, u op voor OSQP
        # Minimaliseer: w.T @ cov @ w (risico)
        # Constraint: som(gewichten) = 1
        pass


if __name__ == "__main__":
    expected_returns = [0.05, 0.08, 0.1]
    covariance_matrix = np.array([[0.001, 0.0002, 0.0001],
                                  [0.0002, 0.002, 0.0003],
                                  [0.0001, 0.0003, 0.001]])

    optimizer = PortfolioOptimizer(expected_returns, covariance_matrix)
    optimal_weights = optimizer.fit()
    print("Optimale gewichten:", optimal_weights)