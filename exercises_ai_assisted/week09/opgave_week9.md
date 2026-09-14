# Week 9 — Oefeningen: Explore vs Exploit

## Leerdoelen
- Je begrijpt het **explore-exploit dilemma** bij multi-armed bandits.
- Je implementeert **epsilon-greedy**.
- Je implementeert de **Gittins-index**.

## Overzicht

| # | Oefening | Tijd |
|---|----------|------|
| 1 | Epsilon-greedy | 30 min |
| 2 | Gittins index | 30 min |

---

# Oefening 1: Epsilon-greedy

Open `epsilon_greedy_start.py`.

De core van het algoritme:
1. Bij elke iteratie, kies **exploit** (beste bandit) met kans `1-ε`, of **explore** (willekeurige bandit) met kans `ε`.
2. Simuleer de reward: `np.random.normal(true_rewards[arm], 1)`.
3. Update `estimated_rewards[arm]` (gemiddelde tot nu toe).
4. Houd `average_rewards` bij (cumulatief gemiddelde).

**Experimenteer met ε = 0, 0.01, 0.1, 0.5**. Wat zie je?

# Oefening 2: Gittins index

Open `gittins_start.py`.

De Gittins index voegt een **exploratiebonus** toe:

```python
if n == 0:
    return float('inf')  # nooit geprobeerd → altijd exploreren
else:
    bonus = sqrt((gamma * log(t)) / (2 * n))
    return X/n + bonus
```

Pas de code aan zodat de computer niet de hoogste `estimated_reward` kiest, maar de bandit met de **hoogste Gittins index**.

**Vraag:** is het nu nog nodig om explore en exploit te scheiden? Waarom wel/niet?

---

## Klaar?
- Commit. Kijk naar **week 10** (reinforcement learning).