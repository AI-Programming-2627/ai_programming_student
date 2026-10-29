"""
Week 5 — Oplossing: Genetische Algoritmes
==========================================
Oefening 1: Word Generator (handgeschreven GA, geen pygad).
Oefening 2: Knapsack probleem met een handgeschreven GA, geen pygad.
"""
import random
import string

import numpy as np


# =============== Oefening 1: Word Generator ===============

class WordPuzzle:
    """Een genetisch algoritme dat een willekeurige zin naar een doelzin
    laat evolueren.

    Args:
        target_phrase: de zin waarnaartoe geëvolueerd wordt.
        population_size: aantal individuen per generatie.
        mutation_rate: kans dat een karakter muteert (tussen 0 en 1).
        num_generations: aantal generaties dat het algoritme draait.
    """

    def __init__(self,
                 target_phrase: str,
                 population_size: int = 100,
                 mutation_rate: float = 0.01,
                 num_generations: int = 10000):
        self.target_phrase = target_phrase
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.num_generations = num_generations

    def generate_phrase(self, length: int) -> str:
        """Genereer een willekeurige zin van een opgegeven lengte.

        Args:
            length: het aantal karakters van de zin.

        Returns:
            Een string van `length` willekeurige karakters uit
            ``string.printable``.
        """
        return ''.join(random.choice(string.printable) for _ in range(length))

    def calculate_fitness(self, phrase: str) -> float:
        """Bereken de fitness van een zin.

        Args:
            phrase: de zin waarvan de fitness berekend wordt.

        Returns:
            Het aandeel (tussen 0.0 en 1.0) van karakters die op de juiste
            positie staan, vergeleken met ``self.target_phrase``.
        """
        if not self.target_phrase:
            return 0.0
        juiste_posities = sum(
            a == b for a, b in zip(phrase, self.target_phrase)
        )
        return juiste_posities / len(self.target_phrase)

    def generate_population(self, size: int, phrase_length: int) -> list:
        """Genereer een populatie van willekeurige zinnen.

        Args:
            size: het aantal individuen in de populatie.
            phrase_length: de lengte van elke zin.

        Returns:
            Een lijst met `size` willekeurige zinnen.
        """
        return [self.generate_phrase(phrase_length) for _ in range(size)]

    def crossover(self, phrase1: str, phrase2: str) -> str:
        """Combineer twee zinnen tot één kind.

        Er wordt een willekeurig knippunt gekozen; het eerste deel komt van
        ``phrase1``, het tweede deel van ``phrase2``.

        Args:
            phrase1: de eerste ouder.
            phrase2: de tweede ouder.

        Returns:
            Het kind, een combinatie van beide ouders.
        """
        knippunt = random.randint(1, len(phrase1) - 1)
        return phrase1[:knippunt] + phrase2[knippunt:]

    def mutate(self, phrase: str, rate: float) -> str:
        """Pas mutatie toe op een zin.

        Args:
            phrase: de zin die muteert.
            rate: kans per karakter om te vervangen (tussen 0 en 1).

        Returns:
            De gemuteerde zin, met dezelfde lengte.
        """
        resultaat = []
        for teken in phrase:
            if random.random() < rate:
                resultaat.append(random.choice(string.printable))
            else:
                resultaat.append(teken)
        return ''.join(resultaat)

    def select_best(self, population: list) -> str:
        """Selecteer de beste zin uit een populatie.

        Args:
            population: een lijst van zinnen.

        Returns:
            De zin met de hoogste fitness.
        """
        return max(population, key=self.calculate_fitness)

    def genetic_algorithm(self) -> str:
        """Voer het genetisch algoritme uit.

        Per generatie wordt de populatie op fitness gesorteerd, worden de
        beste individuen geselecteerd en via crossover + mutatie nieuwe
        generaties gebouwd. Het beste individu ooit wordt teruggegeven.

        Returns:
            De beste gevonden zin.
        """
        lengte = len(self.target_phrase)
        populatie = self.generate_population(self.population_size, lengte)
        beste_zin = self.select_best(populatie)
        beste_fitness = self.calculate_fitness(beste_zin)

        for _ in range(self.num_generations):
            populatie.sort(key=self.calculate_fitness, reverse=True)
            if self.calculate_fitness(populatie[0]) > beste_fitness:
                beste_zin = populatie[0]
                beste_fitness = self.calculate_fitness(beste_zin)
                if beste_fitness == 1.0:
                    break

            # Elitisme: de beste helft wordt ouder
            aantal_ouders = max(2, self.population_size // 2)
            ouders = populatie[:aantal_ouders]

            volgende: list[str] = []
            while len(volgende) < self.population_size:
                p1, p2 = random.sample(ouders, 2)
                kind = self.crossover(p1, p2)
                kind = self.mutate(kind, self.mutation_rate)
                volgende.append(kind)
            populatie = volgende

        return beste_zin


# =============== Oefening 2: Knapsack Probleem ===============

capaciteit = 10
gewichten = np.array([5, 4, 6, 3])
waarden = np.array([10, 40, 30, 50])
n_voorwerpen = len(gewichten)

# GA-parameters
sol_per_pop = 100
num_generations = 100
mutation_percent_genes = 10


def fitness_func(solution, solution_idx: int = 0) -> float:
    """Bereken de fitness van een knapsack-oplossing.

    Args:
        solution: een binaire vector, 1 = voorwerp zit in de rugzak.
        solution_idx: index van de oplossing (niet gebruikt, maar bewaard
            voor compatibiliteit met de oproepvorm van pygad).

    Returns:
        De totale waarde als het totale gewicht binnen de capaciteit blijft,
        anders een lage strafscore (waarde - 1000).
    """
    totaal_gewicht = float(np.dot(solution, gewichten))
    totaal_waarde = float(np.dot(solution, waarden))
    if totaal_gewicht > capaciteit:
        return totaal_waarde - 1000
    return totaal_waarde


def genereer_populatie(grootte: int) -> list[np.ndarray]:
    """Maak een willekeurige startpopulatie van binaire strings.

    Args:
        grootte: het aantal individuen.

    Returns:
        Een lijst van binaire numpy-arrays.
    """
    return [
        np.random.randint(2, size=n_voorwerpen)
        for _ in range(grootte)
    ]


def crossover(parent1: np.ndarray, parent2: np.ndarray) -> np.ndarray:
    """Combineer twee voorouders tot een kind (1-punts crossover).

    Args:
        parent1: eerste ouder (binaire array).
        parent2: tweede ouder (binaire array).

    Returns:
        Een nieuw kind dat het begin van `parent1` en het einde van
        `parent2` erft.
    """
    knippunt = random.randint(1, n_voorwerpen - 1)
    return np.concatenate([parent1[:knippunt], parent2[knippunt:]])


def mutate(individu: np.ndarray, percentage: float) -> np.ndarray:
    """Keer elk gen met een bepaalde kans om.

    Args:
        individu: een binaire array.
        percentage: de kans (%) dat een gen muteert (0-100).

    Returns:
        Het (eventueel) gemuteerde individu.
    """
    for i in range(len(individu)):
        if random.random() < percentage / 100:
            individu[i] = 1 - individu[i]
    return individu


def selecteer_beste(populatie: list[np.ndarray]) -> float:
    """Geef de hoogste fitness uit een populatie terug.

    Args:
        populatie: een lijst van binaire arrays.

    Returns:
        De hoogste fitnesswaarde.
    """
    return max(fitness_func(ind) for ind in populatie)


def los_op() -> float:
    """Los het knapsack probleem op met een handgeschreven GA.

    Returns:
        De beste gevonden totale waarde.
    """
    populatie = genereer_populatie(sol_per_pop)
    beste_fitness = selecteer_beste(populatie)

    for _ in range(num_generations):
        # Selectie: sorteer op fitness en neem de beste helft als ouders
        populatie.sort(key=fitness_func, reverse=True)
        beste_fitness = max(beste_fitness, fitness_func(populatie[0]))
        aantal_ouders = max(2, sol_per_pop // 2)
        ouders = populatie[:aantal_ouders]

        volgende: list[np.ndarray] = []
        while len(volgende) < sol_per_pop:
            p1, p2 = random.sample(ouders, 2)
            kind = crossover(p1, p2)
            kind = mutate(kind, mutation_percent_genes)
            volgende.append(kind)
        populatie = volgende

    return beste_fitness


def main() -> None:
    """Demo: evolueer een doelzin en los het knapsack-probleem op."""
    doelzin = "De basiswetten van de robotica werden ontwikkeld door Asimov"
    puzzel = WordPuzzle(doelzin)
    beste_zin = puzzel.genetic_algorithm()
    print(f"Beste zin: {beste_zin}")

    beste_waarde = los_op()
    print(f"Beste gevonden knapsack-waarde: {beste_waarde}")


if __name__ == "__main__":
    main()
