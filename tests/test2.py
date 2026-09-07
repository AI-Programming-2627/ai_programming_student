"""Test 2: Obstacle detection and avoidance."""

from solution_floor_cleaning import Environment, FloorCleaningAgent


def test_bumper_detects_obstacle():
    """Bumper sensor detects obstacles placed in the environment."""
    env = Environment(10, 5)
    env.add_obstacle(1, 0)  # Place obstacle to the right of start

    agent = FloorCleaningAgent(env)

    # Bumper should detect obstacle to the right
    assert agent.sense_bump('right') is True, "Bumper should detect obstacle at (1,0)"

    # Other directions should be clear (except walls)
    # (0,0) is top-left; up and left are walls, down is clear
    assert agent.sense_bump('down') is False, "(0,1) should be clear"


def test_agent_goes_around_single_obstacle():
    """Agent can navigate around a single obstacle."""
    env = Environment(5, 5)
    env.add_obstacle(1, 0)  # Block the tile right of start

    agent = FloorCleaningAgent(env)
    agent.clean()

    # Obstacle tile should be marked as obstacle in the model
    assert agent.get_model_cell(1, 0) == 'obstacle'

    # All non-obstacle tiles should be clean
    reachable = env.count_reachable_tiles()  # 25 - 1 = 24
    dirty = env.count_dirty_tiles()
    assert dirty == 0, f"Expected 0 dirty tiles, got {dirty}"


def test_agent_cleans_room_with_obstacles():
    """Agent cleans a room with multiple obstacles."""
    env = Environment(10, 5)
    # Place obstacles in a pattern
    env.add_obstacle(3, 1)
    env.add_obstacle(3, 2)
    env.add_obstacle(7, 3)
    env.add_obstacle(5, 0)

    agent = FloorCleaningAgent(env)
    agent.clean()

    # All non-obstacle tiles should be clean
    reachable = env.count_reachable_tiles()
    dirty = env.count_dirty_tiles()
    assert dirty == 0, f"Expected 0 dirty tiles, got {dirty}"

    # Obstacles should be in the agent's model
    assert agent.get_model_cell(3, 1) == 'obstacle'
    assert agent.get_model_cell(3, 2) == 'obstacle'
    assert agent.get_model_cell(7, 3) == 'obstacle'
    assert agent.get_model_cell(5, 0) == 'obstacle'

    # Agent should be back at charging station
    assert agent.get_position() == (0, 0)


def test_obstacle_tile_never_cleaned():
    """Obstacle tiles should never be marked as clean (they are not tiles)."""
    env = Environment(5, 5)
    env.add_obstacle(2, 2)

    # The obstacle tile should not be dirty (it's an obstacle, not a tile)
    # Initially the obstacle tile is marked dirty, but we should not clean it
    # because the agent can't reach it
    assert env.is_blocked(2, 2) is True

    # The obstacle tile is not counted as a reachable tile
    assert env.count_reachable_tiles() == 24  # 25 - 1 obstacle