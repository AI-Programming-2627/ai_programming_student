"""
Week 10 Tests: Multi-Pass Cleaning
"""

from exercises.week10.solution import Environment, FloorCleaningAgent

WEIGHTS = {
    "test_first_pass_cleans_all": 1,
    "test_time_passes_tiles_get_dirty": 1,
    "test_second_pass_cleans_again": 2,
    "test_multiple_cleaning_cycles": 2,
}


def test_first_pass_cleans_all():
    """First cleaning pass cleans all tiles in an empty room."""
    env = Environment(5, 5)
    agent = FloorCleaningAgent(env)
    agent.clean()
    assert env.count_dirty_tiles() == 0, "All tiles should be clean after first pass"


def test_time_passes_tiles_get_dirty():
    """After 7 days, tiles become dirty again."""
    env = Environment(5, 5)
    agent = FloorCleaningAgent(env)
    agent.clean()
    assert env.count_dirty_tiles() == 0
    env.step_time(7)
    assert env.count_dirty_tiles() > 0, "Tiles should be dirty after 7 days"


def test_second_pass_cleans_again():
    """A second cleaning pass cleans tiles that became dirty again."""
    env = Environment(5, 5)
    agent = FloorCleaningAgent(env)
    agent.clean()
    assert env.count_dirty_tiles() == 0
    env.step_time(7)
    dirty_before = env.count_dirty_tiles()
    assert dirty_before > 0
    # Second pass
    agent2 = FloorCleaningAgent(env)
    agent2.clean()
    assert env.count_dirty_tiles() == 0, "All tiles should be clean after second pass"


def test_multiple_cleaning_cycles():
    """Agent can clean, wait, clean, wait, clean — multiple cycles."""
    env = Environment(5, 5)
    for cycle in range(3):
        agent = FloorCleaningAgent(env)
        agent.clean()
        assert env.count_dirty_tiles() == 0, \
            f"All tiles should be clean after pass {cycle + 1}"
        if cycle < 2:
            env.step_time(7)
            assert env.count_dirty_tiles() > 0, \
                f"Tiles should be dirty before pass {cycle + 2}"
