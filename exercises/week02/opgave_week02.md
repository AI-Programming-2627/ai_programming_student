# Week 2 — Oefeningen: zoekalgoritmes & agents

## Leerdoelen
- Je implementeert een **model-based reflex agent** (self-driving car).
- Je gaat om met **foutieve sensoren** met redundante sensoren en interne state.
- Je implementeert een **utility-based agent** (greedy routeplanner).

## Overzicht

| # | Oefening | Tijd |
|---|----------|------|
| 1 | Self-Driving Car (reflex agent) | 30 min |
| 2 | Foute sensor: Boeing 737 MAX | 30 min |
| 3 | Routeplanner (utility-based agent) | 30 min |

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
- Bereken snelheid = vorige_afstand - huidige_afstand (negatief = voorligger rijdt weg, positief = voorligger komt dichter).
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
- Zijn beide sensoren het **bij benadering** eens (verschil < `TOLERANCE`)? -> gebruik het gemiddelde.
- Lopen ze **duidelijk uiteen**? -> dan is er iets mis. Gebruik het `sensor_model`: vertrouw de sensor die **consistent** is met de vorige waarde (interne state!). Tip: het dichtste bij kun je best implementeren met `abs`, de absolute waarde functie.
- Onthoud in de interne state welke sensor als verdacht geldt. Vanaf dan vertrouw je de andere sensor.

### Stap 4: Beslissing
- Als de betrouwbare hoogtemeter een dalende trend tot die niet te sterk is: `return Correct()`. Er mag maximum 10 meter gedaald worden tussen metingen.
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

