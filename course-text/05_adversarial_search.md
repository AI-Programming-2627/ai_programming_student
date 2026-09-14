# Hoofdstuk 5: Adversarial Search (Minimax)

## Multi-Agent Systemen

Spellen zoals poker, schaken, dammen,...

**Soorten**:
- Perfect / Imperfect information
- Zero-sum: 1 winnaar, rest verliest

We bekijken **zero-sum, 2-player, perfect information games**.

---

## Two-Player Zero-Sum Games

Een spel wordt gekenmerkt door:
- **Initiële state**
- **Wie aan beurt** is
- **Mogelijke acties** per state
- **Transitiemodel** als resultaat van acties
- **Terminal test**: checkt of spel klaar is
- **Utility functie**: winnaar +1, verliezer 0, draw ½

De **game tree** bevat alle mogelijke zetten. Wordt snel erg groot.

---

## Minimax Algoritme

**Speler 1 = Max** (wil maximaliseren, utility +1)
**Speler 2 = Min** (wil minimaliseren, utility -1)

Het algoritme werkt recursief:
- Op een **Max**-knoop: kies de actie met de hoogste utility
- Op een **Min**-knoop: kies de actie met de laagste utility

```python
def minimax(board, is_maximizing):
    # Terminal test
    if is_win(board, 'X'):
        return 1  # Max wint
    if is_win(board, 'O'):
        return -1  # Min wint
    if is_draw(board):
        return 0
    
    if is_maximizing:
        best = -float('inf')
        for zet in possible_moves(board):
            nieuwe_board = board.copy()
            nieuwe_board[zet] = 'X'
            best = max(best, minimax(nieuwe_board, False))
        return best
    else:
        best = float('inf')
        for zet in possible_moves(board):
            nieuwe_board = board.copy()
            nieuwe_board[zet] = 'O'
            best = min(best, minimax(nieuwe_board, True))
        return best
```

**Werkt voor**: perfect information games met beperkte game tree.
Bij grotere problemen is de tree te groot.

---

## Depth-Limited Search

De game tree is vaak te groot om volledig te doorzoeken. Oplossingen:
1. **Limited depth**: stop na maximaal N levels
2. **Alpha-beta pruning**: snoei delen van de tree weg
3. **Evaluatiefunctie**: schat boardwaarde ipv. exacte uitkomst

---

## Limited Depth & Utility Functie

In plaats van een terminale staat te vinden, gebruik je een **evaluatiefunctie** die voor **elke** boardpositie een schatting geeft.

**Voorbeeld Schaken**:
```python
def evaluate(board):
    score = 0
    # Materiaal: pion=1, paard=3, loper=3, toren=5, dame=9
    for piece in board.white_pieces:
        score += piece_value[piece.type]
    for piece in board.black_pieces:
        score -= piece_value[piece.type]
    return score
```

De evaluatiefunctie is een **utility functie**: hoe hoger, hoe beter voor Max.

**Trade-off**:
- Moet een goede waarde geven
- Mag niet te lang duren om te berekenen

**Implementatietip**: gebruik **aftellende depth** in plaats van optellende.

```python
def minimax(board, depth, is_maximizing):
    if depth == 0 or is_terminal(board):
        return evaluate(board)
    # ... recursie met depth - 1
```
