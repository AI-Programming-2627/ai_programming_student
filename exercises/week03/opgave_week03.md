# Week 3 — Oefeningen: Maze met DFS & Dijkstra

## Leerdoelen
- Je implementeert **Depth-First Search (DFS)** op een maze.
- Je implementeert **Dijkstra** voor de korste paden.
- Je vergelijkt de strategieën.

## Overzicht

| # | Oefening | Tijd |
|---|----------|------|
| 1 | BFS | 45 min |
| 2 | Schuifpuzzel | 45 min |
| 3 | Maze met DFS | 45 min |
| 4 | Dijkstra | 45 min |

---

# Oefening 1: Breadth-First Search

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

# Oefening 2: Sliding Puzzle

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

# Oefening 3: Maze met DFS

Open `maze_start.py`. Er is al een `Maze`-klasse voorzien die het maze print en geldige zetten kan bepalen.

## Stappenplan

### Stap 1: Implementeer `valid_moves(current)`
Geef alle buurposities terug waar de robot naartoe kan (binnen het grid en niet door een muur `#`).

### Stap 2: Implementeer `extract_path(stack)`
Wanneer de end-positie bereikt is, haal het pad uit de stack (de grid-coördinaten van start naar end).

### Stap 3: Implementeer `find_path(maze)`
Gebruik een **stack** (LIFO) om DFS uit te voeren:
1. Start bij `maze.start`, duw op de stack.
2. Zolang er nodes in de stack zitten:
   - Pop de bovenste node.
   - Als dit de end is: return pad.
   - Voeg de node toe aan `visited`.
   - Duw alle onbezochte `valid_moves` op de stack.

### Stap 4: Test met het voorbeeld

---

# Oefening 4: Dijkstra (uitbreiding)

Open `dijkstra_start.py`. Hier wordt een graaf met gewichten ingelezen.

## Stappenplan

### Stap 1: Begrijp Dijkstra
Dijkstra vindt het kortste pad in een gewogen graaf:
1. Begin bij de start, afstand = 0.
2. Kies telkens de node met de **laagste tot nu toe gekende afstand** die nog niet bezocht is.
3. Update de afstanden van de buren als een korter pad gevonden is.

### Stap 2: Implementeer Dijkstra
Schrijf `dijkstra(problem)` die een `Path` teruggeeft.

*Hint:* gebruik `heapq` voor een priority queue.

### Stap 3: Vergelijk met BFS
Test beide algoritmes op dezelfde graaf. Wanneer geven ze hetzelfde pad? Wanneer niet?

### Stap 4 (Uitbreiding): A*
Voeg een heuristiek toe (bijv. Manhattan-afstand).  
*Hint:* gebruik `f = g + h` in de priority queue.

---

## Klaar?
- Commit. Bekijk alvast **week 4** (simulated annealing / TSP).