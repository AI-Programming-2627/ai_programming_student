"""
Week 06 Tests: Navigate Around a Single Obstacle
"""

from exercises.week06.solution import Environment, FloorCleaningAgent

WEIGHTS = {
    "test_single_obstacle_model_marked": 1,
    "test_clean_room_with_one_obstacle": 2,
    "test_obstacle_tile_not_cleaned": 1,
}


def test_single_obstacle_model_marked():
    """Obstacle tile is marked as 'obstacle' in agent's model after cleaning."""
    env = Environment(5, 5)
    env.add_obstacle(1, 0)
    agent = FloorCleaningAgent(env)
    agent.clean()
    assert agent.get_model_cell(1, 0) == 'obstacle', \
        f"Expected 'obstacle', got '{agent.get_model_cell(1, 0)}'"


def test_clean_room_with_one_obstacle():
    """Agent cleans all reachable tiles despite one obstacle."""
    env = Environment(5, 5)
    env.add_obstacle(1, 0)
    agent = FloorCleaningAgent(env)
    agent.clean()
    reachable = env.count_reachable_tiles()  # 25 - 1 = 24
    dirty = env.count_dirty_tiles()
    assert dirty == 0, f"Expected 0 dirty tiles, got {dirty}"
    assert agent.get_position() == (0, 0), "Agent should return to (0,0)"


def test_obstacle_tile_not_cleaned():
    """Obstacle tiles are not reachable and should not be cleaned."""
    env = Environment(5, 5)
    env.add_obstacle(2, 2)
    assert env.is_blocked(2, 2) is True
    assert env.count_reachable_tiles() == 24  # 25 - 1 obstacle
