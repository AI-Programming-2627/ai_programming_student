"""
Week 04 Tests: Empty Room Sweep — Zigzag Cleaning
"""

from week04.solution import Environment, FloorCleaningAgent

WEIGHTS = {
    "test_clean_empty_room_all_tiles": 2,
    "test_clean_empty_room_returns_to_start": 1,
    "test_clean_empty_room_log_entries": 1,
    "test_agent_visits_all_tiles": 1,
}


def test_clean_empty_room_all_tiles():
    """Agent cleans all 50 tiles in a 10x5 empty room."""
    env = Environment(10, 5)
    agent = FloorCleaningAgent(env)
    agent.clean()
    assert env.count_dirty_tiles() == 0, "Not all tiles were cleaned!"


def test_clean_empty_room_returns_to_start():
    """Agent returns to the charging station (0,0) after cleaning."""
    env = Environment(10, 5)
    agent = FloorCleaningAgent(env, start_x=0, start_y=0)
    agent.clean()
    assert agent.get_position() == (0, 0), "Agent should return to (0,0)"


def test_clean_empty_room_log_entries():
    """The clean() method returns a log with meaningful entries."""
    env = Environment(10, 5)
    agent = FloorCleaningAgent(env)
    log = agent.clean()
    assert len(log) >= 3
    assert "Starting" in log[0]
    assert "Cleaning complete" in log[-1]


def test_agent_visits_all_tiles():
    """Agent visits at least 48 of the 50 tiles during cleaning."""
    env = Environment(10, 5)
    agent = FloorCleaningAgent(env)
    agent.clean()
    assert agent.get_visited_count() >= 48, "Agent didn't visit enough tiles"
