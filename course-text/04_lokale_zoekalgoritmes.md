# Hoofdstuk 4: Lokale Zoekalgoritmes

## Local Search

In tegenstelling tot BFS/DFS focust local search enkel op de **eindoplossing**, niet op het pad ernaartoe.

**Kenmerken**:
- Minder geheugen
- Niet systematisch
- Vindt vaak een goede oplossing, zelfs in grote zoekruimtes
- Risico: **lokaal minimum**

---

## Verband Zoeken en Optimaliseren

Een zoekprobleem kan vaak worden geherformuleerd als optimalisatieprobleem:
- Performance metric (P uit PEAS) = **kostfunctie**
- Oplossing = minimaliseren van die functie

De **Euclidische afstand** (of kwadraat ervan) is de meest gebruikte kostfunctie:

$$\text{MSE} = \frac{1}{n}\sum_{i=1}^{n}(y_i - \hat{y}_i)^2$$

---

## Gradient Descent

Gradient descent zoekt een minimum door:
1. Partiële afgeleiden te berekenen op het huidige punt
2. Een stap in de dalende richting te zetten
3. Te stoppen wanneer er niets meer verandert

```python
def gradient_descent(initial_x, learning_rate, convergence_threshold):
    x = initial_x
    converged = False
    while not converged:
        y = cost_function(x)
        grad = gradient(x)
        new_x = x - learning_rate * grad
        if abs(new_x - x) < convergence_threshold:
            converged = True
        x = new_x
    return x
```

**Risico's**:
- **Lokaal minimum**: gradient descent is greedy en durft niet 'omhoog' te gaan
- **Learning rate**: te hoog → overshoot, te laag → traag
- **Plateau**: stilstand op vlak gebied
- **Ridge**: opeenvolging van lokale minima

---

## Gradient Descent Variaties

- **Stochastic Gradient Descent**: kies richting obv kansverdeling van gradient
- **First-choice Gradient Descent**: sample tot betere richting gevonden
- **Random Restart**: meerdere keren opnieuw starten

---

## Simulated Annealing

Combinatie van gradient descent en 'willekeurig proberen'. Af en toe 'schudden' om uit lokaal minimum te geraken.

```python
import math
import random

def simulated_annealing(initial_state, cost_function, kmax):
    s = initial_state
    s_best = s
    
    for k in range(kmax):
        T = 1 - (k + 1) / kmax  # temperatuur daalt
        s_new = random_neighbor(s)
        
        if cost_function(s_new) < cost_function(s):
            s = s_new  # altijd beter aanvaarden
        else:
            # Soms slechtere oplossing aanvaarden (kans daalt met T)
            delta = cost_function(s_new) - cost_function(s)
            P = math.exp(-delta / T)
            if random.random() < P:
                s = s_new
        
        if cost_function(s) < cost_function(s_best):
            s_best = s
    
    return s_best
```

Simulated annealing was in de jaren '80 dé techniek voor VLSI circuit layout.

---

## Discrete Problemen

Voor puzzels en spellen hebben we vaak discrete functies ('stapfuncties'). Gradient descent werkt dan niet (niet afleidbaar). In dat geval neem je de beste optie uit een eindig aantal mogelijkheden.
