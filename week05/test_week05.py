"""
Week 05 Tests: Bumper Sensor — Obstacle Detection & Model Updates
"""

from week05.solution import Environment, FloorCleaningAgent

WEIGHTS = {
    "test_add_obstacle": 1,
    "test_bumper_detects_obstacle_right": 1,
    "test_bumper_clear_down": 1,
    "test_model_updates_after_bump": 1,
}


def test_add_obstacle():
    """Environment.add_obstacle() marks a tile as blocked."""
    env = Environment(10, 5)
    env.add_obstacle(3, 2)
    assert env.is_blocked(3, 2) is True


def test_bumper_detects_obstacle_right():
    """Bumper sensor detects an obstacle to the right."""
    env = Environment(10, 5)
    env.add_obstacle(1, 0)
    agent = FloorCleaningAgent(env, start_x=0, start_y=0)
    assert agent.sense_bump('right') is True, "Should detect obstacle at (1,0)"


def test_bumper_clear_down():
    """Bumper returns False when no obstacle exists (except walls)."""
    env = Environment(10, 5)
    agent = FloorCleaningAgent(env, start_x=0, start_y=0)
    # Down from (0,0) should be clear (tile (0,1))
    assert agent.sense_bump('down') is False


def test_model_updates_after_bump():
    """After bumping, the agent's model marks the tile as obstacle."""
    env = Environment(5, 5)
    env.add_obstacle(1, 0)
    agent = FloorCleaningAgent(env, start_x=0, start_y=0)
    # Move right — should bump into obstacle
    result = agent.move_right()
    assert result is False, "Should be blocked by obstacle"
    # The model should now know (1,0) is an obstacle
    assert agent.get_model_cell(1, 0) == 'obstacle', \
        f"Expected 'obstacle', got '{agent.get_model_cell(1, 0)}'"
