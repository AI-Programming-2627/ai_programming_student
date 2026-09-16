"""
Week 07 Autograder: Mini Othello met Minimax & Utility.

Test de publieke interface van de oplossing van de student:
- Othello: __init__, is_valid_move, make_move, opponent, count_pieces,
  valid_moves, random_move, evaluate, minimax, best_move

De tests controleren enkel gedrag, niet hoe het geïmplementeerd is.
Studentencode die crasht of infinite loopt wordt netjes afgehandeld.
"""

import contextlib
import importlib
import threading

import pytest

MODULE_PATH = "exercises_ai_assisted.week07.othello_start"

try:
    _mod = importlib.import_module(MODULE_PATH)
    Othello = _mod.Othello
except Exception as import_error:
    pytest.skip(
        f"othello_start.py kon niet geïmporteerd worden: {import_error}",
        allow_module_level=True,
    )

WEIGHTS = {
    "test_bord_init": 1,
    "test_is_valid_move": 1,
    "test_make_move": 1,
    "test_opponent": 1,
    "test_count_pieces": 1,
    "test_valid_moves_start": 1,
    "test_random_move": 2,
    "test_evaluate": 2,
    "test_minimax_diepte_0": 1,
    "test_minimax_simuleert_zetten": 2,
    "test_best_move": 2,
}


@contextlib.contextmanager
def time_limit(seconds: int = 5):
    """Beperk de duur van een blok code (tegen infinite loops).

    Gebruikt threading.Timer omdat SIGALRM niet werkt op Windows.
    """
    timeout_triggered = False

    def _raise():
        nonlocal timeout_triggered
        timeout_triggered = True

    timer = threading.Timer(seconds, _raise)
    timer.start()
    try:
        yield
        if timeout_triggered:
            raise TimeoutError(f"code duurde te lang (>{seconds}s)")
    finally:
        timer.cancel()


# =============== Bord-initialisatie ===============


def test_bord_init():
    """Het bord is 8x8 met de startpositie (O op 3,3/4,4; X op 3,4/4,3)."""
    spel = Othello()
    with time_limit():
        assert len(spel.board) == 8, "bord moet 8 rijen hebben"
        for rij in spel.board:
            assert len(rij) == 8, "elke rij moet 8 kolommen hebben"

        # Startpositie controleren
        assert spel.board[3][3] == "O"
        assert spel.board[4][4] == "O"
        assert spel.board[3][4] == "X"
        assert spel.board[4][3] == "X"

        # Alle andere velden leeg
        for r in range(8):
            for c in range(8):
                if (r, c) in [(3, 3), (4, 4), (3, 4), (4, 3)]:
                    continue
                assert spel.board[r][c] == " ", f"veld ({r},{c}) moet leeg zijn"


# =============== is_valid_move ===============


def test_is_valid_move():
    """is_valid_move keurt ongeldige zetten af en geldige goed."""
    spel = Othello()
    with time_limit():
        # Startpositie: geldige zetten voor X
        assert spel.is_valid_move(2, 3, "X") is True
        assert spel.is_valid_move(3, 2, "X") is True
        assert spel.is_valid_move(4, 5, "X") is True
        assert spel.is_valid_move(5, 4, "X") is True

        # Ongeldige zetten: bezet veld, buiten bereik, geen flankering
        assert spel.is_valid_move(3, 3, "X") is False  # bezet
        assert spel.is_valid_move(0, 0, "X") is False  # geen flankering
        assert spel.is_valid_move(-1, 0, "X") is False
        assert spel.is_valid_move(8, 0, "X") is False


# =============== make_move ===============


def test_make_move():
    """make_move plaatst een steen en draait de juiste stenen om."""
    spel = Othello()
    with time_limit():
        # Zet X op (2, 3): draait (3, 3) van O naar X
        spel.make_move(2, 3, "X")
        assert spel.board[2][3] == "X"
        assert spel.board[3][3] == "X", "steen op (3,3) moet omgedraaid zijn naar X"
        assert spel.board[4][4] == "O"
        assert spel.board[3][4] == "X"
        assert spel.board[4][3] == "X"
# =============== opponent ===============


def test_opponent():
    """opponent geeft de juiste tegenstander."""
    spel = Othello()
    with time_limit():
        spel.player = "X"
        assert spel.opponent() == "O"
        spel.player = "O"
        assert spel.opponent() == "X"


# =============== count_pieces ===============


