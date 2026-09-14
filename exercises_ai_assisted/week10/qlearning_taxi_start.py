"""
Oefening 1: Taxi-v3 met Q-learning
====================================
"""
import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt


def train_taxi(episodes=1000):
    env = gym.make('Taxi-v3')

    # TODO: initialiseer Q-table (shape: [observation_space.n, action_space.n])
    learning_rate = 0.1
    discount_factor = 0.9
    epsilon = 0.1

    rewards = []

    for episode in range(episodes):
        state = env.reset()
        if isinstance(state, tuple):
            state = state[0]
        total_reward = 0

        for step in range(99):
            # TODO: ε-greedy actie selectie
            # TODO: voer actie uit, update Q
            pass

        rewards.append(total_reward)

    env.close()
    return rewards


def plot_rewards(rewards):
    plt.plot(rewards)
    plt.xlabel('Episode')
    plt.ylabel('Reward')
    plt.show()


if __name__ == "__main__":
    rewards = train_taxi(episodes=1000)
    print(f"Gemiddelde reward: {np.mean(rewards):.2f}")
    plot_rewards(rewards)