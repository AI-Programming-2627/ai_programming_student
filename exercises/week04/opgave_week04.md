# Week 4 — Oefening: Traveling Salesman met Simulated Annealing

## Leerdoelen
- Je begrijpt **local search** en **simulated annealing**.
- Je past simmulated annealing toe op het **Traveling Salesman Problem** (TSP).

## Het probleem
Een verkoper wil een aantal steden bezoeken en terugkeren naar de startstad, met een **minimale totale afstand**.  

Voor 50 steden zijn er 50! ≈ 3·10⁶⁴ mogelijke routes — exact zoeken is onmogelijk.  
We streven dus naar een **goede** oplossing met **simulated annealing**.

Je krijgt een **afstandsmatrix**: entry `(i, j)` = afstand tussen stad i en stad j.

## Overzicht

| # | Oefening | Tijd |
|---|----------|------|
| 1 | Simulated Annealing voor TSP | 60 min |
| 2 (optioneel) | Testen met echte steden | 15 min |

---

## Stappenplan

### Stap 1: Representatie
Een **tour** is een permutatie van steden: bv. `[0, 3, 1, 2]` = steden in deze volgorde bezoeken.

### Stap 2: Implementeer `total_distance(tour)`
Loop over de tour en som de afstanden op tussen opeenvolgende steden, **incl. terugkeer naar de eerste stad**.

### Stap 3: Simulated annealing kern
In `simulated_annealing()`:
1. Start met een willekeurige tour (beste tot nu toe = deze).
2. Voor `num_iterations` stappen:
   - Kies 2 willekeurige steden en **verwissel** hun positie.
   - Bereken de nieuwe afstand.
   - **Als nieuwe tour korter is**: aanvaard.
   - **Als nieuwe tour langer is**: aanvaard met kans `exp(-Δ / T)` (T = temperatuur).
   - Update temperatuur: `T *= cooling_rate`.
   - Blijf de beste tour bijhouden.
3. Return `best_tour, best_distance`.

### Stap 4: Test en experimenteer
- Test met de 4-steden matrix hieronder.
- Experimenteer met `initial_temperature`, `cooling_rate` en `num_iterations`.
- Lukt het om voor 4 steden het optimale te vinden?

---

## Testdata

```python
import numpy as np

distance_matrix = np.array([
    [0, 29, 20, 21],
    [29, 0, 15, 18],
    [20, 15, 0, 25],
    [21, 18, 25, 0]
])
```

Verwachte totale afstand (voorbeeld): ~86 (controleer of jouw oplossing dicht bij het optimum zit).