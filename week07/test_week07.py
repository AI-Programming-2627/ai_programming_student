"""
Week 07 Tests: Multiple Obstacles
"""

from week07.solution import Environment, FloorCleaningAgent

WEIGHTS = {
    "test_clean_room_with_multiple_obstacles": 2,
    "test_all_obstacles_in_model": 1,
    "test_agent_returns_to_start_after_multi_obstacle": 1,
    "test_count_reachable_excludes_obstacles": 1,
}


def test_clean_room_with_multiple_obstacles():
    """Agent cleans all reachable tiles with several obstacles."""
    env = Environment(10, 5)
    env.add_obstacle(3, 1)
    env.add_obstacle(3, 2)
    env.add_obstacle(7, 3)
    env.add_obstacle(5, 0)
    agent = FloorCleaningAgent(env)
    agent.clean()
    dirty = env.count_dirty_tiles()
    assert dirty == 0, f"Expected 0 dirty tiles, got {dirty}"


def test_all_obstacles_in_model():
    """All obstacles are marked in the agent's internal model."""
    env = Environment(10, 5)
    env.add_obstacle(3, 1)
    env.add_obstacle(3, 2)
    env.add_obstacle(7, 3)
    env.add_obstacle(5, 0)
    agent = FloorCleaningAgent(env)
    agent.clean()
    assert agent.get_model_cell(3, 1) == 'obstacle'
    assert agent.get_model_cell(3, 2) == 'obstacle'
    assert agent.get_model_cell(7, 3) == 'obstacle'
    assert agent.get_model_cell(5, 0) == 'obstacle'


def test_agent_returns_to_start_after_multi_obstacle():
    """Agent returns to charging station after cleaning with obstacles."""
    env = Environment(10, 5)
    env.add_obstacle(3, 1)
    env.add_obstacle(7, 3)
    agent = FloorCleaningAgent(env)
    agent.clean()
    assert agent.get_position() == (0, 0)


def test_count_reachable_excludes_obstacles():
    """Reachable tile count excludes obstacle tiles."""
    env = Environment(5, 5)
    env.add_obstacle(2, 2)
    assert env.count_reachable_tiles() == 24  # 25 - 1
    env.add_obstacle(0, 0)
    assert env.count_reachable_tiles() == 23  # 25 - 2
