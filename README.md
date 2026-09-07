# Floor Cleaning Agent — Model-based Reflex Agent

Een robotstofzuiger die een 10×5 tegels grote woonkamer systematisch schoonmaakt.
De agent gebruikt een **model-based reflex architectuur**: hij bouwt een intern model
van de omgeving op via sensoren (vuil-detectie, bumper) en werkt dit continu bij.

---

## 📁 Projectstructuur

```
.
├── .github/workflows/autograde.yml   # CI/CD: 3 testjobs + score berekening
├── solution_floor_cleaning.py         # Oplossing: Environment + FloorCleaningAgent
├── grade.py                           # Score calculator (op basis van WEIGHTS)
├── requirements.txt                   # pytest
├── README.md                          # Dit bestand
└── tests/
    ├── test1.py                       # Basis schoonmaak (lege kamer)
    ├── test2.py                       # Obstakel detectie & navigatie
    └── test3.py                       # Tijdsgebonden terugvuiling (7 dagen)
```

---

## 🧠 Architectuur

### `Environment` — De echte wereld

```python
env = Environment(width=10, height=5)
```

| Methode | Beschrijving |
|---|---|
| `is_dirty(x, y)` | Is tegel (x, y) vuil? |
| `is_blocked(x, y)` | Wordt (x, y) geblokkeerd door een muur of obstakel? |
| `clean(x, y)` | Maak de tegel schoon op tijdstip `env.time` |
| `add_obstacle(x, y)` | Plaats een obstakel |
| `set_charger(x, y)` | Plaats het laadstation (tegel is proper) |
| `step_time(days)` | Laat de tijd `days` dagen vooruitgaan. Tegels die ≥7 dagen niet gepoetst zijn, worden opnieuw vuil. |
| `count_dirty_tiles()` | Aantal vuile tegels (excl. obstakels) |
| `count_reachable_tiles()` | Aantal bereikbare tegels (excl. obstakels) |

### `FloorCleaningAgent` — De model-based reflex agent

```python
agent = FloorCleaningAgent(environment, start_x=0, start_y=0)
```

#### Interne state

| Attribuut | Beschrijving |
|---|---|
| `x, y` | Huidige positie (start bij laadstation (0,0)) |
| `model[y][x]` | Wat de agent gelooft over elke tegel: `'unknown'`, `'clean'`, `'dirty'`, `'obstacle'`, `'charging_station'` |
| `visited[y][x]` | Of de agent de tegel al fysiek heeft bezocht |
| `last_cleaned[y][x]` | Tijdstip waarop de agent deze tegel voor het laatst heeft schoongemaakt |
| `time` | Interne teller van de agent |

#### Sensoren

| Sensor | Beschrijving |
|---|---|
| `sense_dirt()` | Checkt of de huidige tegel vuil is |
| `sense_bump(direction)` | Bumper voelt of er een muur/obstakel in `direction` (`'up'`, `'down'`, `'left'`, `'right'`) staat |

#### Transitiemodel

```python
agent.update_model()
```

Werkt de interne `model[][]` bij op basis van de sensorwaarden:
- Als `sense_dirt()` → `'dirty'`, anders `'clean'` (tenzij laadstation)
- Als `sense_bump(dir)` → de buur wordt gemarkeerd als `'obstacle'`

#### Acties

| Actie | Beschrijving |
|---|---|
| `move_up()` / `move_down()` / `move_left()` / `move_right()` | Verplaats 1 tegel (return `True` bij succes) |
| `clean_tile()` | Maak huidige tegel schoon |
| `stay()` | Doe niets (1 tijdseenheid) |

#### Strategie

De `clean()` methode gebruikt een **boustrophedon (zigzag)** patroon:

1. Rij per rij: rij 0 → rechts, rij 1 → links, rij 2 → rechts, …
2. BFS-padzoeken om rond obstakels te navigeren
3. Na alle rijen terugkeren naar het laadstation (0,0)

---

## 🧪 Testen

### Testgroepen

| Bestand | Focus | Tests | Punten |
|---|---|---|---|
| `tests/test1.py` | Basis schoonmaak (lege kamer) | 5 | 7 |
| `tests/test2.py` | Obstakel detectie & navigatie | 4 | 7 |
| `tests/test3.py` | Tijdsgebonden terugvuiling (7 dagen) | 5 | 8 |
| **Totaal** | | **14** | **22** |

### Punten toekennen aan testen

Elk testbestand heeft een `WEIGHTS` dictionary bovenaan. Pas deze aan om het aantal punten per test te wijzigen:

```python
# tests/test1.py
WEIGHTS = {
    "test_agent_initialization": 1,
    "test_single_tile_clean": 1,
    "test_move_right": 1,
    "test_move_blocked_by_wall": 1,
    "test_clean_entire_room": 3,
}
```

### Lokaal testen

```bash
# Alle testen
uv run python -m pytest tests/ -v

# Eén testbestand
uv run python -m pytest tests/test1.py -v

# Eén specifieke test
uv run python -m pytest tests/test1.py::test_move_right -v
```

### Score berekenen

```bash
# Basis (toont totaal per bestand + eindscore)
uv run python grade.py

# Gedetailleerd (toont elke test + status)
uv run python grade.py --verbose
```

---

## 🤖 GitHub Actions Workflow

Bij elke `push` of `pull_request` worden 4 jobs gestart:

```
test1  ✅  pytest tests/test1.py  (7 pt)
test2  ✅  pytest tests/test2.py  (7 pt)
test3  ✅  pytest tests/test3.py  (8 pt)
Score  ✅  grade.py               (22/22 = 100%)
```

**Belangrijk:** `fail-fast: false` — als één testgroep faalt, blijven de andere gewoon lopen.
De **Score** job start pas nadat alle testjobs klaar zijn (`needs: test`) en berekent
de gewogen score. Het resultaat verschijnt in de **Summary** tab van de workflow run.

---

## 🚀 Snelstart

```bash
# 1. Installeer uv (zie https://docs.astral.sh/uv/)
# 2. Maak een virtual environment en installeer dependencies
uv venv
uv pip install -r requirements.txt

# 3. Voer de testen uit
uv run python -m pytest tests/ -v

# 4. Bereken de score
uv run python grade.py --verbose
```
