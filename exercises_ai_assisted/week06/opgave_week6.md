# Week 6 — Oefening: TicTacToe met Minimax & Alpha-Beta

## Leerdoelen
- Je implementeert **Minimax** voor TicTacToe.
- Je voegt **alpha-beta pruning** toe.
- Je voegt **depth limiting** toe.

## Overzicht

| # | Oefening | Tijd |
|---|----------|------|
| 1 | TicTacToe met Minimax | 40 min |
| 2 | Alpha-beta pruning | 20 min |
| 3 | Depth limiting | 20 min |

---

## Stappenplan

### Stap 1: Implementeer TicTacToe

Open `tictactoe_start.py`. Vul de klasse aan:

- `__init__`: 3×3 bord (lege velden), speler `'X'` begint.
- `is_valid_move(x, y)`: check of (x,y) leeg is.
- `make_move(x, y, player)`: plaats `player` op (x,y).
- `check_winner()`: return `'X'`, `'O'` of `None`.
- `is_draw()`: bord vol zonder winnaar.
- `print_board()`: toon het bord (zie opgave_tictactoe.md voor voorbeeld).

### Stap 2: Implementeer Minimax

```python
def minimax(self, depth, is_maximizing):
    if self.check_winner() == 'X': return 1
    if self.check_winner() == 'O': return -1
    if self.is_draw(): return 0

    if is_maximizing:
        best = -float('inf')
        for zet in self.possible_moves():
            self.make_move(*zet, 'X')
            best = max(best, self.minimax(depth+1, False))
            self.undo_move(*zet)
        return best
    else:
        best = float('inf')
        for zet in self.possible_moves():
            self.make_move(*zet, 'O')
            best = min(best, self.minimax(depth+1, True))
            self.undo_move(*zet)
        return best
```

### Stap 3: `find_best_move()`
Doorloop alle mogelijke zetten en kies de zet met de hoogste minimax-waarde (voor `'X'`).

### Stap 4: Speel het spel
Maak een `play()`-methode: computer speelt `'X'`, jij speelt `'O'` via input.

### Stap 5: Alpha-beta pruning
Voeg `alpha` en `beta` parameters toe aan minimax.  
Prune (stop de loop) als `beta <= alpha` in een max-knoop, of `alpha >= beta` in een min-knoop.

### Stap 6: Depth limiting
Voeg een `max_depth`-parameter toe. Als `depth >= max_depth`: return 0 ipv verder te rekenen.

---

## Klaar?
- Raken jullie niet meer aan de computer te winnen? Indien wel, voeg een kans-element toe: 50% random move, 50% minimax.  
- Kijk al naar **week 7** (Othello).