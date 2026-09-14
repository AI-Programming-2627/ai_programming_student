# Week 3 — Oefeningen: Maze met DFS & Dijkstra

## Leerdoelen
- Je implementeert **Depth-First Search (DFS)** op een maze.
- Je implementeert **Dijkstra** voor de korste paden.
- Je vergelijkt de strategieën.

## Overzicht

| # | Oefening | Tijd |
|---|----------|------|
| 1 | Maze met DFS | 45 min |
| 2 | Dijkstra | 45 min |

---

# Oefening 1: Maze met DFS

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

# Oefening 2: Dijkstra (variaties)

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