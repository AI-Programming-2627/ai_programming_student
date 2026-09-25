"""
Oefening 2: Breadth-First Search
=================================
Implementeer BFS met backward printing van het pad.
"""
from collections import deque


class State:
    def __init__(self, name):
        self.name = name


class Node:
    def __init__(self, state):
        self.state = state
        self.actions = []

    def add_action(self, action):
        self.actions.append(action)


def breadth_first_search(initial_node, goal_state):
    # TODO: implementeer BFS met een queue
    # HINT: gebruik parent-tracking om het pad te reconstrueren
    pass


def print_path(parent, goal_node):
    # TODO: print het pad van start naar goal (backward printing)
    pass


if __name__ == "__main__":
    # Graaf opbouwen
    state_a = State("A")
    state_b = State("B")
    state_c = State("C")
    state_d = State("D")
    state_e = State("E")
    state_f = State("F")
    state_h = State("H")

    node_a = Node(state_a)
    node_b = Node(state_b)
    node_c = Node(state_c)
    node_d = Node(state_d)
    node_e = Node(state_e)
    node_f = Node(state_f)
    node_h = Node(state_h)

    node_a.add_action(node_b)
    node_a.add_action(node_c)
    node_b.add_action(node_d)
    node_b.add_action(node_e)
    node_c.add_action(node_f)
    node_f.add_action(node_h)

    solution = breadth_first_search(node_a, state_h)
    if solution:
        print("Oplossing gevonden! Doel:", solution.state.name)
    else:
        print("Geen oplossing.")