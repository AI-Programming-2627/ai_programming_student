# Hoofdstuk 10: Q-Learning

## Late Rewards

Sommige problemen hebben pas een beloning helemaal op het einde:
- Mountain car: punten pas bij de vlag
- Taxichauffeur: pas betaald op bestemming
- Diploma: pas na jaren studie

**Oplossing**: gebruik **discounted rewards** (toekomstige rewards zijn minder waard).

---

## De Q-Tabel

Voor elke combinatie (observatie, actie) houden we een **Q-waarde** bij.

| Q-tabel | Actie 1 | Actie 2 | Actie 3 |
|---------|---------|---------|---------|
| Obs 1   | 0       | 0       | 0       |
| Obs 2   | 5       | -20     | 2       |
| Obs 3   | 0       | 0       | 0       |

Start met neutrale verwachtingen (alles 0).

---

## Epsilon: Explore vs Exploit

In elke fase kies je met kans **epsilon**:
- **Explore** (kans ε): kies een random actie
- **Exploit** (kans 1-ε): kies de actie met hoogste Q-waarde

---

## Q-Update Formule

$$Q(s,a) \leftarrow Q(s,a) + \alpha (r + \gamma \max_{a'} Q(s',a') - Q(s,a))$$

- $\alpha$ = learning rate
- $\gamma$ = discount factor
- $r$ = ontvangen reward
- $s'$ = nieuwe state

---

## Q-Learning in Python (Taxi-voorbeeld)

```python
import gymnasium as gym
import numpy as np

# Omgeving
env = gym.make('Taxi-v3')
Q_table = np.zeros([env.observation_space.n, env.action_space.n])

# Hyperparameters
learning_rate = 0.1
discount_factor = 0.9
num_episodes = 1000
max_steps_per_episode = 99
epsilon = 0.1

for episode in range(num_episodes):
    state = env.reset()[0]
    
    for step in range(max_steps_per_episode):
        # Explore vs exploit
        if np.random.uniform(0, 1) < epsilon:
            action = env.action_space.sample()
        else:
            action = np.argmax(Q_table[state, :])
        
        # Actie uitvoeren
        new_state, reward, terminated, truncated, _ = env.step(action)
        
        # Q-table update
        old_value = Q_table[state, action]
        next_max = np.max(Q_table[new_state, :])
        new_value = (1 - learning_rate) * old_value +                     learning_rate * (reward + discount_factor * next_max)
        Q_table[state, action] = new_value
        
        state = new_state
        if terminated or truncated:
            break
```

---

## Discretisatie

Voor continue observaties (bv. Mountain Car) moeten we **discretiseren**:

```python
def discretize_observation(observation, bins, obs_space):
    normalized = (observation - obs_space.low) / (obs_space.high - obs_space.low)
    discretized = np.floor(normalized * bins).astype(int)
    return np.clip(discretized, 0, bins - 1)

# Q-tabel voor continue ruimte
bins = [10, 10]
Q_table = np.zeros(tuple(bins) + (env.action_space.n,))
```

---

## Taxi-v3 Omgeving

De taxi moet een passagier oppikken en afzetten op de juiste plaats:
- Elke move kost -1
- Fout afzetten kost veel (straf)
- Juist afzetten geeft beloning

De Q-tabel is hier **rechtstreeks bruikbaar** (discrete states).
