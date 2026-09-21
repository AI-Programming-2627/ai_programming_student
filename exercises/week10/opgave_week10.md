# Week 10 — Oefeningen: Reinforcement Learning met Q-Learning

## Leerdoelen
- Je begrijpt het **Q-learning** algoritme.
- Je implementeert Q-learning in een **Gymnasium** omgeving.
- Je past **explore vs exploit** toe met epsilon-decay.

## Overzicht

| # | Oefening | Tijd |
|---|----------|------|
| 1 | Taxi-v3 met Q-learning | 45 min |
| 2 | CartPole (discretisatie) | 45 min |

---

# Oefening 1: Taxi-v3

Open `qlearning_taxi_start.py`. De Q-learning update formule:

```
Q(s,a) ← Q(s,a) + α · (r + γ · max Q(s',a') - Q(s,a))
```

Implementeer:
1. Zet de Q-tabel op: `np.zeros([env.observation_space.n, env.action_space.n])`.
2. Voor elke episode: reset de omgeving, bepaal state (als tuple: pak `[0]`).
3. In elke stap: kies actie (ε-greedy: explore willekeurig, exploit `argmax Q[state]`).
4. Voer actie uit, krijg `new_state, reward, terminated, truncated`.
5. Update Q-tabel met de formule.
6. Als `terminated or truncated`: break.

**Test:** Hoeveel episodes nodig voor een gemiddelde reward > 0?

# Oefening 2: CartPole (uitbreiding)

Open `qlearning_cartpole_start.py`. Voor CartPole zijn de states **continu** → **discretiseer** ze.

## Stappenplan
1. Bepaal bins per dimensie (position, velocity, angle, angular velocity).
2. `discretize_state(state)`: zet continue waarden om naar discrete indices.
3. Q-tabel: `np.zeros(bins + [action_space.n])`.
4. Voeg **epsilon-decay** toe: begin ε=1.0, daalt met factor 0.995 per episode, min 0.01.
5. Train 1000 episodes. Print elke 100 episodes een update.

---

## Klaar?
- Commit. Kijk naar **week 11** (LLM agents).