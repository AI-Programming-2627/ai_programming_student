"""
Week 09 Tests: Time-Based Soiling
"""

from exercises.week09.solution import Environment, FloorCleaningAgent

WEIGHTS = {
    "test_step_time_less_than_7_days": 1,
    "test_step_time_more_than_7_days": 2,
    "test_obstacle_tiles_never_soiled": 1,
    "test_different_tiles_soiled_at_different_times": 2,
}


def test_step_time_less_than_7_days():
    """A cleaned tile stays clean when less than 7 days pass."""
    env = Environment(5, 5)
    env.clean(2, 2)
    assert env.is_dirty(2, 2) is False
    env.step_time(3)
    assert env.is_dirty(2, 2) is False, "Tile should still be clean after 3 days"


def test_step_time_more_than_7_days():
    """A cleaned tile becomes dirty again after 7+ days."""
    env = Environment(5, 5)
    env.clean(2, 2)
    assert env.is_dirty(2, 2) is False
    env.step_time(8)
    assert env.is_dirty(2, 2) is True, "Tile should be dirty after 8 days"


def test_obstacle_tiles_never_soiled():
    """Obstacle tiles are not affected by time-based soiling."""
    env = Environment(5, 5)
    env.add_obstacle(2, 2)
    env.step_time(10)
    assert env.is_blocked(2, 2) is True


def test_different_tiles_soiled_at_different_times():
    """Tiles cleaned at different times become dirty at different times."""
    env = Environment(5, 5)
    env.clean(0, 0)      # cleaned at t=0
    env.step_time(3)
    env.clean(1, 0)      # cleaned at t=3
    env.step_time(3)     # total time = 6
    # (0,0): cleaned at t=0, 6 days passed — still clean
    assert env.is_dirty(0, 0) is False, "(0,0): only 6 days passed"
    # (1,0): cleaned at t=3, 3 days passed — still clean
    assert env.is_dirty(1, 0) is False, "(1,0): only 3 days passed"
    env.step_time(2)     # total time = 8
    # (0,0): 8 days passed — dirty!
    assert env.is_dirty(0, 0) is True, "(0,0): 8 days passed, should be dirty"
    # (1,0): 5 days passed — still clean
    assert env.is_dirty(1, 0) is False, "(1,0): only 5 days passed, should be clean"
