# Week 2 — Oefeningen: zoekalgoritmes & agents

## Leerdoelen
- Je implementeert een **model-based reflex agent** (self-driving car).
- Je gaat om met **foutieve sensoren** met redundante sensoren en interne state.
- Je implementeert een **utility-based agent** (greedy routeplanner).
- Je implementeert **Breadth-First Search** met pad-printing.
- Je lost een **sliding puzzle** op met BFS/DFS.

## Overzicht

| # | Oefening | Tijd |
|---|----------|------|
| 1 | Self-Driving Car (reflex agent) | 30 min |
| 2 | Foute sensor: Boeing 737 MAX | 30 min |
| 3 | Routeplanner (utility-based agent) | 30 min |
| 4 | Breadth-First Search | 30 min |
| 5 | Sliding Puzzle | 45 min |

---

# Oefening 1: Self-Driving Car (model-based reflex)

Open `selfdriving_car_start.py`. Je vindt de klassen `LidarSensorInput`, `Brake`, `Nothing` en `Agent`.

De self-driving car moet zijn voorligger volgen.  
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
- Schat tijd tot botsing: als snelheid != 0, dan `tijd = afstand / snelheid`.
- Als tijd < 5 seconden: `return Brake()`, anders `return Nothing()`.
- Update de opgeslagen afstand.

### Stap 4: Test met de meegeleverde code

---

# Oefening 2: Foute sensor — Boeing 737 MAX (model-based reflex)

Open `faulty_sensor_start.py`.

Uit les 1: een **foute sensor** kan desastreuze gevolgen hebben. Bij de Boeing 737 MAX leidde één externe sensor (de AoA-sensor) tot twee crashes. De les: bouw **redundantie** in en laat de agent **intern redeneren** over de betrouwbaarheid van zijn sensoren.

## Stappenplan

### Stap 1: PEAS-analyse
Vul voor deze agent de PEAS-tabel in. Wat is de performance measure? Wat kan de agent waarnemen?

### Stap 2: Implementeer `read_all()`
Geef de metingen van beide sensoren terug als tuple.

### Stap 3: Plausibiliteitscheck in `process(p)`
- Zijn beide sensoren het **bij benader** eens (verschil < `TOLERANCE`)? -> gebruik het gemiddelde.
- Lopen ze **duidelijk uiteen**? -> dan is er iets mis. Gebruik het `sensor_model`: vertrouw de sensor die **consistent** is met de vorige waarde (interne state!).
- Onthoud in de interne state welke sensor als verdacht geldt. Vanaf dan vertrouw je de andere sensor.

### Stap 4: Beslissing
- Als de betrouwbare hoogtemeter een dalende trend toont terwijl de autothrottle actief is: `return Correct()`.
- Anders: `return Nothing()`.

### Stap 5: Test met de meegeleverde reeks
De reeks in `__main__` bevat een moment waarop sensor A stuk gaat. Controleer of de agent correct blijft doorvliegen op sensor B. Wat gebeurt er als je de plausibiliteitscheck weglaat?

### Reflectie
- Waarom is een simple reflex agent hier **gevaarlijk**?
- Dit is een voorbeeld van een agent met een **sensor model** en **interne state**: welk agenttype is dit?

---

# Oefening 3: Routeplanner (utility-based agent)

Open `routeplanner_start.py`.

Uit les 1: een **utility-based agent** maximaliseert een interne utility-functie. Voor de route Antwerpen -> Parijs was de utility `$-d(huidige, nieuwe)$`: hoe korter de sprong, hoe beter.

Deze agent zoekt **niet** (geen BFS/DFS): hij kiest bij elke stap **greedy** de buur met de hoogste utility.

## Stappenplan

### Stap 1: Implementeer `utility(from_city, to_city)`
Geef `$-d$` terug, de negatieve afstand tussen de twee steden.

### Stap 2: Implementeer `choose_next(current_city, visited)`
- Geef alle **nog niet bezochte** buren van `current_city`.
- Kies de buur met de hoogste utility (kleinste afstand).
- Als er geen buren meer zijn: return `None`.

### Stap 3: Implementeer `plan_route(start_city, goal_city)`
- Herhaal: kies de volgende stad via `choose_next`, voeg toe aan de route, update `visited`.
- Stop als je in de goal bent of vastzit (geen buren meer).

### Stap 4: Test met de meegeleverde graaf
Komt de agent aan in Parijs? Waarom is greedy **niet altijd optimaal**? Teken de situatie op papier waar de greedy agent in een doodlopende weg of een langere route terechtkomt.

### Reflectie
- Welk type agent is dit: goal-based of utility-based? Waarom?
- Wat zou een *goal-based* agent anders doen? (Welke stap in het plan verandert er?)
- Waarom is dit geen vervanging voor Dijkstra? (week 3!)

---

# Oefening 4: Breadth-First Search

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

# Oefening 5: Sliding Puzzle

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

## Klaar?
- Commit je werk. Als je tijd hebt, kijk al naar **week 3** (maze DFS, Dijkstra).