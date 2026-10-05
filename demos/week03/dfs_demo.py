"""DEMO: depth-first search op de stedengraaf Antwerpen -> Parijs.

DFS pakt telkens de diepste node uit de frontier en zoekt dus
eerst in de diepte. Snel een antwoord, maar niet het kortste pad.
"""

from demos.week03.graaf import DOEL, START, STEDEN_GRAAF, depth_first_search


def main() -> None:
    print(f"Zoek van {START} naar {DOEL} met DFS")
    print("-" * 50)
    pad = depth_first_search(STEDEN_GRAAF, START, DOEL, verbose=True)
    print("-" * 50)
    if pad is None:
        print("Geen pad gevonden")
        return
    print(f"Gevonden pad ({len(pad) - 1} stappen):")
    print(" -> ".join(pad))


if __name__ == "__main__":
    main()
