"""
Oefening 1: Epsilon-Greedy voor Multi-Armed Bandits
=====================================================
"""
import numpy as np
import matplotlib.pyplot as plt


def epsilon_greedy(arms, epsilon, num_iterations):
    num_arms = arms
    true_rewards = np.random.normal(0, 1, num_arms)
    estimated_rewards = np.zeros(num_arms)
    arm_counts = np.zeros(num_arms)
    total_reward = 0
    average_rewards = []

    for _ in range(num_iterations):
        # TODO: kies between explore en exploit
        # if np.random.rand() < epsilon: explore (random arm)
        # else: exploit (arm met hoogste estimated_rewards)

        # TODO: simuleer reward via np.random.normal(true_rewards[selected_arm], 1)
        # Update estimated_rewards[selected_arm] als gemiddelde

        total_reward += reward
        average_rewards.append(total_reward / (_ + 1))

    return average_rewards, true_rewards


def plot_results(average_rewards, true_rewards, selected_arm):
    plt.plot(average_rewards, label='Gemiddelde Reward')
    plt.plot(true_rewards[selected_arm] * np.ones_like(average_rewards),
             linestyle='--', label='True Reward (Gekozen)')
    plt.xlabel('Iteratie')
    plt.ylabel('Reward')
    plt.legend()
    plt.show()


if __name__ == "__main__":
    avg_rew, true_rew = epsilon_greedy(arms=5, epsilon=0.1, num_iterations=1000)
    plot_results(avg_rew, true_rew, np.argmax(true_rew))