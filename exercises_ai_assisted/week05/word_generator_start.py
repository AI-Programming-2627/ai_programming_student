"""
Oefening 1: Word Generator (Genetisch Algoritme)
==================================================
Evolueer een populatie van willekeurige zinnen naar een doelzin.
"""
import random
import string


class WordPuzzle:
    def __init__(self, target_phrase, population_size=100, mutation_rate=0.01, num_generations=10000):
        self.target_phrase = target_phrase
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.num_generations = num_generations

    def generate_phrase(self, length):
        pass

    def calculate_fitness(self, phrase):
        pass

    def generate_population(self, size, phrase_length):
        pass

    def crossover(self, phrase1, phrase2):
        pass

    def mutate(self, phrase, rate):
        pass

    def select_best(self, population):
        pass

    def genetic_algorithm(self):
        pass


def main():
    target_phrase = "De basiswetten van de robotica werden ontwikkeld door Asimov"
    puzzle = WordPuzzle(target_phrase)
    best_phrase = puzzle.genetic_algorithm()
    print(f"Beste zin: {best_phrase}")


if __name__ == "__main__":
    main()