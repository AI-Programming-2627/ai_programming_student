# Week 1 — Oefeningen: Sorteeralgoritmes & Intelligente Agents

## Leerdoelen deze week

- Je begrijpt hoe **Insertion Sort** werkt en kan het zelf implementeren in Python.
- Je kan de performantie van sorteeralgoritmes vergelijken met Big-O notatie.
- Je begrijpt het **agentenmodel** (sensors, actuators, agent program).
- Je kan een **model-based reflex agent** ontwerpen en implementeren voor de "floor cleaning agent".

## Overzicht

| Oefening | Onderwerp | Geschatte tijd |
|----------|-----------|----------------|
| 1 | Insertion Sort implementeren | 30 min |
| 2 | Floor Cleaning Agent (model-based reflex) | 60 min |

---

# Oefening 1: Insertion Sort

## Stappenplan

Volg onderstaande stappen om Insertion Sort te implementeren:

### Stap 1: Begrijp het algoritme

Insertion Sort werkt zoals je speelkaarten in je hand sorteert:

- Je begint met een lege "gesorteerde" lijst (of het eerste element van de originele lijst).
- Je neemt één voor één elk nieuw element uit de ongeordende lijst.
- Je **voegt het in** op de juiste positie in de (al gesorteerde) deel-lijst, zodat die gesorteerd blijft.
**Voorbeeld:**  
`[5, 2, 4, 6, 1, 3]`

1. Begin met `[5]` (eerste element is al gesorteerd).
2. Neem `2` — voeg in vóór `5` → `[2, 5]`
3. Neem `4` — voeg in tussen `2` en `5` → `[2, 4, 5]`
4. Neem `6` — voeg in na `5` → `[2, 4, 5, 6]`
5. Neem `1` — voeg in vooraan → `[1, 2, 4, 5, 6]`
6. Neem `3` — voeg in tussen `2` en `4` → `[1, 2, 3, 4, 5, 6]`

### Stap 2: Open het startbestand

Open `insertion_sort_start.py`. Je vindt er een functie-skelet.

### Stap 3: Implementeer de sorteerfunctie

- Neem het eerste element als begin van de gesorteerde lijst.
- Doorloop de rest van de lijst.
- Vergelijk elk element met de elementen in het gesorteerde deel en schuif waar nodig.
- **Tip:** Werk **in-place** (verander de lijst zelf) of maak een nieuwe lijst aan. Allebei mag.

<details>
<summary><b>🔎 Meer hulp nodig? Klik hier</b></summary>

Een veelgebruikte aanpak in-place:

```python
def insertion_sort(sequence):
    for i in range(1, len(sequence)):
        key = sequence[i]
        j = i - 1
        while j >= 0 and sequence[j] > key:
            sequence[j + 1] = sequence[j]
            j -= 1
        sequence[j + 1] = key
    return sequence
```

Probeer eerst zelf, gebruik dit alleen als je vast zit!
</details>

### Stap 4: Test je implementatie

Test met deze cases:

- Een lege lijst `[]`
- Een lijst met één element `[42]`
- Een al gesorteerde lijst `[1, 2, 3, 4]`
- Een omgekeerd gesorteerde lijst `[5, 4, 3, 2, 1]`
- Een lijst met duplicaten `[3, 1, 2, 1, 3]`

### Stap 5 (Uitbreiding): Vergelijk met Bubble Sort en Merge Sort

Kopieer Bubble Sort en Merge Sort uit de cursus naar jouw bestand en vergelijk de snelheden voor lijsten van:

- 10, 100, 1000, 10 000 items

Gebruik de `time`-module. Welk algoritme is het snelst? Klopt dat met Big-O?

---

# Oefening 2: Floor Cleaning Agent (Model-based Reflex Agent)

## Stappenplan

### Stap 1: Wat is het probleem?

Bekijk hoofdstuk 1 over agents. Je gaat een **model-based reflex agent** programmeren voor een robotstofzuiger.

**De situatie:**
- De kamer is **10 tegels bij 5 tegels** (een grid van 10 kolommen × 5 rijen).
- De robot start **linksboven** (rij 0, kolom 0) — het laadstation.
- Elke tegel is ofwel **vuil** of **proper**.
- De robot is exact even groot als één tegel.
- De robot kan: **verplaatsen** (omhoog, omlaag, links, rechts), **stofzuigen**, of **stil staan**.
- De robot weet waar hij is (interne state) en houdt bij welke tegels al gepoetst zijn.
### Stap 2: Ontwerp de interne state

