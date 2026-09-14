# Hoofdstuk 9: Reinforcement Learning

## Introductie

In RL kent de agent de **spelregels niet**, maar heeft wel toegang tot een **beloningsfunctie** (reward).

```
Omgeving → reward
  ↑
Agent → actie
```

RL bevindt zich op de kruising van supervised en unsupervised learning.

**Toepassingen**:
- Robot leren stappen (beloning als hij sneller wordt)
- Energiebeheer (beloning bij minder energieverlies)
- Chatbots: thumbs up/down als feedback

---

## Passief vs Actief Leren

| Type | Beschrijving |
|------|-------------|
| **Passief** | Model ondergaat wat er gebeurt (zoals video kijken) |
| **Actief** | Model beslist zelf welke stappen te nemen |

---

## Explore vs Exploit

**Explore** = nieuwe opties proberen om informatie te verkrijgen
**Exploit** = de beste gekende optie kiezen

**Voorbeeld**: restaurantkeuze — probeer je een nieuw restaurant (explore) of ga je naar je favoriet (exploit)?

---

## Multi-Armed Bandits

Stel: een casino heeft meerdere one-armed bandits. Elke machine heeft een vaste payout-rate, maar die ken je niet.

Strategie:
1. Houd per machine het aantal pogingen en winsten bij
2. Maak een **schatting** van de payout rate
3. Combineer explore (nieuwe machines) en exploit (beste machine)

### Epsilon-Greedy Algoritme

```python
import numpy as np

def epsilon_greedy(num_arms, num_iterations, epsilon):
    true_rewards = np.random.normal(0, 1, num_arms)
    estimated_rewards = np.zeros(num_arms)
    arm_counts = np.zeros(num_arms)
    
    for _ in range(num_iterations):
        if np.random.rand() < epsilon:
            # Explore: kies willekeurig
            arm = np.random.randint(num_arms)
        else:
            # Exploit: kies beste
            arm = np.argmax(estimated_rewards)
        
        # Simuleer spelen
        reward = np.random.normal(true_rewards[arm], 1)
        arm_counts[arm] += 1
        # Update schatting
        estimated_rewards[arm] += (reward - estimated_rewards[arm]) / arm_counts[arm]
```

---

### Gittins Index

Een meer geavanceerde oplossing: de **Gittins index** (John Gittins, 1979).

Berekening gebruikt **discounting**: een win vandaag is meer waard dan een win morgen.

```python
def calculate_gittins_index(n, X, t, gamma):
    if n == 0:
        return float('inf')  # ongeteste machine blijft interessant
    else:
        exploration_term = math.sqrt((gamma * math.log(t)) / (2 * n))
        return X / n + exploration_term
```

Kies telkens de bandit met de hoogste Gittins index.

---

## Explore vs Exploit in het Dagelijks Leven

**Explore**: studeren, investeren, lange termijn doelen
**Exploit**: pluk de dag, korte termijn beloningen

- Begin van een citytrip: alles ontdekken (explore)
- Laatste dag: terug naar het beste restaurant (exploit)
- Begin van carrière: veel proberen; later: bij goede job blijven
