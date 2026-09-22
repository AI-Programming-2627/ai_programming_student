# Lokaal testen & beoordelen (zonder GitHub Actions)

Dit project gebruikt **`uv`** als package manager en **pytest** voor testen.  
Je kunt alle tests en de scoreberekening lokaal uitvoeren — de GitHub Actions-workflow is niet nodig.

---

## Voorbereiding

1. **`uv` installeren** – In de devcontainer is `uv` al beschikbaar.  
   Op je host: volg [https://docs.astral.sh/uv/](https://docs.astral.sh/uv/).

2. **Dependencies installeren** – Vanuit de projectroot:

   ```bash
   uv sync
   ```

   Dit installeert alle packages uit `pyproject.toml` (numpy, pytest, gymnasium, …).

---

## Eén week testen

```bash
uv run python -m pytest -v tests/test_week01.py
```

Vervang `week01` door een andere week (`week02`…`week11`). **Opgelet**, je oplossing moet de naam hebben zoals die in de `/tests` folder is gedefinieerd. Als je een andere naam gebruikt, kan je ook de naam bovenaan in de testfile aanpassen.

### Handige pytest-vlaggen

| Vlag | Doel |
|---|---|
| `-v` | Uitgebreide uitvoer |
| `--tb=short` | Kortere foutmeldingen |
| `-k "filter"` | Testen op naam filteren (bv. `-k "sort"`) |
| `-x` | Stop na eerste fout |

Voorbeeld — enkel de Floor Cleaning Agent-testen uit week 1:

```bash
uv run python -m pytest -v -k "agent" tests/test_week01.py
```

---

## Alle testen + gewogen score

Het script **`grade.py`** (in de projectroot) ontdekt alle `tests/test_week*.py`-bestanden, voert ze uit, leest de `WEIGHTS`-dict per week en berekent een totaalscore:

```bash
uv run python grade.py
```

Voor details per test:

```bash
uv run python grade.py --verbose
```

### Voorbeelduitvoer (samenvatting)

```
  ─────────────────────────────────────────────────────
  week01     5/ 7 pts  ████████░░░░░░░░░░░░  71.4%
  week02     ...
  ─────────────────────────────────────────────────────
  TOTAAL    20/59 pts  ██████░░░░░░░░░░░░░░  33.9%
  ─────────────────────────────────────────────────────
  EINDCIFER:  20 / 59  (33.9%)
```

---

## Hoe werkt het?

- `grade.py` importeert elk `tests/test_weekXX.py` en leest de **`WEIGHTS`**-dict (bijv. `{"test_insertion_sort_basic": 2}`).
- Alle testen worden via `pytest.main()` gedraaid met `--junitxml` voor een XML-rapport.
- Per geslaagde test wordt het bijbehorende gewicht opgeteld bij de totaalscore.
- Eindoordeel: `(behaalde_punten / totaal_punten) * 100`.

> Er zijn **geen GitHub Actions-variabelen nodig**. De `write_github_summary()`-functie in `grade.py` doet niets als `$GITHUB_STEP_SUMMARY` niet is ingesteld.

---

## Snelle referentie

| Commando | Wat het doet |
|---|---|
| `uv sync` | Alle dependencies installeren |
| `uv run python -m pytest -v tests/test_week01.py` | Week 1 testen |
| `uv run python -m pytest -v tests/` | Alle weken testen (zonder weging) |
| `uv run python grade.py` | Alle testen + gewogen score |
| `uv run python grade.py --verbose` | Idem, met detail per test |