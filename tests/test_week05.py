"""
Week 05 Autograder: Word Generator (GA) en Knapsack Probleem.

Test de publieke interface van de oplossing van de student:
- WordPuzzle: generate_phrase, calculate_fitness, generate_population,
  crossover, mutate, select_best, genetic_algorithm
- knapsack_start: fitness_func

De tests controleren enkel gedrag, niet hoe het geimplementeerd is.
Studentencode die crasht of infinite loopt wordt netjes afgehandeld.
"""

import contextlib
import importlib
import threading

import pytest

MODULE_WORD = "exercises_ai_assisted.week05.word_generator_start"
MODULE_KNAPSACK = "exercises_ai_assisted.week05.knapsack_start"

# ---------- veilige import van WordPuzzle ----------
try:
    _mod_word = importlib.import_module(MODULE_WORD)
    WordPuzzle = _mod_word.WordPuzzle
except Exception as import_error:
    pytest.skip(
        f"word_generator_start.py kon niet geimporteerd worden: {import_error}",
        allow_module_level=True,
    )

# ---------- veilige import van knapsack ----------
try:
    _mod_knap = importlib.import_module(MODULE_KNAPSACK)
    fitness_func = _mod_knap.fitness_func
    capaciteit = _mod_knap.capaciteit
    gewichten = _mod_knap.gewichten
    waarden = _mod_knap.waarden
    n_voorwerpen = _mod_knap.n_voorwerpen
except Exception as import_error:
    pytest.skip(
        f"knapsack_start.py kon niet geimporteerd worden: {import_error}",
        allow_module_level=True,
    )

WEIGHTS = {
    # Word Generator
    "test_wordpuzzle_initialization": 1,
    "test_generate_phrase_length": 1,
    "test_calculate_fitness_perfect": 1,
    "test_calculate_fitness_zero": 1,
    "test_calculate_fitness_partial": 1,
    "test_generate_population_size": 1,
    "test_crossover_length": 1,
    "test_crossover_inheritance": 1,
    "test_mutate_length": 1,
    "test_mutate_different": 1,
    "test_select_best": 1,
    "test_genetic_algorithm_convergence": 2,
    # Knapsack
    "test_fitness_func_valid": 2,
    "test_fitness_func_overweight": 2,
    "test_fitness_func_empty": 1,
    "test_fitness_func_optimal": 2,
}

@contextlib.contextmanager
def time_limit(seconds: int = 5):
    """Beperk de duur van een blok code (tegen infinite loops).

    Gebruikt threading.Timer omdat SIGALRM niet werkt op Windows.
    """
    timeout_triggered = False

    def _raise():
        nonlocal timeout_triggered
        timeout_triggered = True

    timer = threading.Timer(seconds, _raise)
    timer.start()
    try:
        yield
        if timeout_triggered:
            raise TimeoutError(f"code duurde te lang (>{seconds}s)")
    finally:
        timer.cancel()


# =============== Oefening 1: Word Generator ===============


def _maak_puzzle(target="test", pop_size=10, mut_rate=0.1, gen=100):
    """Hulpfunctie om een WordPuzzle te maken met korte parameters."""
    return WordPuzzle(
        target_phrase=target,
        population_size=pop_size,
        mutation_rate=mut_rate,
        num_generations=gen,
    )


def test_wordpuzzle_initialization():
    """WordPuzzle slaat de parameters correct op."""
    puzzle = _maak_puzzle("hallo", 50, 0.05, 200)
    assert puzzle.target_phrase == "hallo"
    assert puzzle.population_size == 50
    assert puzzle.mutation_rate == 0.05
    assert puzzle.num_generations == 200


def test_generate_phrase_length():
    """generate_phrase geeft een string met de gevraagde lengte."""
    puzzle = _maak_puzzle()
    with time_limit():
        phrase = puzzle.generate_phrase(10)
    assert isinstance(phrase, str), "moet een string teruggeven"
    assert len(phrase) == 10, f"verwacht lengte 10, kreeg {len(phrase)}"


def test_calculate_fitness_perfect():
    """Een perfecte match geeft fitness 1.0."""
    puzzle = _maak_puzzle("abc")
    with time_limit():
        fitness = puzzle.calculate_fitness("abc")
    assert fitness == 1.0, f"perfecte match moet 1.0 geven, kreeg {fitness}"


def test_calculate_fitness_zero():
    """Een volledig foute zin geeft fitness 0.0."""
    puzzle = _maak_puzzle("abc")
    with time_limit():
        fitness = puzzle.calculate_fitness("xyz")
    assert fitness == 0.0, f"volledig fout moet 0.0 geven, kreeg {fitness}"

def test_calculate_fitness_partial():
    """Een deels correcte zin geeft een fitness tussen 0 en 1."""
    puzzle = _maak_puzzle("abcdef")
    with time_limit():
        fitness = puzzle.calculate_fitness("abxxxx")
    verwacht = 2 / 6
    assert abs(fitness - verwacht) < 0.001, (
        f"verwacht {verwacht}, kreeg {fitness}"
    )


