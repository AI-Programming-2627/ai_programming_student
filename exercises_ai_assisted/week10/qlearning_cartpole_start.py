"""
Oefening 2: CartPole met Discretisatie & Q-learning
======================================================
"""
import gymnasium as gym
import numpy as np


def discretize_state(state, state_bins):
    idx = []
    for i in range(len(state)):
        idx.append(np.digitize(state[i], state_bins[i]) - 1)
    return tuple(idx)


def train_cartpole(episodes=1000):
    env = gym.make('CartPole-v1')

    num_bins = 10
    state_bins = [
        np.linspace(-4.8, 4.8, num_bins),      # x
        np.linspace(-4, 4, num_bins),           # x'
        np.linspace(-0.418, 0.418, num_bins),   # θ
        np.linspace(-4, 4, num_bins)            # θ'
    ]

    # TODO: Q-table (vorm: (num_bins, num_bins, num_bins, num_bins, action_space.n))
    alpha = 0.1
    gamma = 0.99
    epsilon = 1.0
    epsilon_decay = 0.995
    epsilon_min = 0.01

    for episode in range(episodes):
        state = env.reset()
        if isinstance(state, tuple):
            state = state[0]
        state = discretize_state(state, state_bins)
        done = False

        while not done:
            # TODO: ε-greedy (met epsilon-decay)
            # TODO: Q-learning update
            pass

        if episode % 100 == 0:
            print(f"Episode {episode} done, epsilon = {epsilon:.3f}")

    env.close()


if __name__ == "__main__":
    train_cartpole()