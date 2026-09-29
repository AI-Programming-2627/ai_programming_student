"""
Week 1: Insertion Sort + Floor Cleaning Agent (Model-based Reflex Agent)
========================================================================

Opgeloste oefeningen van week 1 (zie opgave_week1.md).
"""


def insertion_sort(sequence):
    """
    Sorteer een lijst van klein naar groot met behulp van insertion sort.

    Parameters:
        sequence (list): De lijst om te sorteren.

    Returns:
        list: De gesorteerde lijst.
    """
    for i in range(1, len(sequence)):
        key = sequence[i]
        j = i - 1
        while j >= 0 and sequence[j] > key:
            sequence[j + 1] = sequence[j]
            j -= 1
        sequence[j + 1] = key
    return sequence


class FloorCleaningAgent:
    """
    Een model-based reflex agent die een kamer proper maakt.

    De kamer is een grid van `rows` × `cols` tegels.
    De robot start in de linkerbovenhoek (rij 0, kolom 0).
    """

    def __init__(self, rows=5, cols=10):
        """Initialiseer de robot met een lege kamer van `rows` × `cols`."""
        self.rows = rows
        self.cols = cols

        # Interne state
        self.row = 0
        self.col = 0
        self.grid = [[False for _ in range(cols)] for _ in range(rows)]

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
        if self.row < self.rows - 1:
            self.row += 1
            print(f"Verplaats naar ({self.row}, {self.col})")
        else:
            print("Kan niet omlaag: rand bereikt")

    def move_left(self):
        """Verplaats de robot één tegel naar links (kolom -1)."""
        if self.col > 0:
            self.col -= 1
            print(f"Verplaats naar ({self.row}, {self.col})")
        else:
            print("Kan niet naar links: rand bereikt")

    def move_right(self):
        """Verplaats de robot één tegel naar rechts (kolom +1)."""
        if self.col < self.cols - 1:
            self.col += 1
            print(f"Verplaats naar ({self.row}, {self.col})")
        else:
            print("Kan niet naar rechts: rand bereikt")

    # ---------- Stofzuigen ----------

    def clean_tile(self):
        """Stofzuig de huidige tegel (maak hem proper)."""
        self.grid[self.row][self.col] = True
        print(f"Tegel ({self.row}, {self.col}) is nu proper!")

    # ---------- Helper om naar een specifieke tegel te gaan ----------

    def move_to(self, target_row, target_col):
        """Verplaats de robot naar (target_row, target_col)."""
        while self.row < target_row:
            self.move_down()
        while self.row > target_row:
            self.move_up()
        while self.col < target_col:
            self.move_right()
        while self.col > target_col:
            self.move_left()

    # ---------- Strategie ----------

    def clean_room(self):
        """Laat de robot de volledige kamer proper maken (zigzag)."""
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

    # ---------- Weergave ----------

    def print_status(self):
        """Toon de huidige status van de kamer."""
        print("\nKamer status (V = vuil, P = proper, R = robot):")
        for r in range(self.rows):
            rij_str = ""
            for c in range(self.cols):
                if r == self.row and c == self.col:
                    rij_str += " R "
                elif self.grid[r][c]:
                    rij_str += " P "
                else:
                    rij_str += " V "
            print(rij_str)
        print()


if __name__ == "__main__":
    robot = FloorCleaningAgent()

    print("Beginstatus:")
    robot.print_status()

    robot.clean_room()

    print("Eindstatus:")
    robot.print_status()
