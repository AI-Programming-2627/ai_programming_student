# Hoofdstuk 6: Alpha-Beta Pruning & Expectimax

## Alpha-Beta Pruning

In veel game trees kunnen we shortcuts nemen: we 'snoeien' delen van de tree weg zonder de uitkomst te wijzigen.

**Werking**:
- **Alpha** = beste waarde voor Max (initieel -∞)
- **Beta** = beste waarde voor Min (initieel +∞)
- Als beta ≤ alpha: verdere takken zijn irrelevant → **prune**

```python
def minimax(board, depth, is_maximizing, alpha, beta):
    if depth == 0 or is_terminal(board):
        return evaluate(board)
    
    if is_maximizing:
        best = -float('inf')
        for zet in possible_moves(board):
            nieuwe_board = board.copy()
            nieuwe_board[zet] = 'X'
            score = minimax(nieuwe_board, depth-1, False, alpha, beta)
            best = max(best, score)
            alpha = max(alpha, best)
            if beta <= alpha:
                break  # alpha pruning
        return best
    else:
        best = float('inf')
        for zet in possible_moves(board):
            nieuwe_board = board.copy()
            nieuwe_board[zet] = 'O'
            score = minimax(nieuwe_board, depth-1, True, alpha, beta)
            best = min(best, score)
            beta = min(beta, best)
            if beta <= alpha:
                break  # beta pruning
        return best
```

**Voordelen**:
- Geen kwaliteitsverlies (exacte oplossing)
- Kan gecombineerd worden met depth-limited search
- Altijd efficiënt om te implementeren!

---

## Expectimax: Stochastische Spellen

Minimax gaat uit van een **perfecte tegenstrever**. Dit is niet altijd realistisch:
- Menselijke fouten
- Kanscomponenten (dobbelstenen, kaarten)

**Expectimax** gebruikt de **verwachte waarde** voor kansopties:

```python
# Voor een kansknoop met 3 mogelijke uitkomsten (elk 1/3 kans):
expected = (9 * 1/3 + 0 * 1/3 + 3 * 1/3)  # = 4
```

| Aspect | Minimax | Expectimax |
|--------|---------|------------|
| Tegenstrever | Perfect | Mogelijk feilbaar |
| Type spellen | Zero-sum, perfect info | Stochastic, imperfect info |
| Evaluatie | Statische functie | Kansverdeling nodig |

---

## Diagram Notatie

- ▲ = Max (driehoek, punt omhoog)
- ▼ = Min (driehoek, punt omlaag)
- ○ = Kans (cirkel)

**Oorzaken van kanstheoretische processen**:
- Dobbelsteen gooien
- Kaart trekken
- Random initialisatie
- Imperfect information (poker, solitaire, 21'en)