Een model-based reflex agent heeft een **interne state** en een **transition model**.  
Bepaal zelf:

- Welke informatie moet de robot **onthouden**? (bijv. huidige positie, status van elke tegel)
- Hoe ziet het **transition model** eruit? (bijv. na `move_down()` verandert de rij)

<details>
<summary><b>🔎 Hint</b></summary>

Je hebt minstens nodig:
- De huidige `x`- en `y`-positie (kolom en rij).
- Een grid (bv. 2D-lijst) dat bijhoudt welke tegels vuil/proper zijn.
- Een lijst van bezochte tegels of een status per tegel.
</details>

### Stap 3: Open het startbestand

Open `floor_cleaning_agent_start.py`. Je vindt een klasse-skelet.

### Stap 4: Implementeer de basisbewegingen

Implementeer eerst de bewegingen:

- `move_up()` — verplaats één tegel omhoog
- `move_down()` — verplaats één tegel omlaag
- `move_left()` — verplaats één tegel naar links
- `move_right()` — verplaats één tegel naar rechts

**Let op:** De robot kan niet buiten het grid bewegen. Controleer dus of de volgende positie binnen de grenzen (0-9 voor kolom, 0-4 voor rij) valt. In realiteit zou je bijvoorbeeld kunnen denken dat een robot een muur kan zien of voelen als hij er vlak naast staat of tegen botst.

### Stap 5: Implementeer `clean_tile()`

De robot kan de huidige tegel stofzuigen. Markeer die tegel als proper.

### Stap 6: Kies een strategie

De robot moet **alle tegels** bezoeken en proper maken.  
Bedenk een eenvoudige strategie om dit te doen.
<details>
<summary><b>🔎 Hint</b></summary>

Je kan een eenvoudige **zigzag-strategie** gebruiken:

1. Ga naar rechts tot je aan de rechterrand bent.
2. Ga één rij omlaag.
3. Ga naar links tot je aan de linkerrand bent.
4. Ga één rij omlaag.
5. Herhaal tot alle rijen gedaan zijn.

Of bedenk zelf een andere strategie.
</details>

### Stap 7: Implementeer de scan-and-clean methode

Schrijf een methode `clean_room()` die de robot systematisch door de kamer laat bewegen en elke tegel proper maakt.

<details>
<summary><b>🔎 Hint voor een zigzag-patroon</b></summary>

```python
def clean_room(self):
    for row in range(self.rows):
        if row % 2 == 0:  # even rijen: rechtswaarts
            for col in range(self.cols):
                self.move_to(row, col)
                self.clean_tile()
        else:  # oneven rijen: linkswaarts
            for col in range(self.cols - 1, -1, -1):
                self.move_to(row, col)
                self.clean_tile()
    print("Kamer is proper!")
```

Je moet dan wel een `move_to()` voorzien die naar een bepaalde (rij, kolom) gaat via `move_up/down/left/right`.
</details>

### Stap 8: Test je agent

Voeg onder `if __name__ == "__main__":` testcode toe die:

1. Een `FloorCleaningAgent` aanmaakt.
2. De kamer toont (print een overzicht van proper/vuil).
3. `clean_room()` aanroept.
4. Na het poetsen opnieuw de status toont om te controleren dat alles proper is.

### Stap 9 (Uitbreiding — enkel als je tijd hebt)

Pas je agent aan zodat:

- **Tegels na 7 stappen opnieuw vuil worden.**  
  *Hint:* houd een teller bij per tegel.
- **Tegels die vuil worden volgens een kansverdeling: gebruik de random module in python.
- **Er obstakels in de kamer staan.**  
  De robot voelt ze met een bumper (enkel als hij ernaartoe beweegt).  
  Geef obstakels mee als een lijst van (rij, kolom)-coördinaten in de constructor.  
  Als de robot tegen een obstakel botst, print "Obstakel!" en probeer een andere richting.

---

## Klaar?

- Commit je wijzigingen naar Git.
- Als je tijd over hebt, begin al eens aan **week 2** (self-driving car, breadth-first, sliding puzzle) te kijken — de bestanden staan in de map `oefeningen/`.