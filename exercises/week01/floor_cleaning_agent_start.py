"""
Oefening 2: Floor Cleaning Agent (Model-based Reflex Agent)
=============================================================
Implementeer een model-based reflex agent voor een robotstofzuiger.
Volg het stappenplan in opgave_week1.md.
"""


class FloorCleaningAgent:
    """
    Een model-based reflex agent die een kamer proper maakt.

    De kamer is een grid van `rows` × `cols` tegels.
    De robot start in de linkerbovenhoek (rij 0, kolom 0).
    """

    def __init__(self, rows=5, cols=10):
        """
        Initialiseer de robot met een lege kamer van `rows` × `cols`.

        Tip: gebruik een 2D-lijst om de status van elke tegel bij te houden.
        """
        self.rows = rows
        self.cols = cols

        # TODO: interne state initialiseren
        # - huidige positie (rij, kolom)
        # - grid met proper/vuil status per tegel (bv. True = proper, False = vuil)

        self.row = 0  # startrij (bovenaan)
        self.col = 0  # startkolom (links)

        # Voorbeeld: grid aanmaken (alle tegels beginnen vuil)
        # self.grid = [[False for _ in range(cols)] for _ in range(rows)]

    # ---------- Basisbewegingen ----------

    def move_up(self):
        """Verplaats de robot één tegel omhoog (rij -1)."""
        if self.row > 0:
            self.row -= 1
            print(f"Verplaats naar ({self.row}, {self.col})")
        else:
            print("Kan niet omhoog: rand bereikt")

    def move_down(self):
        """Verplaats de robot één tegel omlaag (rij +1)."""
        # TODO: implementeer
        pass

    def move_left(self):
        """Verplaats de robot één tegel naar links (kolom -1)."""
        # TODO: implementeer
        pass

    def move_right(self):
        """Verplaats de robot één tegel naar rechts (kolom +1)."""
        # TODO: implementeer
        pass

    # ---------- Stofzuigen ----------

    def clean_tile(self):
        """Stofzuig de huidige tegel (maak hem proper)."""
        # TODO: markeer huidige tegel als proper
        # print(f"Tegel ({self.row}, {self.col}) is nu proper!")
        pass

    # ---------- Strategie ----------

    def clean_room(self):
        """
        Laat de robot de volledige kamer proper maken.
        Gebruik een systematische strategie (bv. zigzag-patroon).
        """
        # TODO: implementeer een strategie
        # Tip: je kan een move_to(row, col) hulpmethode gebruiken
        pass

    # ---------- Helper om naar een specifieke tegel te gaan ----------

    def move_to(self, target_row, target_col):
        """
        Verplaats de robot van huidige positie naar (target_row, target_col).
        Gebruik de basisbewegingen move_up/down/left/right.
        """
        # TODO: implementeer
        # Beweeg eerst verticaal, dan horizontaal (of omgekeerd)
        pass

    # ---------- Weergave ----------

    def print_status(self):
        """Toon de huidige status van de kamer."""
        print("\nKamer status (V = vuil, P = proper, R = robot):")
        for r in range(self.rows):
            rij_str = ""
            for c in range(self.cols):
                if r == self.row and c == self.col:
                    rij_str += " R "
                else:
                    # TODO: toon 'V' of 'P' op basis van interne grid
                    rij_str += " ? "
            print(rij_str)
        print()


if __name__ == "__main__":
    # Test je agent
    robot = FloorCleaningAgent()

    print("Beginstatus:")
    robot.print_status()

    # TODO: roep clean_room() aan
    # robot.clean_room()

    print("Eindstatus:")
    robot.print_status()