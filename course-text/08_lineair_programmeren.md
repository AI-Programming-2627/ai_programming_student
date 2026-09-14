# Hoofdstuk 8: Lineair Programmeren

## Continue Zoekruimtes

Tot nu toe werkten we met **discrete** zoekruimtes (eindig aantal states). Nu kijken we naar **continue** variabelen.

We behandelen **kwadratische optimalisatiemodellen** met:
- Variabelen (dingen waarvan we de waarde willen weten)
- Een **kostfunctie** (te minimaliseren)
- **Randvoorwaarden** (gelijkheden of ongelijkheden)

---

## Voorbeeld: Kippen, Neushoorns en Geiten

Een boerderij met 12 hoofden, 38 voeten en 10 hoorns.
- k = aantal kippen (2 voeten, 0 hoorns)
- n = aantal neushoorns (4 voeten, 1 hoorn)
- g = aantal geiten (4 voeten, 2 hoorns)

```
[1 1 1]   [k]   [12]
[2 4 4] x [n] = [38]
[0 1 2]   [g]   [10]
```

Oplossing: k=5, n=4, g=3. Maar vaak zijn er **meerdere oplossingen** en extra randvoorwaarden.

---

## Algemene Vorm

$$\text{Minimaliseer: } \frac{1}{2}x^TPx + q^Tx$$

Met constraints: $l \leq Ax \leq u$

- **P** = matrix voor kwadratische kost
- **q** = vector voor lineaire kost
- **A** = constraint matrix
- **l, u** = onder- en bovengrenzen

---

## OSQP Library

OSQP (Operator Splitting Quadratic Programmer) is een library om dit soort problemen op te lossen.

```python
import numpy as np
import osqp
from scipy.sparse import csc_matrix

# P en q definiëren de kostfunctie
P = np.array([[4, 1], [1, 2]])
q = np.array([1, 1])

# A, l, u definiëren de randvoorwaarden
A = np.array([[1, 1], [-1, 2], [2, 1]])
l = np.array([1, 0, 2])
u = np.array([2, 2, 3])

# OSQP setup
prob = osqp.OSQP()
prob.setup(
    P=csc_matrix(P),
    q=q,
    A=csc_matrix(A),
    l=l,
    u=u
)

# Oplossing
result = prob.solve()
print(result.x)  # optimale waarden
```

Het moeilijkste is het **opzetten van de matrices**!

---

## Voorbeeld: Fabrieksoptimalisatie

Een bedrijf maakt twee producten:
- **AquaSparkle**: 2 eenheden X, 1 eenheid Y, winst €5
- **BioBurst**: 1 eenheid X, 3 eenheden Y, winst €8

Voorraad: 100 X, 90 Y.

```python
# Variabelen: a = aantal AquaSparkle, b = aantal BioBurst
# Kost: -(5*a + 8*b) -> minimaliseren
# Constraints:
#   2*a + b <= 100  (grondstof X)
#   a + 3*b <= 90   (grondstof Y)
#   a, b >= 0
```

---

## Toepassing: Data Fusion in Verkeerskunde

Verschillende databronnen geven restricties:
- Telco (mobiele data): overkoepelend beeld
- FCD (GPS): relatieve drukte
- Telraam: lokaal verkeer
- ANPR: nummerplaatherkenning

**Data fusion** = leg 'knikkers' op stratengrid zodat ze aan zoveel mogelijk criteria voldoen.
Technisch: een **linear optimization model met quadratic cost function**.
