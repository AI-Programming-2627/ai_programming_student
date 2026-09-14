"""
Week 02 Tests: Movement — Four Directions + Wall Detection
"""

from week02.solution import Environment, FloorCleaningAgent

WEIGHTS = {
    "test_move_right": 1,
    "test_move_down": 1,
    "test_move_up": 1,
    "test_move_left": 1,
    "test_move_blocked_by_wall_up": 1,
    "test_move_blocked_by_wall_left": 1,
}


def test_move_right():
    """Agent can move right and updates its position."""
    env = Environment(10, 5)
    agent = FloorCleaningAgent(env, start_x=0, start_y=0)
    result = agent.move_right()
    assert result is True
    assert agent.get_position() == (1, 0)


def test_move_down():
    """Agent can move down and updates its position."""
    env = Environment(10, 5)
    agent = FloorCleaningAgent(env, start_x=0, start_y=0)
    result = agent.move_down()
    assert result is True
    assert agent.get_position() == (0, 1)


def test_move_up():
    """Agent can move up from a non-edge position."""
    env = Environment(10, 5)
    agent = FloorCleaningAgent(env, start_x=5, start_y=3)
    result = agent.move_up()
    assert result is True
    assert agent.get_position() == (5, 2)


def test_move_left():
    """Agent can move left from a non-edge position."""
    env = Environment(10, 5)
    agent = FloorCleaningAgent(env, start_x=5, start_y=3)
    result = agent.move_left()
    assert result is True
    assert agent.get_position() == (4, 3)


def test_move_blocked_by_wall_up():
    """Agent cannot move up from the top row (wall detected)."""
    env = Environment(10, 5)
    agent = FloorCleaningAgent(env, start_x=0, start_y=0)
    result = agent.move_up()
    assert result is False, "move_up at top row should fail"
    assert agent.get_position() == (0, 0)


def test_move_blocked_by_wall_left():
    """Agent cannot move left from the leftmost column (wall detected)."""
    env = Environment(10, 5)
    agent = FloorCleaningAgent(env, start_x=0, start_y=0)
    result = agent.move_left()
    assert result is False, "move_left at leftmost column should fail"
    assert agent.get_position() == (0, 0)