def test_generate_population_size():
    """generate_population geeft het juiste aantal zinnen."""
    puzzle = _maak_puzzle()
    with time_limit():
        population = puzzle.generate_population(20, 5)
    assert isinstance(population, list), "moet een list teruggeven"
    assert len(population) == 20, f"verwacht 20, kreeg {len(population)}"


def test_crossover_length():
    """Crossover geeft een kind met dezelfde lengte als de ouders."""
    puzzle = _maak_puzzle("abcdefghij")
    p1 = "aaaaaaaaaa"
    p2 = "bbbbbbbbbb"
    with time_limit():
        kind = puzzle.crossover(p1, p2)
    assert isinstance(kind, str), "moet een string teruggeven"
    assert len(kind) == len(p1), (
        f"kind heeft lengte {len(kind)}, verwacht {len(p1)}"
    )


def test_crossover_inheritance():
    """Crossover combineert karakters van beide ouders."""
    puzzle = _maak_puzzle("abcdef")
    p1 = "aaaaaa"
    p2 = "bbbbbb"
    with time_limit():
        kind = puzzle.crossover(p1, p2)
    heeft_a = "a" in kind
    heeft_b = "b" in kind
    assert heeft_a and heeft_b, (
        f"kind moet karakters van beide ouders bevatten: {kind}"
    )


def test_mutate_length():
    """Mutatie behoudt de lengte van de zin."""
    puzzle = _maak_puzzle()
    phrase = "abcdefghij"
    with time_limit():
        gemuteerd = puzzle.mutate(phrase, 0.0)
    assert len(gemuteerd) == len(phrase), (
        f"gemuteerd heeft lengte {len(gemuteerd)}, verwacht {len(phrase)}"
    )


def test_mutate_different():
    """Met rate=1.0 verandert de zin (bijna altijd)."""
    puzzle = _maak_puzzle()
    phrase = "abcdefghij"
    with time_limit():
        gemuteerd = puzzle.mutate(phrase, 1.0)
    assert gemuteerd != phrase, (
        "mutatie met rate=1.0 moet de zin veranderen"
    )


def test_select_best():
    """select_best geeft de zin met de hoogste fitness terug."""
    puzzle = _maak_puzzle("abc")
    population = ["xxx", "abc", "aaa"]
    with time_limit():
        beste = puzzle.select_best(population)
    assert beste == "abc", f"verwacht 'abc', kreeg {beste}"


def test_genetic_algorithm_convergence():
    """Het genetisch algoritme benadert de doelzin."""
    puzzle = WordPuzzle(
        target_phrase="hallo",
        population_size=50,
        mutation_rate=0.05,
        num_generations=500,
    )
    with time_limit(30):
        beste_zin = puzzle.genetic_algorithm()

    assert isinstance(beste_zin, str), (
        f"moet een string teruggeven, kreeg {type(beste_zin)}"
    )
    aantal_juist = sum(
        1 for a, b in zip(beste_zin, "hallo") if a == b
    )
    assert aantal_juist >= 2, (
        f"na 500 generaties zou de zin dichter bij 'hallo' moeten zijn, "
        f"kreeg '{beste_zin}' met {aantal_juist}/5 juist"
    )

# =============== Oefening 2: Knapsack Probleem ===============


def test_fitness_func_valid():
    """Een geldige oplossing (binnen capaciteit) krijgt positieve fitness."""
    oplossing = [0, 1, 0, 1]
    with time_limit():
        fitness = fitness_func(oplossing, 0)
    assert fitness == 90, (
        f"verwacht fitness 90, kreeg {fitness}"
    )


def test_fitness_func_overweight():
    """Een oplossing over de capaciteit krijgt een strafscore."""
    oplossing = [1, 1, 1, 1]
    with time_limit():
        fitness = fitness_func(oplossing, 0)
    assert fitness < 130, (
        f"overgewicht moet een straf krijgen, fitness {fitness} is niet "
        f"lager dan 130"
    )
    geldig = fitness_func([0, 1, 0, 1], 0)
    assert fitness < geldig, (
        f"overgewicht ({fitness}) mag niet beter zijn dan een geldige "
        f"oplossing ({geldig})"
    )


def test_fitness_func_empty():
    """Een lege oplossing (niets gekozen) geeft fitness 0."""
    oplossing = [0, 0, 0, 0]
    with time_limit():
        fitness = fitness_func(oplossing, 0)
    assert fitness == 0, (
        f"lege oplossing moet fitness 0 geven, kreeg {fitness}"
    )


def test_fitness_func_optimal():
    """De bekende optimale oplossing heeft fitness 90."""
    oplossing = [0, 1, 0, 1]
    with time_limit():
        fitness = fitness_func(oplossing, 0)
    assert fitness == 90, (
        f"optimale oplossing moet fitness 90 geven, kreeg {fitness}"
    )
