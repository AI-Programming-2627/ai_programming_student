"""
Week 09: Time-Based Soiling

Focus: Tiles that were cleaned become dirty again after 7 days.
The Environment.step_time() method advances the clock and marks
tiles as dirty if they haven't been cleaned in >= 7 days.

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

    def step_time(self, days=1):
        """
        Advance time by `days`. Tiles not cleaned for >= 7 days
        become dirty again.
        """
        raise NotImplementedError("Implement in Week 09")

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
    """Agent that cleans in a timed environment."""

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
        raise NotImplementedError("Implement in Week 09")

    def move_down(self):
        raise NotImplementedError("Implement in Week 09")

    def move_left(self):
        raise NotImplementedError("Implement in Week 09")

    def move_right(self):
        raise NotImplementedError("Implement in Week 09")

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
        raise NotImplementedError("Implement in Week 09")

    def _navigate_to(self, target_x, target_y):
        raise NotImplementedError("Implement in Week 09")

    def clean(self):
        raise NotImplementedError("Implement in Week 09")
