"""Test 3: Time-based dirt accumulation (tiles become dirty after 7 days)."""

from solution_floor_cleaning import Environment, FloorCleaningAgent

# Weight per test for scoring (out of 20 total across all test files)
WEIGHTS = {
    "test_env_step_time_marks_cleaned_tiles_dirty": 1,
    "test_agent_does_second_pass_after_time_passes": 2,
    "test_different_tiles_soiled_at_different_times": 2,
    "test_obstacle_tiles_never_soiled": 1,
    "test_cleaning_after_time_soiling": 2,
}


def test_env_step_time_marks_cleaned_tiles_dirty():
    """After 7+ days, a cleaned tile becomes dirty again."""
    env = Environment(5, 5)

    # Clean a specific tile
    env.clean(2, 2)
    assert env.is_dirty(2, 2) is False, "Tile should be clean after cleaning"

    # Advance time — less than 7 days, should stay clean
    env.step_time(3)
    assert env.is_dirty(2, 2) is False, "Tile should still be clean after 3 days"

    # Advance time past 7 days
    env.step_time(5)  # total time = 8
    assert env.is_dirty(2, 2) is True, "Tile should be dirty after 7+ days"


def test_agent_does_second_pass_after_time_passes():
    """After cleaning, if time passes, the agent can clean again."""
    env = Environment(5, 5)
    agent = FloorCleaningAgent(env)

    # First pass: clean everything
    agent.clean()
    assert env.count_dirty_tiles() == 0, "All tiles should be clean after first pass"

    # Simulate 7 days passing
    env.step_time(7)

    # Now tiles should be dirty again
    assert env.count_dirty_tiles() > 0, "Tiles should be dirty after 7 days"

    # Second pass: clean again
    agent2 = FloorCleaningAgent(env)
    agent2.clean()
    assert env.count_dirty_tiles() == 0, "All tiles should be clean after second pass"


def test_different_tiles_soiled_at_different_times():
    """Tiles cleaned at different times become dirty at different times."""
    env = Environment(5, 5)

    # Clean tile (0,0) at time 0
    env.clean(0, 0)

    # Advance time 3 days, clean tile (1,0)
    env.step_time(3)
    env.clean(1, 0)

    # Advance time 3 more days (total = 6)
    # Tile (0,0) was cleaned at t=0, so at t=6 it's been 6 days — still clean
    # Tile (1,0) was cleaned at t=3, so at t=6 it's been 3 days — still clean
    env.step_time(3)
    assert env.is_dirty(0, 0) is False, "(0,0): only 6 days passed"
    assert env.is_dirty(1, 0) is False, "(1,0): only 3 days passed"

    # Advance 2 more days (total = 8)
    # Tile (0,0): 8 days passed — dirty!
    # Tile (1,0): 5 days passed — still clean
    env.step_time(2)
    assert env.is_dirty(0, 0) is True, "(0,0): 8 days passed, should be dirty"
    assert env.is_dirty(1, 0) is False, "(1,0): only 5 days passed, should be clean"


def test_obstacle_tiles_never_soiled():
    """Obstacle tiles are not affected by time-based soiling."""
    env = Environment(5, 5)
    env.add_obstacle(2, 2)

    # The obstacle tile is not a cleanable tile, so it should not be counted
    env.step_time(10)
    # Obstacle tiles are not counted in dirty_tiles
    # The obstacle may have 'dirt' flag but it's not a reachable tile
    assert env.is_blocked(2, 2) is True


def test_cleaning_after_time_soiling():
    """After tiles become dirty from time, cleaning them again works."""
    env = Environment(5, 5)
    agent = FloorCleaningAgent(env)

    # Clean everything
    agent.clean()
    assert env.count_dirty_tiles() == 0

    # Wait 7 days — tiles become dirty
    env.step_time(7)
    dirty_before = env.count_dirty_tiles()
    assert dirty_before > 0, "There should be dirty tiles after 7 days"

    # Clean again
    agent2 = FloorCleaningAgent(env)
    agent2.clean()
    assert env.count_dirty_tiles() == 0, "All tiles should be clean after second clean"