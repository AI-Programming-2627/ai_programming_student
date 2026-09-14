"""
Oefening 2: Gittins Index
==========================
"""
import math


def calculate_gittins_index(n, X, t, gamma=0.9):
    if n == 0:
        return float('inf')
    else:
        exploration_term = math.sqrt((gamma * math.log(t)) / (2 * n))
        return X / n + exploration_term


class GittinsAgent:
    def __init__(self, num_arms):
        self.num_arms = num_arms
        self.counts = [0] * num_arms
        self.rewards = [0] * num_arms
        self.t = 1

    def select_arm(self):
        # TODO: kies de arm met de hoogste Gittins index
        # in plaats van de hoogste gemiddelde reward
        pass

    def update(self, arm, reward):
        self.counts[arm] += 1
        self.rewards[arm] += reward
        self.t += 1


# Simpele test
if __name__ == "__main__":
    # Test Gittins index berekening
    idx = calculate_gittins_index(10, 5, 100)
    print(f"Gittins index (n=10, X=5, t=100): {idx}")