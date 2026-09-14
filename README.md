# Floor Cleaning Agent — Model-based Reflex Agent (11-Week Course)

Een robotstofzuiger die een 10×5 tegels grote woonkamer systematisch schoonmaakt.
De agent gebruikt een **model-based reflex architectuur**: hij bouwt een intern model
van de omgeving op via sensoren (vuil-detectie, bumper) en werkt dit continu bij.

---

## 📁 Projectstructuur

```
.
├── .github/workflows/autograde.yml   # CI/CD: 11 testjobs + score berekening
├── grade.py                           # Score calculator (dynamisch, alle weken)
├── requirements.txt                   # pytest
├── README.md                          # Dit bestand
├── exercises/
│   ├── week01/                       # Week 1:  Environment + Agent init
│   │   ├── solution.py              #   Placeholder — implementeer zelf
│   │   └── test_week01.py           #   5 tests, 5 pt
│   ├── week02/                       # Week 2:  Movement (4 richtingen + muren)
│   │   ├── solution.py
│   │   └── test_week02.py           #   6 tests, 6 pt
│   ├── week03/                       # Week 3:  Cleaning (dirt sensor, clean_tile)
│   │   ├── solution.py
│   │   └── test_week03.py           #   4 tests, 4 pt
│   ├── week04/                       # Week 4:  Empty room sweep (zigzag)
│   │   ├── solution.py
│   │   └── test_week04.py           #   4 tests, 5 pt
│   ├── week05/                       # Week 5:  Bumper sensor + obstacle model
│   │   ├── solution.py
│   │   └── test_week05.py           #   4 tests, 4 pt
│   ├── week06/                       # Week 6:  Navigate around single obstacle
│   │   ├── solution.py
│   │   └── test_week06.py           #   3 tests, 4 pt
│   ├── week07/                       # Week 7:  Multiple obstacles
│   │   ├── solution.py
│   │   └── test_week07.py           #   4 tests, 5 pt
│   ├── week08/                       # Week 8:  BFS pathfinding
│   │   ├── solution.py
│   │   └── test_week08.py           #   3 tests, 5 pt
│   ├── week09/                       # Week 9:  Time-based soiling (step_time)
│   │   ├── solution.py
│   │   └── test_week09.py           #   4 tests, 6 pt
│   ├── week10/                       # Week 10: Multi-pass cleaning
│   │   ├── solution.py
│   │   └── test_week10.py           #   4 tests, 6 pt
│   └── week11/                       # Week 11: Full solution (alles gecombineerd)
│       ├── solution.py
│       └── test_week11.py           #   3 tests, 9 pt
│
Totaal: 44 tests, 59 punten
```

---

## 🧠 Architectuur (per week opgebouwd)

Elke week bouwt voort op de vorige. De `solution.py` in elke map bevat
**stub-methoden** die jij moet implementeren. De bijbehorende `test_week*.py`
testen of jouw implementatie correct is.

### Week-overzicht

| Week | Focus | Wat je leert |
|------|-------|-------------|
| 01 | Environment + Agent init | Grid, dirty tiles, position tracking, model |
| 02 | Movement | 4 richtingen, wall detection via bumper |
| 03 | Cleaning | Dirt sensor, clean_tile(), model update |
| 04 | Empty room sweep | Boustrophedon (zigzag) patroon |
| 05 | Bumper sensor | Obstacle detection, model marking |
| 06 | Single obstacle | Navigatie rond 1 obstakel |
| 07 | Multiple obstacles | Meerdere obstakels, complexe navigatie |
| 08 | BFS pathfinding | Breadth-First Search voor optimale routes |
| 09 | Time-based soiling | `step_time()`, 7-dagen vuil-cyclus |
| 10 | Multi-pass cleaning | Clean → wait → clean again |
| 11 | Full solution | Alle features samen |

---

## 🧪 Testen

### Punten per week

Elk testbestand heeft een `WEIGHTS` dictionary bovenaan. Pas deze aan om het
aantal punten per test te wijzigen:

```python
# week03/test_week03.py
WEIGHTS = {
    "test_env_clean_single_tile": 1,
    "test_agent_sense_dirt": 1,
    "test_agent_clean_tile": 1,
    "test_env_set_charger": 1,
}
```

### Lokaal testen

```bash
# Alle testen (alle weken)
uv run python -m pytest exercises/week*/test_week*.py -v

# Eén week
uv run python -m pytest exercises/week03/test_week03.py -v

# Eén specifieke test
uv run python -m pytest exercises/week03/test_week03.py::test_agent_clean_tile -v
```

### Score berekenen

```bash
# Basis (toont per-week overzicht + eindscore)
uv run python grade.py

# Gedetailleerd (toont elke test per week + status)
uv run python grade.py --verbose
```

**Voorbeeld output:**

```
========================================================================
  FLOOR CLEANING AGENT — WEEKLY PROGRESS REPORT
========================================================================

  WEEK          SCORE       PROGRESS
  ─────────────────────────────────────────────────────
  week01     5/5  pts  ████████████████████ 100.0%
  week02     4/6  pts  █████████████░░░░░░░  66.7%
  ...

  ─────────────────────────────────────────────────────
  TOTAAL    35/59 pts  ████████████░░░░░░░░  59.3%
──────────────────────────────────────────────────────────
  EINDCIFER:   35 / 59  (59.3%)
========================================================================
```

---

## 🤖 GitHub Actions Workflow

Bij elke `push` of `pull_request` worden **12 jobs** gestart:

```
test01  ✅  pytest exercises/week01/test_week01.py  (5 pt)
test02  ✅  pytest exercises/week02/test_week02.py  (6 pt)
test03  ✅  pytest exercises/week03/test_week03.py  (4 pt)
...
test11  ✅  pytest exercises/week11/test_week11.py  (9 pt)
Score   ✅  grade.py --verbose            (35/59 = 59.3%)
```

**Belangrijk:** `fail-fast: false` — als één week faalt, blijven de andere gewoon lopen.
De **Score** job start pas nadat alle testjobs klaar zijn (`needs: test`) en berekent
de gewogen score. Het resultaat verschijnt in de **Summary** tab van de workflow run
met een per-week progressieoverzicht.

---

## 🚀 Snelstart

```bash
# 1. Installeer uv (zie https://docs.astral.sh/uv/)
# 2. Maak een virtual environment en installeer dependencies
uv venv
uv pip install -r requirements.txt

# 3. Begin met week 01 — implementeer de stubs in exercises/week01/solution.py
# 4. Test je implementatie
uv run python -m pytest exercises/week01/test_week01.py -v

# 5. Ga verder naar week 02, 03, ...
# 6. Bereken de totale score
uv run python grade.py --verbose
```
