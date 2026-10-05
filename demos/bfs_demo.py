"""DEMO: breadth-first search op de stedengraaf Antwerpen -> Parijs.

BFS opent de frontier niveau per niveau en vindt zo het pad
met het minste aantal steden.
"""

from graaf import DOEL, START, STEDEN_GRAAF, breadth_first_search


def main() -> None:
    print(f"Zoek van {START} naar {DOEL} met BFS")
    print("-" * 50)
    pad = breadth_first_search(STEDEN_GRAAF, START, DOEL, verbose=True)
    print("-" * 50)
    if pad is None:
        print("Geen pad gevonden")
        return
    print(f"Gevonden pad ({len(pad) - 1} stappen):")
    print(" -> ".join(pad))


if __name__ == "__main__":
    main()