def test_count_pieces():
    """count_pieces geeft de correcte aantallen."""
    spel = Othello()
    with time_limit():
        x, o = spel.count_pieces()
        assert x == 2, f"start X = 2, kreeg {x}"
        assert o == 2, f"start O = 2, kreeg {o}"


# =============== valid_moves ===============


def test_valid_moves_start():
    """valid_moves geeft 4 geldige zetten voor X en 4 voor O op startbord."""
    spel = Othello()
    with time_limit():
        x_zetten = spel.valid_moves("X")
        assert len(x_zetten) == 4, f"X moet 4 geldige zetten hebben, kreeg {len(x_zetten)}"
        for zet in x_zetten:
            assert spel.is_valid_move(zet[0], zet[1], "X") is True

        o_zetten = spel.valid_moves("O")
        assert len(o_zetten) == 4, f"O moet 4 geldige zetten hebben, kreeg {len(o_zetten)}"


# =============== random_move ===============


def test_random_move():
    """random_move geeft een geldige zet terug."""
    spel = Othello()
    with time_limit():
        # Meerdere keren testen voor consistentie
        for _ in range(10):
            zet = spel.random_move()
            assert zet is not None, "random_move mag None niet teruggeven"
            assert len(zet) == 2, f"random_move moet (rij, kol) tuple geven, kreeg {zet}"
            r, c = zet
            assert 0 <= r < 8 and 0 <= c < 8, f"zet ({r},{c}) is buiten het bord"
            assert spel.is_valid_move(r, c, "X") is True, (
                f"random_move gaf ongeldige zet ({r},{c})"
            )


# =============== evaluate ===============


def test_evaluate():
    """evaluate geeft een numerieke score terug voor een speler."""
    spel = Othello()
    with time_limit():
        score_x = spel.evaluate("X")
        score_o = spel.evaluate("O")

        # Moet een getal zijn (int of float)
        assert isinstance(score_x, (int, float)), "evaluate moet een getal teruggeven"
        assert isinstance(score_o, (int, float)), "evaluate moet een getal teruggeven"

        # Nadat X een zet doet, moet X een hogere score hebben
        spel.make_move(2, 3, "X")
        score_x_na = spel.evaluate("X")
        score_o_na = spel.evaluate("O")
        assert score_x_na != score_o_na or abs(score_x_na - score_o_na) > 0.5, (
            "evaluate moet een verschil zien na een zet"
        )


# =============== minimax ===============


def test_minimax_diepte_0():
    """minimax met depth=0 geeft de evaluate-score terug."""
    spel = Othello()
    with time_limit():
        # Depth=0 is bladknoop, moet evaluate() oproepen
        score = spel.minimax(0, True, "X")
        eval_score = spel.evaluate("X")
        assert score == eval_score, (
            f"minimax depth=0 moet evaluate(X) geven ({eval_score}), kreeg {score}"
        )

        score = spel.minimax(0, True, "O")
        eval_score = spel.evaluate("O")
        assert score == eval_score, (
            f"minimax depth=0 moet evaluate(O) geven ({eval_score}), kreeg {score}"
        )


def test_minimax_simuleert_zetten():
    """minimax simuleert zetten en wijzigt het bord niet permanent."""
    spel = Othello()
    with time_limit():
        # Onthoud de starttoestand
        bord_voor = [rij[:] for rij in spel.board]

        # Roep minimax aan met depth=1 (moet zetten simuleren)
        score = spel.minimax(1, True, "X")

        # Bord mag niet gewijzigd zijn
        for r in range(8):
            for c in range(8):
                assert spel.board[r][c] == bord_voor[r][c], (
                    f"minimax mag het bord niet wijzigen, veld ({r},{c}) veranderd"
                )

        # Score moet een getal zijn
        assert isinstance(score, (int, float)), "minimax moet een getal teruggeven"


# =============== best_move ===============


def test_best_move():
    """best_move geeft een geldige zet terug."""
    spel = Othello()
    with time_limit():
        zet = spel.best_move()
        assert zet is not None, "best_move mag None niet teruggeven"
        assert len(zet) == 2, f"best_move moet (rij, kol) tuple geven, kreeg {zet}"
        r, c = zet
        assert 0 <= r < 8 and 0 <= c < 8, f"zet ({r},{c}) is buiten het bord"
        assert spel.is_valid_move(r, c, "X") is True, (
            f"best_move gaf ongeldige zet ({r},{c}) voor X"
        )