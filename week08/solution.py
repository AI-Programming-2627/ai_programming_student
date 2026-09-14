"""
Week 08: BFS Pathfinding

Focus: Implementing BFS (Breadth-First Search) to find optimal
paths around obstacles. The agent plans its route rather than
relying solely on reactive bumper behavior.

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

    def add_obstacle(self, x, y):
        if self._in_bounds(x, y):
            self.obstacles[y][x] = True

    def clean(self, x, y):
        if self._in_bounds(x, y):
            self.dirt[y][x] = False
            self.last_cleaned[y][x] = self.time

    def set_charger(self, x, y):
        if self._in_bounds(x, y):
            self.dirt[y][x] = False
            self.last_cleaned[y][x] = 0
        return (x, y)

    def count_dirty_tiles(self):
        count = 0
        for y in range(self.height):
            for x in range(self.width):
                if not self.obstacles[y][x] and self.dirt[y][x]:
                    count += 1
        return count

    def count_reachable_tiles(self):
        count = 0
        for y in range(self.height):
            for x in range(self.width):
                if not self.obstacles[y][x]:
                    count += 1
        return count


class FloorCleaningAgent:
    """Agent with BFS pathfinding for optimal navigation."""

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
        self.time = 0
        self.log = []

    def get_position(self):
        return (self.x, self.y)

    def get_model_cell(self, x, y):
        return self.model[y][x]

    def get_visited_count(self):
        return sum(sum(1 for v in row if v) for row in self.visited)

    def sense_bump(self, direction):
        dx, dy = self.DIR_VECTORS[direction]
        nx, ny = self.x + dx, self.y + dy
        return self.env.is_blocked(nx, ny)

    def move_up(self):
        pass

    def move_down(self):
        pass

    def move_left(self):
        pass

    def move_right(self):
        pass

    def sense_dirt(self):
        return self.env.is_dirty(self.x, self.y)

    def clean_tile(self):
        if self.env.is_dirty(self.x, self.y):
            self.env.clean(self.x, self.y)
            self.last_cleaned[self.y][self.x] = self.time
            return True
        return False

    def update_model(self):
        if self.sense_dirt():
            self.model[self.y][self.x] = 'dirty'
        else:
            self.model[self.y][self.x] = 'clean'
        for direction in self.DIR_VECTORS:
            if self.sense_bump(direction):
                dx, dy = self.DIR_VECTORS[direction]
                nx, ny = self.x + dx, self.y + dy
                if self.env._in_bounds(nx, ny):
                    self.model[ny][nx] = 'obstacle'

    def _bfs(self, start_x, start_y, target_x, target_y):
        """
        BFS pathfinding from (start_x, start_y) to (target_x, target_y).
        Returns a list of (x, y) steps from start to target (excluding start),
        or None if no path exists.
        """
        pass

    def _navigate_to(self, target_x, target_y):
        """Navigate to (target_x, target_y) using BFS."""
        pass

    def clean(self):
        pass