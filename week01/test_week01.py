"""
Week 01 Tests: Environment + Agent Initialization

Tests that the Environment and FloorCleaningAgent classes can be
instantiated and that basic position / model queries work.
"""

from week01.solution import Environment, FloorCleaningAgent

WEIGHTS = {
    "test_environment_creation": 1,
    "test_agent_initialization": 1,
    "test_get_position": 1,
    "test_get_model_cell_charging_station": 1,
    "test_unknown_tiles_outside_start": 1,
}


def test_environment_creation():
    """A 10x5 Environment can be created and reports correct dimensions."""
    env = Environment(10, 5)
    assert env.width == 10
    assert env.height == 5
    # All tiles should start dirty
    assert env.is_dirty(0, 0) is True
    assert env.is_dirty(9, 4) is True


def test_agent_initialization():
    """Agent can be created with a given environment."""
    env = Environment(10, 5)
    agent = FloorCleaningAgent(env, start_x=0, start_y=0)
    assert agent is not None
    assert agent.env is env


def test_get_position():
    """Agent reports its starting position correctly."""
    env = Environment(10, 5)
    agent = FloorCleaningAgent(env, start_x=2, start_y=3)
    pos = agent.get_position()
    assert pos == (2, 3), f"Expected (2, 3), got {pos}"


def test_get_model_cell_charging_station():
    """The starting tile is marked as 'charging_station' in the model."""
    env = Environment(10, 5)
    agent = FloorCleaningAgent(env, start_x=0, start_y=0)
    assert agent.get_model_cell(0, 0) == 'charging_station'


def test_unknown_tiles_outside_start():
    """Tiles other than the start position should be 'unknown'."""
    env = Environment(10, 5)
    agent = FloorCleaningAgent(env, start_x=0, start_y=0)
    assert agent.get_model_cell(1, 0) == 'unknown'
    assert agent.get_model_cell(0, 1) == 'unknown'
    assert agent.get_model_cell(5, 3) == 'unknown'
