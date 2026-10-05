"""De volledige stedengraaf van Antwerpen naar Parijs (startversie).

Gedeeld door de BFS- en DFS-demo's: alle verbindingen komen
letterlijk uit de regio-slides van week 3.
Vul zelf de functies buren, reconstruct_pad, breadth_first_search
en depth_first_search in.
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


def buren(graaf, stad):
    """Geef de buren van een stad, in de volgorde van de graaf."""
    pass


def reconstruct_pad(ouder, doel):
    """Bouw het gevonden pad op via de ouder-verwijzingen."""
    pass


def breadth_first_search(graaf, start, doel, verbose=False):
    """BFS: openklappen niveau per niveau via een FIFO-queue.

    Vindt het pad met het minste aantal steden.
    """
    pass


def depth_first_search(graaf, start, doel, explored=None, ouder=None, verbose=False, diepte=0):
    """DFS: recursief, eerst zoeken in de diepte.

    Vindt snel een pad, maar niet noodzakelijk het kortste.
    """
    pass


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
