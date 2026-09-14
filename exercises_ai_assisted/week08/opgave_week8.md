# Week 8 — Oefeningen: Lineair Programmeren met OSQP

## Leerdoelen
- Je stelt **quadratic programming**-problemen op als matrices.
- Je gebruikt **OSQP** om optimalisaties op te lossen.
- Je lost een 'dichtste bij'-probleem op.

## Overzicht

| # | Oefening | Tijd |
|---|----------|------|
| 1 | OSQP basis | 20 min |
| 2 | Fabrieksoptimalisatie | 25 min |
| 3 | Dichtste bij (portefeuille) | 30 min |

---

## Oefening 1: OSQP Basis

Open `osqp_start.py`. OSQP lost problemen op van de vorm:

```
Minimaliseer:  ½ xᵀ P x + qᵀ x
met:           l ≤ A x ≤ u
```

Los het standaardvoorbeeld uit de cursus op:

```python
P = [[4, 1], [1, 2]]
q = [1, 1]
A = [[1, 1], [-1, 2], [2, 1]]
l = [1, 0, 2]
u = [2, 2, 3]
```

Gebruik `csc_matrix(P)` voor sparse matrices.

## Oefening 2: Fabrieksoptimalisatie

Een bedrijf maakt twee producten:
- **AquaSparkle**: 2 eenheden X, 1 eenheid Y, winst €5
- **BioBurst**: 1 eenheid X, 3 eenheden Y, winst €8

Voorraad: 100 X, 90 Y.

- Variabelen: `a` = aantal AquaSparkle, `b` = aantal BioBurst
- Kost = `-(5a + 8b)` (minimaliseren = winst max)
- Constraints: `2a + b ≤ 100`, `a + 3b ≤ 90`, `a,b ≥ 0`

Wat is de optimale productie?

## Oefening 3: Portefeuille-optimalisatie ('dichtste bij')

Open `portfolio_start.py`. Een `PortfolioOptimizer` heeft `expected_returns` en een `covariance_matrix`.  
Implementeer `fit()`:

- Minimaliseer **risico** = `wᵀ Σ w` (gewogen variantie)
- Met constraint dat som van gewichten = 1 (alles beleggen)
- Één variabele per asset, en één extra constraint: `l = u = [1]` voor som gewichten.

Dit is een 'dichtste bij'-probleem: we zoeken de portefeuille die het dichtst bij een doelrendement ligt.

---

## Klaar?
- Commit. Kijk naar **week 9** (explore vs exploit).