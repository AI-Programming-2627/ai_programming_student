# Hoofdstuk 1: Intelligente Agents

## Wat is Artificiële Intelligentie?

AI draait om **rationele entiteiten**: systemen die keuzes maken en acties ondernemen om een bepaalde performantiemetriek te maximaliseren.

- **Narrow AI**: AI die één specifieke taak goed kan (deze cursus)
- **General AI / AGI**: AI die alle menselijke intellectuele taken kan uitvoeren
- **Machine Learning**: deeldomein van AI, systemen die beter worden met ervaring
- **Deep Learning**: onderdeel van ML, gebaseerd op neurale netwerken

AI is multidisciplinair: filosofie, wiskunde, economie, neurowetenschap, psychologie, CS en linguïstiek.

---

## Het Agentenmodel

Een **agent** is een systeem dat via **sensors** informatie binnenkrijgt uit zijn omgeving. Op basis daarvan en zijn interne logica (het **agent program**) voert de agent via **actuators** acties uit.

```
Agent
  • Sensors   → observeren
  • Agent program → beslissen
  • Actuators → ageren
              ↓
         Omgeving
```

### Agent Function

Een agent wordt bepaald door zijn **agent function**. In theorie een **state-action tabel** voor elke mogelijke inputreeks.

In de praktijk is die tabel gigantisch:
- Schaken: ±10¹⁵⁴ entries (atomen in universum: ±10⁸⁰)

### Wat is AI in dit framework?

De taak van AI is een **agent program** ontwerpen dat de agent function implementeert — concrete code voor een specifieke **agent architecture**.

---

## Rationele Agents

- Handel zodanig dat de **doelfunctie** (performance measure) wordt gemaximaliseerd
- Rationeel ≠ alleswetend!
- Moet kunnen leren uit ervaring, autonoom

---

## Task Environment (PEAS)

| Component | Betekenis |
|-----------|----------|
| **P** (Performance) | Doelfunctie |
| **E** (Environment) | De wereld waarin de agent opereert |
| **A** (Actuators) | Wat het systeem kan aansturen |
| **S** (Sensors) | Wat het systeem kan waarnemen |

---

## Soorten Problemen

| As | Types |
|----|-------|
| Observeerbaarheid | Volledig vs. Partieel |
| Aantal agents | Single vs. Multi |
| Zekerheid | Deterministisch vs. Stochastisch |
| Structuur | Episodisch vs. Sequentieel |
| Tijd | Statisch vs. Dynamisch |
| Waarden | Discreet vs. Continu |

---

## Soorten Agent Programs

### 1. Simple Reflex Agents

Ageren op **huidige** sensor input, zonder geheugen.

```python
if sensor == "gras, plaats rechtdoor":
    actie = "maaien"
elif sensor == "gemaaid, plaats":
    actie = "rechtdoor"
elif sensor == "gemaaid, geen plaats":
    actie = "links"
```

### 2. Model-based Reflex Agents

Hebben een **interne state** en een **transition model**.

```python
class ModelBasedAgent:
    def __init__(self):
        self.interne_kaart = {}
    
    def update(self, sensor_input, actie):
        self.interne_kaart.update(sensor_input)
```

### 3. Goal-based & Utility Agents

Hebben een **doel** en een **utility-functie**.

```python
def utility(huidige_stad, nieuwe_stad):
    return -afstand(huidige_stad, nieuwe_stad)
```

---

## AI Geschiedenis

| Jaar | Gebeurtenis |
|------|-------------|
| 1950 | Turing Test |
| 1956 | Term 'AI' (Dartmouth) |
| 1966 | ELIZA: eerste chatbot |
| 1970s | Eerste AI Winter |
| 1997 | Deep Blue verslaat Kasparov |
| 2006 | Google Translate |
| 2011 | SIRI, Watson wint Jeopardy! |
| 2017 | AlphaGo verslaat Sedol Lee |
| 2022 | ChatGPT |
