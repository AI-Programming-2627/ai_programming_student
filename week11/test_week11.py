"""
Week 11 Tests: Full Solution — All Features Combined
"""

from week11.solution import Environment, FloorCleaningAgent

WEIGHTS = {
    "test_clean_room_with_obstacles_and_time": 3,
    "test_multi_pass_with_obstacles": 3,
    "test_all_features_combined": 3,
}


def test_clean_room_with_obstacles_and_time():
    """Agent cleans a room with obstacles, then handles time-based soiling."""
    env = Environment(10, 5)
    env.add_obstacle(3, 1)
    env.add_obstacle(7, 3)
    agent = FloorCleaningAgent(env)
    agent.clean()
    assert env.count_dirty_tiles() == 0, "All reachable tiles should be clean"
    assert agent.get_position() == (0, 0), "Agent should return to start"
    # After time passes
    env.step_time(7)
    assert env.count_dirty_tiles() > 0, "Tiles should be dirty after 7 days"
    # Clean again
    agent2 = FloorCleaningAgent(env)
    agent2.clean()
    assert env.count_dirty_tiles() == 0, "All tiles should be clean after second pass"


def test_multi_pass_with_obstacles():
    """Agent performs multiple cleaning cycles in a room with obstacles."""
    env = Environment(10, 5)
    env.add_obstacle(2, 0)
    env.add_obstacle(2, 1)
    env.add_obstacle(2, 2)
    for cycle in range(3):
        agent = FloorCleaningAgent(env)
        agent.clean()
        assert env.count_dirty_tiles() == 0, \
            f"All tiles clean after pass {cycle + 1}"
        if cycle < 2:
            env.step_time(7)
            assert env.count_dirty_tiles() > 0, \
                f"Tiles dirty before pass {cycle + 2}"


def test_all_features_combined():
    """Comprehensive test: obstacles + time + multi-pass + return to start."""
    env = Environment(10, 5)
    # Place obstacles
    env.add_obstacle(1, 1)
    env.add_obstacle(3, 3)
    env.add_obstacle(6, 2)
    env.add_obstacle(8, 4)
    # First clean
    agent = FloorCleaningAgent(env)
    agent.clean()
    reachable = env.count_reachable_tiles()
    assert env.count_dirty_tiles() == 0, "All reachable tiles should be clean"
    assert agent.get_position() == (0, 0), "Agent should return to (0,0)"
    # Model should have obstacles recorded
    assert agent.get_model_cell(1, 1) == 'obstacle'
    assert agent.get_model_cell(3, 3) == 'obstacle'
    assert agent.get_model_cell(6, 2) == 'obstacle'
    assert agent.get_model_cell(8, 4) == 'obstacle'
    # Time passes
    env.step_time(10)
    dirty_after_time = env.count_dirty_tiles()
    assert dirty_after_time > 0, "Tiles should be dirty after time passes"
    assert dirty_after_time <= reachable, "Only reachable tiles can be dirty"
    # Second clean
    agent2 = FloorCleaningAgent(env)
    agent2.clean()
    assert env.count_dirty_tiles() == 0, "All tiles clean after second pass"
    assert agent2.get_position() == (0, 0), "Agent should return to (0,0)"
