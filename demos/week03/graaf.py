"""De volledige stedengraaf van Antwerpen naar Parijs.

Gedeeld door de BFS- en DFS-demo's. States zijn `State`-objecten,
zoekoperaties werken op `Node`-objecten met acties.
"""

from collections import deque

STEDEN_GRAAF = {
    "Antwerpen": ["Breda", "Eindhoven", "Gent"],
    "Breda": ["Antwerpen", "Rotterdam", "Eindhoven"],
    "Eindhoven": ["Antwerpen", "Breda"],
    "Rotterdam": ["Breda"],
    "Gent": ["Antwerpen", "Brugge", "Kortrijk", "Brussel"],
    "Brugge": ["Gent", "Kortrijk"],
    "Kortrijk": ["Gent", "Brugge", "Lille"],
    "Brussel": ["Gent", "Charleroi", "Namen"],
    "Charleroi": ["Brussel", "Namen"],
    "Namen": ["Brussel", "Charleroi", "Luxemburg"],
    "Luxemburg": ["Namen", "Metz"],
    "Lille": ["Kortrijk", "Arras"],
    "Arras": ["Lille", "Amiens"],
    "Amiens": ["Arras", "Saint-Quentin", "Rouen", "Beauvais"],
    "Saint-Quentin": ["Amiens", "Laon"],
    "Laon": ["Saint-Quentin", "Reims", "Soissons"],
    "Reims": ["Laon", "Metz"],
    "Soissons": ["Laon", "Compiegne"],
    "Rouen": ["Amiens"],
    "Beauvais": ["Amiens", "Compiegne", "Saint-Denis"],
    "Compiegne": ["Beauvais", "Soissons", "Saint-Denis"],
    "Saint-Denis": ["Compiegne", "Beauvais", "Parijs"],
    "Metz": ["Luxemburg", "Reims", "Dijon"],
    "Dijon": ["Metz", "Parijs"],
    "Parijs": ["Saint-Denis", "Versailles", "Orleans", "Dijon"],
    "Versailles": ["Parijs", "Le Mans"],
    "Orleans": ["Parijs", "Le Mans"],
    "Le Mans": ["Versailles", "Orleans"],
}

START = "Antwerpen"
DOEL = "Parijs"


class State:
    """Een state in de state space (hier: een stad)."""

    def __init__(self, name: str) -> None:
        self.name = name


class Node:
    """Een node in de search tree: een state plus zijn acties."""

    def __init__(self, state: State, parent: "Node | None" = None) -> None:
        self.state = state
        self.actions: list[Node] = []
        self.parent = parent

    def add_action(self, action: "Node") -> None:
        self.actions.append(action)


def bouw_nodes(graaf: dict[str, list[str]]) -> dict[str, Node]:
    """Vertaal de adjacency-dict naar Node-objecten met acties."""
    nodes = {stad: Node(State(stad)) for stad in graaf}
    for stad, verbindingen in graaf.items():
        for buur in verbindingen:
            nodes[stad].add_action(nodes[buur])
    return nodes


def reconstruct_pad(node: Node) -> list[str]:
    """Bouw het gevonden pad op via de parent-verwijzingen."""
    pad: list[str] = []
    while node is not None:
        pad.append(node.state.name)
        node = node.parent
    return list(reversed(pad))


def breadth_first_search(
    graaf: dict[str, list[str]], start: str, doel: str, verbose: bool = False
) -> list[str] | None:
    """BFS volgens de cursustekst: openklappen niveau per niveau via een FIFO-queue.

    Vindt het pad met het minste aantal steden.
    """
    nodes = bouw_nodes(graaf)
    initial_node = nodes[start]
    goal_state = nodes[doel].state

    frontier = deque([initial_node])
    explored: set[str] = set()
    niveau = 0
    while frontier:
        if verbose:
            print(f"niveau {niveau}: frontier = {[n.state.name for n in frontier]}")
        niveau += 1
        node = frontier.popleft()
        if node.state.name == goal_state.name:
            return reconstruct_pad(node)
        explored.add(node.state.name)
        for action in node.actions:
            if action.state.name not in explored:
                if action.parent is None:
                    action.parent = node
                frontier.append(action)
    return None


def depth_first_search(
    graaf: dict[str, list[str]], start: str, doel: str, verbose: bool = False
) -> list[str] | None:
    """DFS volgens de cursustekst: recursief, eerst zoeken in de diepte.

    Vindt snel een pad, maar niet noodzakelijk het kortste.
    """
    nodes = bouw_nodes(graaf)
    explored: set[str] = set()
    return dfs_recursive(nodes[start], nodes[doel], explored, verbose)


def dfs_recursive(
    node: Node, goal_node: Node, explored: set[str], verbose: bool = False, diepte: int = 0
) -> list[str] | None:
    """Recursieve hulpfunctie voor depth_first_search (zie cursustekst)."""
    if verbose:
        print(f"{'  ' * diepte}bezoek: {node.state.name}")
    if node.state.name == goal_node.state.name:
        return reconstruct_pad(node)
    explored.add(node.state.name)
    for action in node.actions:
        if action.state.name not in explored:
            if action.parent is None:
                action.parent = node
            resultaat = dfs_recursive(action, goal_node, explored, verbose, diepte + 1)
            if resultaat:
                return resultaat
    return None


def naar_mermaid(graaf):
    """Exporteer de graaf als mermaid flowchart (elke rand één keer)."""
    regels = ["flowchart LR"]
    gezien = set()
    for stad, verbindingen in graaf.items():
        for buur in verbindingen:
            rand = frozenset({stad, buur})
            if rand not in gezien:
                gezien.add(rand)
                regels.append(f"    {stad} --- {buur}")
    return "\n".join(regels)
