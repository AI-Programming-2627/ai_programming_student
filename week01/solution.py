"""
Week 01: Environment + Agent Initialization

Focus: Setting up the Environment class (grid, dirt, obstacles) and
initializing the FloorCleaningAgent with position tracking and a
simple internal model.

Placeholder — replace method bodies with real implementations.
"""


class Environment:
    """The actual environment the robot operates in."""

    def __init__(self, width=10, height=5):
        self.width = width
        self.height = height
        self.dirt = [[True for _ in range(width)] for _ in range(height)]
        self.obstacles = [[False for _ in range(width)] for _ in range(height)]
        self.last_cleaned = [[-1 for _ in range(width)] for _ in range(height)]
        self.time = 0

    def _in_bounds(self, x, y):
        """Return True if (x, y) is inside the grid."""
        return 0 <= x < self.width and 0 <= y < self.height

    def is_dirty(self, x, y):
        """Return True if tile (x, y) is dirty."""
        if not self._in_bounds(x, y):
            return False
        return self.dirt[y][x]

    def is_blocked(self, x, y):
        """Return True if (x, y) is blocked by an obstacle or wall."""
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return True
        return self.obstacles[y][x]

    def count_dirty_tiles(self):
        """Return the number of dirty tiles (excluding obstacles)."""
        pass

    def count_reachable_tiles(self):
        """Return the number of non-obstacle tiles."""
        pass


class FloorCleaningAgent:
    """A simple cleaning agent that starts at (0,0) and tracks its position."""

    MODEL_VALUES = ('unknown', 'clean', 'dirty', 'obstacle', 'charging_station')

    def __init__(self, environment, start_x=0, start_y=0):
        self.env = environment
        self.x = start_x
        self.y = start_y
        self.model = [['unknown' for _ in range(environment.width)]
                      for _ in range(environment.height)]
        self.model[start_y][start_x] = 'charging_station'
        self.visited = [[False for _ in range(environment.width)]
                        for _ in range(environment.height)]
        self.visited[start_y][start_x] = True

    def get_position(self):
        """Return the current (x, y) position."""
        pass

    def get_model_cell(self, x, y):
        """Return what the agent believes about tile (x, y)."""
        pass

    def get_visited_count(self):
        """Return the number of tiles the agent has visited."""
        pass