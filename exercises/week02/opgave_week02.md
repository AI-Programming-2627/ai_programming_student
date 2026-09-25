# Week 2 — Oefeningen: Zoekalgoritmes & Agenten

## Leerdoelen
- Je implementeert een **model-based reflex agent** (self-driving car).
- Je implementeert **Breadth-First Search** met pad-printing.
- Je lost een **sliding puzzle** op met BFS/DFS.

## Overzicht

| # | Oefening | Tijd |
|---|----------|------|
| 1 | Self-Driving Car (reflex agent) | 30 min |
| 2 | Breadth-First Search | 30 min |
| 3 | Sliding Puzzle | 45 min |

---

# Oefening 1: Self-Driving Car (model-based reflex)

Open `selfdriving_car_start.py`. Je vindt de klassen `LidarSensorInput`, `Brake`, `Nothing` en `Agent`.

De self-driving car moet zijn voorligger volgen op **10m afstand**.  
De LIDAR sensor geeft elke stap de afstand tot de voorligger.  
**Remmen** is nodig als de tijd tot botsing < 5 seconden is.

## Stappenplan

### Stap 1: Bepaal de relatieve snelheid
De agent moet de **relatieve snelheid** kennen. Dat kan door het verschil te nemen tussen de vorige en huidige meting (`Δafstand / Δt`).  
Je hebt dus een **interne state** nodig: onthoud de vorige afstand.

### Stap 2: Implementeer `__init__`
Welke variabele(n) moet de agent onthouden? Voeg ze toe in de constructor.

### Stap 3: Implementeer `process(p)`
- Lees `p.DistanceTo` uit de LIDAR.
- Bereken snelheid = vorige_afstand - huidige_afstand (positief = voorligger rijdt weg, negatief = voorligger komt dichter).
- Schat tijd tot botsing: als snelheid > 0, dan `tijd = afstand / snelheid`.
- Als tijd < 5 seconden: `return Brake()`, anders `return Nothing()`.
- Update de opgeslagen afstand.

### Stap 4: Test met de meegeleverde code

---

# Oefening 2: Breadth-First Search

Open `breadth_first_start.py`. Het bestand bevat de klassen `State`, `Node` en een `breadth_first_search(initial_node, goal_state)` functie-skelet.

## Stappenplan

### Stap 1: Begrijp BFS
BFS onderzoekt de graaf **niveau per niveau** met een **queue** (FIFO).

Algorithm:
1. Start met `initial_node` in de **frontier** (queue).
2. Hou een set `explored` bij van bezochte nodes.
3. Zolang de frontier niet leeg is:
   - Pop de **voorste** node uit de queue.
   - Check of dit de goal is → zo ja, return.
   - Voeg anders deze node toe aan `explored`.
   - Voeg alle **niet-bezochte** kinderen toe aan de **achterkant** van de queue.

### Stap 2: Implementeer BFS
Gebruik `from collections import deque` voor een efficiënte queue.

### Stap 3: Backward printing (Uitbreiding)
Zorg dat het pad van start tot goal wordt **teruggeprint**.  
*Hint:* bewaar bij elke node ook de **parent** (vanwaar je kwam), zodat je achteraf het pad kunt reconstrueren.

<details>
<summary><b>🔎 Hint parent-tracking</b></summary>
Je kan een dictionary `parent = {}` bijhouden. Bij elk bezoek: `parent[child_node] = current_node`.  
Na de search loop je van goal terug naar start via parent-links.
</details>

---

# Oefening 3: Sliding Puzzle

Open `sliding_puzzle_start.py`. Het bevat een `SlidingPuzzle`-klasse.

## Stappenplan

### Stap 1: Begrijp het probleem
Een 8-puzzle (3×3 grid) heeft getallen 1-8 en een leeg vakje (0).  
Je kan het lege vakje verschuiven (omhoog, omlaag, links, rechts).  
Doel: bereik de opgeloste configuratie `[[1,2,3],[4,5,6],[7,8,0]]`.

### Stap 2: Implementeer `possible_new_configurations()`
Geef een lijst van nieuwe `SlidingPuzzle`-objecten na elke mogelijke zet.

### Stap 3: Implementeer `cost()` (heuristiek)
Gebruik de **Manhattan-distance**:
`cost = som over alle tegels van |rij_doel - rij_huidig| + |kol_doel - kol_huidig|`

### Stap 4: Los de puzzel op met BFS
Schrijf een functie `solve_puzzle(start_puzzle)` die BFS gebruikt.  
Gebruik de `possible_new_configurations()` om de volgende states te genereren.

### Stap 5: Test met de voorbeeldpuzzel uit `__main__`.

---

## Klaar?
- Commit je werk. Als je tijd hebt, kijk al naar **week 3** (maze DFS, Dijkstra).