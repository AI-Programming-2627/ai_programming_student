"""
Week 03 Tests: Cleaning — Dirt Sensor and Clean Tile
"""

from exercises.week03.solution import Environment, FloorCleaningAgent

WEIGHTS = {
    "test_env_clean_single_tile": 1,
    "test_agent_sense_dirt": 1,
    "test_agent_clean_tile": 1,
    "test_env_set_charger": 1,
}


def test_env_clean_single_tile():
    """Environment.clean() marks a tile as not dirty."""
    env = Environment(5, 5)
    assert env.is_dirty(2, 2) is True
    env.clean(2, 2)
    assert env.is_dirty(2, 2) is False


def test_agent_sense_dirt():
    """Agent can detect dirt on the current tile."""
    env = Environment(5, 5)
    agent = FloorCleaningAgent(env, start_x=0, start_y=0)
    # Starting tile should be dirty
    assert agent.sense_dirt() is True


def test_agent_clean_tile():
    """Agent can clean the tile it is standing on."""
    env = Environment(5, 5)
    agent = FloorCleaningAgent(env, start_x=0, start_y=0)
    assert env.is_dirty(0, 0) is True
    agent.clean_tile()
    assert env.is_dirty(0, 0) is False


def test_env_set_charger():
    """Setting a charger marks the tile as clean and tracks it."""
    env = Environment(5, 5)
    env.set_charger(2, 2)
    assert env.is_dirty(2, 2) is False
