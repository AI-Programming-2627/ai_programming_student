"""
Week 08 Tests: BFS Pathfinding
"""

from exercises.week08.solution import Environment, FloorCleaningAgent

WEIGHTS = {
    "test_bfs_finds_path_in_empty_room": 2,
    "test_bfs_finds_path_around_obstacle": 2,
    "test_bfs_returns_none_if_unreachable": 1,
}


def test_bfs_finds_path_in_empty_room():
    """BFS finds a path from (0,0) to (9,4) in an empty 10x5 room."""
    env = Environment(10, 5)
    agent = FloorCleaningAgent(env)
    path = agent._bfs(0, 0, 9, 4)
    assert path is not None, "BFS should find a path"
    assert len(path) > 0, "Path should have steps"
    # Path should end at the target
    assert path[-1] == (9, 4), f"Path should end at (9,4), ends at {path[-1]}"
    # All steps should be valid adjacent moves
    cx, cy = 0, 0
    for step in path:
        dx = abs(step[0] - cx)
        dy = abs(step[1] - cy)
        assert dx + dy == 1, f"Step {step} is not adjacent to ({cx},{cy})"
        cx, cy = step


def test_bfs_finds_path_around_obstacle():
    """BFS routes around a wall of obstacles."""
    env = Environment(5, 5)
    # Create a wall at x=2 from y=0 to y=4
    for y in range(5):
        env.add_obstacle(2, y)
    agent = FloorCleaningAgent(env)
    path = agent._bfs(0, 0, 4, 4)
    assert path is not None, "BFS should find a path around the wall"
    assert path[-1] == (4, 4), f"Path should end at (4,4), ends at {path[-1]}"


def test_bfs_returns_none_if_unreachable():
    """BFS returns None when target is completely walled off."""
    env = Environment(5, 5)
    # Wall off the right half
    for y in range(5):
        env.add_obstacle(3, y)
    agent = FloorCleaningAgent(env)
    path = agent._bfs(0, 0, 4, 4)
    assert path is None, "BFS should return None for unreachable target"
