"""
Week 02: Movement — Four Directions + Wall Detection

Focus: Adding movement methods (move_up, move_down, move_left, move_right)
that update the agent's position and detect walls via the bumper sensor.

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
        return 0 <= x < self.width and 0 <= y < self.height

    def is_dirty(self, x, y):
        if not self._in_bounds(x, y):
            return False
        return self.dirt[y][x]

    def is_blocked(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return True
        return self.obstacles[y][x]

    def count_dirty_tiles(self):
        pass

    def count_reachable_tiles(self):
        pass


class FloorCleaningAgent:
    """Agent that can move in 4 directions and detect walls."""

    DIR_VECTORS = {
        'up': (0, -1),
        'down': (0, 1),
        'left': (-1, 0),
        'right': (1, 0),
    }

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
        pass

    def get_model_cell(self, x, y):
        pass

    def get_visited_count(self):
        pass

    def sense_bump(self, direction):
        """
        Bumper sensor. Returns True if there is a wall or obstacle
        in the given direction from the agent's current position.
        """
        pass

    def move_up(self):
        """Move one tile up. Returns True on success, False if blocked."""
        pass

    def move_down(self):
        """Move one tile down. Returns True on success, False if blocked."""
        pass

    def move_left(self):
        """Move one tile left. Returns True on success, False if blocked."""
        pass

    def move_right(self):
        """Move one tile right. Returns True on success, False if blocked."""
        pass