# Skill: create testset oefeningen

## Doel
Schrijf pytest-tests voor programmeeroefeningen in de centrale `tests/` map
die het gedrag van de studentenoplossing verifiëren zonder hints naar de implementatie te
geven.

## Stappenplan

### 1. Analyseer de oefening
- Lees de spec in `specs/` (indien aanwezig)
- Lees `solution.py` (de stub/oplossing) om de publieke interface te begrijpen
- Identificeer: functies, klassen, methoden, parameters, returnwaarden
- Let op: welke attributen/documentatie is **publiek** (deel van de API)?
- check dat de naamgeving van de oplossing die van de studenten wordt verwacht expliciet duidelijk is en gebruik die zelf in het testscript

### 2. Bepaal de teststrategie
- Elke test test **één concreet gedrag** (black-box)
- Gebruik enkel de publieke interface — geen `hasattr`, `inspect`, of interne attributen
- Uitzondering: als een attribuut (`grid`, `model`) de **enige manier** is om de toestand te
  controleren, mag het gelezen worden — maar niet geschreven of aangepast

### 3. Testbestand opbouwen
- Plaats het testbestand in de centrale `tests/` map met naam `test_weekXX.py`

#### a. Imports — veilig
```python
import importlib
import pytest

MODULE_PATH = "exercises_ai_assisted.weekXX.solution"

try:
    _mod = importlib.import_module(MODULE_PATH)
    func_naam = _mod.func_naam
    KlassNaam = _mod.KlassNaam
except Exception as e:
    pytest.skip(f"solution.py kon niet geïmporteerd worden: {e}",
                allow_module_level=True)
```

#### b. WEIGHTS-dictionary
```python
WEIGHTS = {
    "test_naam": 2,   # punten
}
```

#### c. Cross-platform time-out (geen SIGALRM!)
```python
import contextlib
import threading


@contextlib.contextmanager
def time_limit(seconds: int = 5):
    """Beperk de duur van een blok code (tegen infinite loops)."""
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
```

#### d. Testcases
- **Algoritmes**: basic (gewone lijsten), edge cases (leeg, 1 elem, duplicaten),
  random (vergelijken met `sorted()`)
- **Agent-klassen**: constructor, initiële toestand, mutaties, grenzen/randen

### 4. Validatie
- Test dat de test zelf werkt met een correcte oplossing
- Test dat de test faalt met een foute/ontbrekende implementatie
- Geef **geen** foutmeldingen die de implementatie verraden
  (bv. "vergeet `self.row` op 0 te zetten" is een hint)

## Wat vermijd je?
- ❌ `signal.SIGALRM` — werkt niet op Windows
- ❌ Hints in foutmeldingen ("je moet X doen")
- ❌ Meerdere asserts in één test die verschillende concepten testen
- ❌ Testen die afhangen van `print()`-output (print is voor de student)
- ❌ `monkeypatch` of `mock` tenzij de oefening dat expliciet vereist

## Sjabloon: volledig testbestand
```python
"""
Week XX Autograder: [onderwerp].

Test de publieke interface van de oplossing van de student.
De tests controleren enkel gedrag, niet hoe het geïmplementeerd is.
"""

import contextlib
import importlib
import random
import threading

import pytest

MODULE_PATH = "exercises_ai_assisted.weekXX.solution"

try:
    _mod = importlib.import_module(MODULE_PATH)
    # Vervang door effectieve functies/klassen uit de oefening
    mijn_functie = _mod.mijn_functie
    MijnKlasse = _mod.MijnKlasse
except Exception as e:
    pytest.skip(f"solution.py kon niet geïmporteerd worden: {e}",
                allow_module_level=True)

WEIGHTS = {
    "test_basis": 2,
    "test_randgevallen": 1,
}


@contextlib.contextmanager
def time_limit(seconds: int = 5):
    """Beperk de duur van een blok code (tegen infinite loops)."""
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


def test_basis():
    """Basisgedrag werkt correct."""
    with time_limit():
        resultaat = mijn_functie([3, 1, 2])
    assert resultaat == [1, 2, 3]


def test_randgevallen():
    """Randgevallen worden correct afgehandeld."""
    with time_limit():
        assert mijn_functie([]) == []
```