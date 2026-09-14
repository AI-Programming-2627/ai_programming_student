# Hoofdstuk 11: Genetische Algoritmes

## Introductie

Genetische algoritmes (GA) zijn geïnspireerd op **natuurlijke selectie**:

```
Populatie → Evaluatie → Selectie → Mutatie → Nieuwe populatie
```

---

## Basisconcepten

- **Individu** = een kandidaat-oplossing
- **Populatie** = set van individuen
- **Fitness** = hoe goed een individu het probleem oplost
- **Selectie** = kies de beste individuen
- **Crossover** = combineer twee ouders
- **Mutatie** = willekeurige verandering

---

## OneMax Probleem

Simple voorbeeld: maximaliseer het aantal 1'en in een binaire string.

```python
import pygad
import numpy as np

def fitness_func(solution, solution_idx):
    return sum(solution)  # tel de 1'en

ga_instance = pygad.GA(
    num_generations=40,
    num_parents_mating=10,
    sol_per_pop=300,
    num_genes=100,
    fitness_func=fitness_func,
    mutation_percent_genes=5
)

ga_instance.run()
solution, solution_fitness, _ = ga_instance.best_solution()
print(f"Beste: {solution} met fitness {solution_fitness}")
```

---

## Toepassing: Tekst Genereren

Doel: een bepaalde zin genereren via evolutie.

```python
import random
import string

def generate_phrase(length):
    return ''.join(random.choice(string.printable) for _ in range(length))

def calculate_fitness(phrase, target):
    score = sum(1 for a, b in zip(phrase, target) if a == b)
    return score / len(target)

def crossover(p1, p2):
    point = random.randint(1, len(p1) - 1)
    return p1[:point] + p2[point:]

def mutate(phrase, rate):
    chars = list(phrase)
    for i in range(len(chars)):
        if random.random() < rate:
            chars[i] = random.choice(string.printable)
    return ''.join(chars)
```

---

## Toepassing: Traveling Salesman (TSP)

- **Representatie**: elk individu is een route (= volgorde van steden)
- **Fitness**: totale afstand (te minimaliseren)
- **Crossover**: Order Crossover (OX) of Partially Mapped Crossover (PMX)
- **Mutatie**: wissel twee steden

---

## Toepassing: Knapsack Probleem

- **Representatie**: binaire string (1 = voorwerp in rugzak, 0 = niet)
- **Fitness**: totale waarde, met straf bij overschrijding capaciteit
- **Crossover**: eenpunts- of meerpuntskruising
- **Mutatie**: bit-flip

---

## Toepassing: Toernooi Planner

```python
class TournamentScheduler:
    def __init__(self, n=4, population_size=100, mutation_rate=0.02):
        self.n = n
        self.population_size = population_size
        self.mutation_rate = mutation_rate
    
    def fitness(self, individual):
        score = 0
        # Check: teams niet dubbel, matchups uniek, velden niet conflicteren
        return score
    
    def genetic_algorithm(self):
        pop = self.generate_population()
        for gen in range(self.num_generations):
            pop.sort(key=self.fitness, reverse=True)
            elite = pop[:int(0.1 * self.population_size)]
            new = elite.copy()
            while len(new) < self.population_size:
                p1 = random.choice(pop[:50])
                p2 = random.choice(pop[:50])
                child = self.crossover(p1, p2)
                new.append(self.mutate(child))
            pop = new
        return pop[0]
```
