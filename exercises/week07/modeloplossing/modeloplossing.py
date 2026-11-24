"""
Week 7 — Oplossing: TicTacToe met Minimax, Alpha-Beta en Depth Limiting
=======================================================================
Oefening uit `opgave_tictactoe.md` en `opgave_week6.md`: een TicTacToe
waarbij de computer (X) met minimax speelt, met alpha-beta pruning,
een maximale zoekdiepte (depth limiting) en als uitbreiding een
kans-element (50% willekeurige zetten).

Zie ook `oefeningen-adversarial_search.md` (labo week 7-8).
"""

import random

# =============== Oefening 1: TicTacToe met Minimax ===============


class TicTacToe:
    """Een 3x3 TicTacToe-bord met een minimax-computer die X speelt."""

    def __init__(self) -> None:
        """Maak een leeg bord; X speelt altijd eerst."""
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.current_player = "X"

    def possible_moves(self) -> list[tuple[int, int]]:
        """Geef een lijst van (rij, kolom)-tupels van lege velden."""
        return [(r, c) for r in range(3) for c in range(3)
                if self.board[r][c] == " "]

    def is_valid_move(self, x: int, y: int) -> bool:
        """Controleer of (x, y) een leeg veld is binnen het bord.

        Args:
            x: het rij-nummer (0 tot 2).
            y: het kolom-nummer (0 tot 2).

        Returns:
            True als het veld leeg is, anders False.
        """
        return 0 <= x < 3 and 0 <= y < 3 and self.board[x][y] == " "

    def make_move(self, x: int, y: int, player: str) -> None:
        """Zet `player` op veld (x, y) en geef de beurt door.

        Args:
            x: het rij-nummer.
            y: het kolom-nummer.
            player: "X" of "O".
        """
        if self.is_valid_move(x, y):
            self.board[x][y] = player
            self.current_player = "O" if player == "X" else "X"

    def undo_move(self, x: int, y: int) -> None:
        """Maak veld (x, y) terug leeg (gebruikt door minimax)."""
        self.board[x][y] = " "

    def check_winner(self) -> str | None:
        """Geef de winnaar terug: "X", "O" of None als er geen is.

        Returns:
            "X" of "O" bij drie op een rij (rij, kolom of diagonaal),
            anders None.
        """
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != " ":
                return self.board[i][0]
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != " ":
                return self.board[0][i]
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != " ":
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != " ":
            return self.board[0][2]
        return None

    def is_draw(self) -> bool:
        """Geef True als het bord vol is zonder winnaar."""
        return not self.possible_moves() and self.check_winner() is None
    def minimax(self, depth: int, is_maximizing: bool,
                alpha: float | None = None,
                beta: float | None = None,
                max_depth: int | None = None) -> float:
        """Minimax met alpha-beta pruning en depth limiting.

        Args:
            depth: de huidige diepte in de zoekboom (start op 0).
            is_maximizing: True op een X-knoop (computer), False op een
                O-knoop.
            alpha: de beste waarde die X (max) al gevonden heeft.
            beta: de beste waarde die O (min) al gevonden heeft.
            max_depth: de maximale zoekdiepte; als depth >= max_depth wordt
                er 0 teruggegeven, ook al is de staat niet terminaal.

        Returns:
            De score vanuit X-perspectief: 1 (X wint), -1 (O wint),
            0 (gelijkspel of dieptelimiet bereikt).
        """
        winnaar = self.check_winner()
        if winnaar == "X":
            return 1
        if winnaar == "O":
            return -1
        if self.is_draw() or (max_depth is not None and depth >= max_depth):
            return 0

        if is_maximizing:
            best = float("-inf")
            for x, y in self.possible_moves():
                self.make_move(x, y, "X")
                best = max(best,
                           self.minimax(depth + 1, False, alpha, beta, max_depth))
                self.undo_move(x, y)
                if alpha is not None:
                    alpha = max(alpha, best)
                    if beta is not None and beta <= alpha:
                        break
            return best
        best = float("inf")
        for x, y in self.possible_moves():
            self.make_move(x, y, "O")
            best = min(best,
                       self.minimax(depth + 1, True, alpha, beta, max_depth))
            self.undo_move(x, y)
            if beta is not None:
                beta = min(beta, best)
                if alpha is not None and beta <= alpha:
                    break
        return best

    def find_best_move(self) -> tuple[int, int] | None:
        """Kies de beste zet voor X via minimax.

        Returns:
            Het (rij, kolom)-tupel van de beste zet, of None als het bord
            vol is.
        """
        beste_zet = None
        beste_waarde = float("-inf")
        for x, y in self.possible_moves():
            self.make_move(x, y, "X")
            waarde = self.minimax(0, False)
            self.undo_move(x, y)
            if waarde > beste_waarde:
                beste_waarde = waarde
                beste_zet = (x, y)
        return beste_zet

    def make_random_move(self) -> tuple[int, int] | None:
        """Kies een willekeurige geldige zet.

        Returns:
            Een willekeurig (rij, kolom)-tupel, of None als het bord vol is.
        """
        zetten = self.possible_moves()
        if not zetten:
            return None
        return random.choice(zetten)

    def print_board(self) -> None:
        """Toon het bord in de terminal."""
        horizontal_line = "+---+---+---+"
        print(horizontal_line)
        for row in self.board:
            print(f"| {row[0]} | {row[1]} | {row[2]} |")
            print(horizontal_line)

    def play(self, mixed: bool = False) -> None:
        """Speel een volledig spel tegen de computer (X).

        Args:
            mixed: als True kiest de computer 50% van de tijd een
                willekeurige zet (uitbreiding uit de opgave).
        """
        print("TicTacToe: X = computer, O = jij (rij SPATIE kolom).")
        self.print_board()
        while True:
            if not self.possible_moves():
                break
            if mixed and random.random() < 0.5:
                zet = self.make_random_move()
            else:
                zet = self.find_best_move()
            if zet is None:
                break
            self.make_move(zet[0], zet[1], "X")
            self.print_board()
            if self.check_winner() is not None or not self.possible_moves():
                break
            x, y = self._vraag_zet()
            if (x, y) == (-1, -1):
                continue
            self.make_move(x, y, "O")
            self.print_board()
            if self.check_winner() is not None:
                break

        winnaar = self.check_winner()
        if winnaar is not None:
            print(f"Speler {winnaar} wint!")
        elif not self.possible_moves():
            print("Gelijkspel.")

    def _vraag_zet(self) -> tuple[int, int]:
        """Vraag de menselijke speler om een geldige zet of geef (-1, -1)."""
        try:
            x, y = map(int, input("Enter je zet (rij SPATIE kolom): ").split())
        except ValueError:
            print("Ongeldige invoer. Geef twee getallen, bv. '0 0'.")
            return (-1, -1)
        while not self.is_valid_move(x, y):
            print("Ongeldige zet. Kies een leeg veld tussen 0 en 2.")
            x, y = map(int, input("Enter je zet (rij SPATIE kolom): ").split())
        return (x, y)


if __name__ == "__main__":
    game = TicTacToe()
    game.play()
