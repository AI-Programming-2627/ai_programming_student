# Hoofdstuk 7: Stochastische Problemen

## Niet-Deterministische Problemen

Je kan niet exact voorspellen wat een bepaalde zet oplevert (bv. dobbelstenen).

- In een deterministisch probleem = een vast **pad**
- In een stochastisch probleem = een **boom** met beslissingen **afhankelijk van de state**

---

## AND-OR Zoektrees

In niet-deterministische problemen zijn er twee soorten knopen:
- **OR-knopen**: beslissingen van de agent (keuze)
- **AND-knopen**: kanselementen (geen controle)

**Voorbeeld**: een automatische bladverzamelaar weet niet of er nog bladeren bijvallen. Bij elke stap moet hij checken of bepaalde stukken opnieuw moeten worden opgeruimd.

```
          [Robot start]
               |
        Vallen er blaadjes?
          /          \
       Ja            Nee
        |              |
    [Opruimen]    [Doorgaan]
```

---

## Partieel Observeerbare Problemen

Hier heb je een **belief-state space**: een verzameling states die mogelijk overeenkomen met de realiteit.

- **Initiële state**: een set mogelijke beginstates
- **Acties**: als een illegale zet niets uithaalt, neem de unie van alle acties op de belief states
- **Transitie**: de agent moet blind navigeren en meerdere states in rekening nemen

Bij elke zet van de tegenspeler moet de belief-state space worden bijgewerkt.

---

## Toepassing: Expectimax voor Stochastische Spellen

Zie het hoofdstuk over Expectimax voor de concrete algoritmische aanpak van stochastische spellen zoals poker, backgammon, en Mensch-ärgere-Dich-nicht.
