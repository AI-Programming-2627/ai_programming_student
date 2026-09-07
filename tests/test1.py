"""Test 1: Basic cleaning of an empty room (no obstacles, no time-based soiling)."""

from solution_floor_cleaning import Environment, FloorCleaningAgent


def test_agent_initialization():
    """Verify the agent starts at (0,0) with a correct internal model."""
    env = Environment(10, 5)
    agent = FloorCleaningAgent(env, start_x=0, start_y=0)

    pos = agent.get_position()
    assert pos == (0, 0), f"Expected (0, 0), got {pos}"

    # The agent should know its starting tile is the charging station
    assert agent.get_model_cell(0, 0) == 'charging_station'

    # Other tiles should be unknown
    assert agent.get_model_cell(1, 0) == 'unknown'


def test_single_tile_clean():
    """Agent can clean the single tile it stands on."""
    env = Environment(10, 5)
    agent = FloorCleaningAgent(env)

    assert env.is_dirty(0, 0) is True
    agent.clean_tile()
    assert env.is_dirty(0, 0) is False


def test_move_right():
    """Agent can move right and updates its position."""
    env = Environment(10, 5)
    agent = FloorCleaningAgent(env)

    result = agent.move_right()
    assert result is True, "move_right should succeed"
    assert agent.get_position() == (1, 0)


def test_move_blocked_by_wall():
    """Agent cannot move outside the grid (wall detected by bumper)."""
    env = Environment(10, 5)
    agent = FloorCleaningAgent(env)

    # Try to move up from (0,0) — should be blocked by the top wall
    result = agent.move_up()
    assert result is False, "move_up at top row should fail"
    assert agent.get_position() == (0, 0)

    # Try to move left from (0,0) — blocked by left wall
    result = agent.move_left()
    assert result is False, "move_left at leftmost column should fail"


def test_clean_entire_room():
    """Agent cleans all 50 tiles in a 10x5 room with no obstacles."""
    env = Environment(10, 5)
    agent = FloorCleaningAgent(env)

    log = agent.clean()

    # All reachable tiles should now be clean
    assert env.count_dirty_tiles() == 0, "Not all tiles were cleaned!"

    # The agent should have visited many tiles
    assert agent.get_visited_count() >= 48, "Agent didn't visit enough tiles"

    # The agent should be back at the charging station
    assert agent.get_position() == (0, 0), "Agent should return to (0,0)"

    # Verify the log has entries
    assert len(log) >= 3
    assert "Starting" in log[0]
    assert "Cleaning complete" in log[-1]