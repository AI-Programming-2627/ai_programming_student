"""
Week 03: Cleaning — Dirt Sensor and Clean Tile

Focus: Adding a dirt sensor (sense_dirt) and the clean_tile action.
The agent can now detect whether the current tile is dirty and clean it.

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

    def clean(self, x, y):
        """Clean the tile at (x, y), marking it as not dirty."""
        raise NotImplementedError("Implement in Week 03")

    def set_charger(self, x, y):
        """Place the charging station at (x, y)."""
        raise NotImplementedError("Implement in Week 03")

    def count_dirty_tiles(self):
        raise NotImplementedError("Implement in Week 03")

    def count_reachable_tiles(self):
        raise NotImplementedError("Implement in Week 03")


class FloorCleaningAgent:
    """Agent that can sense dirt and clean the current tile."""

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
        self.last_cleaned = [[-1 for _ in range(environment.width)]
                             for _ in range(environment.height)]

    def get_position(self):
        raise NotImplementedError("Implement in Week 03")

    def get_model_cell(self, x, y):
        raise NotImplementedError("Implement in Week 03")

    def get_visited_count(self):
        raise NotImplementedError("Implement in Week 03")

    def sense_bump(self, direction):
        raise NotImplementedError("Implement in Week 03")

    def move_up(self):
        raise NotImplementedError("Implement in Week 03")

    def move_down(self):
        raise NotImplementedError("Implement in Week 03")

    def move_left(self):
        raise NotImplementedError("Implement in Week 03")

    def move_right(self):
        raise NotImplementedError("Implement in Week 03")

    def sense_dirt(self):
        """Return True if the current tile is dirty."""
        raise NotImplementedError("Implement in Week 03")

    def clean_tile(self):
        """Clean the current tile. Returns True if something was cleaned."""
        raise NotImplementedError("Implement in Week 03")

    def update_model(self):
        """Update the internal model based on current sensor readings."""
        raise NotImplementedError("Implement in Week 03")
