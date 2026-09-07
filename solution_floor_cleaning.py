
"""
Solution: Floor Cleaning Agent (Model-based Reflex Agent)

A robot vacuum cleaner that cleans a 10x5 grid of tiles.
The agent maintains an internal model of its environment, uses
sensors (dirt detector, bumper), and updates its state accordingly.

Strategy: Row-by-row sweep with BFS pathfinding to route around obstacles.
"""


class Environment:
    """The actual environment the robot operates in.

    Attributes:
        width, height: Grid dimensions (default 10 x 5).
        dirt[y][x]: True if tile (x, y) is dirty.
        obstacles[y][x]: True if there is an obstacle on tile (x, y).
        last_cleaned[y][x]: Environment time when tile was last cleaned (-1 = never).
        time: Global environment time counter (simulated days).
    """

    def __init__(self, width=10, height=5):
        self.width = width
        self.height = height
        self.dirt = [[True for _ in range(width)] for _ in range(height)]
        self.obstacles = [[False for _ in range(width)] for _ in range(height)]
        self.last_cleaned = [[-1 for _ in range(width)] for _ in range(height)]
        self.time = 0

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

    def clean(self, x, y):
        """Clean the tile at (x, y)."""
        if self._in_bounds(x, y):
            self.dirt[y][x] = False
            self.last_cleaned[y][x] = self.time

    def add_obstacle(self, x, y):
        """Place an obstacle at (x, y)."""
        if self._in_bounds(x, y):
            self.obstacles[y][x] = True

    def set_charger(self, x, y):
        """Place the charging station at (x, y). Tile is clean by default."""
        if self._in_bounds(x, y):
            self.dirt[y][x] = False
            self.last_cleaned[y][x] = 0
        return (x, y)

    def step_time(self, days=1):
        """Advance time. Tiles not cleaned for >= 7 days become dirty."""
        self.time += days
        for y in range(self.height):
            for x in range(self.width):
                if self.obstacles[y][x]:
                    continue
                if self.last_cleaned[y][x] >= 0:
                    if self.time - self.last_cleaned[y][x] >= 7:
                        self.dirt[y][x] = True

    def count_dirty_tiles(self):
        """Return the number of dirty tiles (excluding obstacles)."""
        count = 0
        for y in range(self.height):
            for x in range(self.width):
                if not self.obstacles[y][x] and self.dirt[y][x]:
                    count += 1
        return count

    def count_reachable_tiles(self):
        """Return the number of non-obstacle tiles."""
        count = 0
        for y in range(self.height):
            for x in range(self.width):
                if not self.obstacles[y][x]:
                    count += 1
        return count

    def _in_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def __str__(self):
        lines = []
        for y in range(self.height):
            row = ""
            for x in range(self.width):
                if self.obstacles[y][x]:
                    row += " X "
                elif self.dirt[y][x]:
                    row += " D "
                else:
                    row += " . "
            lines.append(row)
        return "\n".join(lines)


class FloorCleaningAgent:
    """Model-based reflex agent for floor cleaning.

    Internal state:
      - x, y: Current position (starts at the charging station, (0,0))
      - model[y][x]: What the agent believes about each tile
        ('unknown', 'clean', 'dirty', 'obstacle', 'charging_station')
      - visited[y][x]: Whether the agent has physically been on this tile
      - last_cleaned[y][x]: Agent's internal time when it last cleaned this tile
      - time: Agent's internal action counter

    Sensors:
      - sense_dirt(): Checks if the current tile is dirty (in the real env)
      - sense_bump(direction): Checks if a wall/obstacle blocks movement

    Transition model:
      - update_model(): Updates internal beliefs based on sensor readings

    Actions:
      - move_up(), move_down(), move_left(), move_right()
      - clean_tile()
      - stay()

    Strategy:
      - Row-by-row sweep (boustrophedon) with BFS pathfinding to
        route around obstacles discovered via the bumper.
    """

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

        # --- Internal model of the environment ---
        self.model = [
            ['unknown' for _ in range(environment.width)]
            for _ in range(environment.height)
        ]
        self.model[start_y][start_x] = 'charging_station'

        # --- Visited / last-cleaned trackers ---
        self.visited = [
            [False for _ in range(environment.width)]
            for _ in range(environment.height)
        ]
        self.visited[start_y][start_x] = True

        self.last_cleaned = [
            [-1 for _ in range(environment.width)]
            for _ in range(environment.height)
        ]

        # --- Agent's internal clock ---
        self.time = 0

        # --- Logging ---
        self.log = []
# -----------------------------------------------------------------
    # Sensors
    # -----------------------------------------------------------------

    def sense_dirt(self):
        """Return True if the tile under the robot is dirty."""
        return self.env.is_dirty(self.x, self.y)

    def sense_bump(self, direction):
        """Bumper sensor: return True if a wall/obstacle blocks 'direction'."""
        dx, dy = self.DIR_VECTORS[direction]
        return self.env.is_blocked(self.x + dx, self.y + dy)

    # -----------------------------------------------------------------
    # Transition model (update internal beliefs)
    # -----------------------------------------------------------------

    def update_model(self):
        """Update the internal model based on current sensor readings."""
        # Dirt sensor on current tile
        if self.sense_dirt():
            self.model[self.y][self.x] = 'dirty'
        elif self.model[self.y][self.x] != 'charging_station':
            self.model[self.y][self.x] = 'clean'

        # Bumper sensors in all four directions
        for direction in ('up', 'down', 'left', 'right'):
            if self.sense_bump(direction):
                dx, dy = self.DIR_VECTORS[direction]
                nx, ny = self.x + dx, self.y + dy
                if 0 <= nx < self.env.width and 0 <= ny < self.env.height:
                    self.model[ny][nx] = 'obstacle'
# -----------------------------------------------------------------
    # Actions
    # -----------------------------------------------------------------

    def clean_tile(self):
        """Clean the current tile. Returns True if it was actually dirty."""
        was_dirty = self.env.is_dirty(self.x, self.y)
        if was_dirty:
            self.env.clean(self.x, self.y)
            self.model[self.y][self.x] = 'clean'
            self.last_cleaned[self.y][self.x] = self.time
            self.log.append(f"  Cleaned ({self.x}, {self.y}) at t={self.time}")
        self.time += 1
        return was_dirty

    def move_up(self):
        """Move up one tile. Returns True if the move succeeded."""
        if self.y > 0 and not self.sense_bump('up'):
            self.y -= 1
            self.visited[self.y][self.x] = True
            self.time += 1
            return True
        return False

    def move_down(self):
        """Move down one tile. Returns True if the move succeeded."""
        if self.y < self.env.height - 1 and not self.sense_bump('down'):
            self.y += 1
            self.visited[self.y][self.x] = True
            self.time += 1
            return True
        return False

    def move_left(self):
        """Move left one tile. Returns True if the move succeeded."""
        if self.x > 0 and not self.sense_bump('left'):
            self.x -= 1
            self.visited[self.y][self.x] = True
            self.time += 1
            return True
        return False

    def move_right(self):
        """Move right one tile. Returns True if the move succeeded."""
        if self.x < self.env.width - 1 and not self.sense_bump('right'):
            self.x += 1
            self.visited[self.y][self.x] = True
            self.time += 1
            return True
        return False

    def stay(self):
        """Do nothing for one time unit."""
        self.time += 1
# -----------------------------------------------------------------
    # BFS Navigation
    # -----------------------------------------------------------------

    def _navigate_to(self, target_x, target_y):
        """Navigate to (target_x, target_y) using BFS through traversable tiles.

        Uses the internal model to avoid known obstacles. If a newly discovered
        obstacle blocks the path mid-route, re-routes automatically.
        Returns True if the target was reached.
        """
        from collections import deque

        if (self.x, self.y) == (target_x, target_y):
            return True

        path = self._bfs(target_x, target_y)
        if path is None:
            return False

        for step_x, step_y in path:
            self.update_model()
            moved = self._move_step(step_x, step_y)
            if not moved:
                # A new obstacle was discovered — re-plan
                return self._navigate_to(target_x, target_y)
        return (self.x, self.y) == (target_x, target_y)

    def _bfs(self, target_x, target_y):
        """BFS shortest path from (self.x, self.y) to (target_x, target_y).

        Considers a tile traversable if it is not marked 'obstacle' in the model.
        Returns a list of (x, y) steps, or None if no path exists.
        """
        from collections import deque

        def traversable(x, y):
            if not (0 <= x < self.env.width and 0 <= y < self.env.height):
                return False
            return self.model[y][x] != 'obstacle'

        start = (self.x, self.y)
        target = (target_x, target_y)

        if not traversable(*target):
            return None

        queue = deque()
        queue.append([start])
        visited = {start}

        while queue:
            path = queue.popleft()
            cx, cy = path[-1]

            for _dir, (dx, dy) in self.DIR_VECTORS.items():
                nx, ny = cx + dx, cy + dy
                if (nx, ny) == target:
                    # Return the steps from the current position to the target
                    return path[1:] + [(nx, ny)]
                if traversable(nx, ny) and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append(path + [(nx, ny)])

        return None  # no path found

    def _move_step(self, target_x, target_y):
        """Move one step from current position toward (target_x, target_y).

        The target must be adjacent (Manhattan distance = 1).
        Returns True if the move succeeded.
        """
        dx = target_x - self.x
        dy = target_y - self.y

        if abs(dx) + abs(dy) != 1:
            return False

        if dx == 1:
            return self.move_right()
        elif dx == -1:
            return self.move_left()
        elif dy == 1:
            return self.move_down()
        elif dy == -1:
            return self.move_up()
        return False

    # -----------------------------------------------------------------
    # Strategy: clean the entire room
    # -----------------------------------------------------------------

    def clean(self):
        """Main cleaning routine.

        Uses a row-by-row sweep (boustrophedon) with BFS to navigate
        around obstacles discovered via the bumper sensor. After the
        sweep, returns to the charging station at (0,0).
        """
        self.log = []
        self.log.append(f"Starting at ({self.x}, {self.y})")

        for row in range(self.env.height):
            # Determine scan direction for this row (zigzag)
            if row % 2 == 0:
                col_range = range(self.env.width)
            else:
                col_range = range(self.env.width - 1, -1, -1)

            for col in col_range:
                # Skip if we already know this tile is an obstacle
                if self.model[row][col] == 'obstacle':
                    continue

                # Navigate to the tile
                self._navigate_to(col, row)

                # Clean if dirty
                self.update_model()
                if self.sense_dirt():
                    self.clean_tile()
                else:
                    self.time += 1

        self.log.append("All tiles cleaned (first pass).")

        # Return to charging station
        self._navigate_to(0, 0)
        self.log.append("Returned to charging station.")
        self.log.append("Cleaning complete!")

        return self.log

    # -----------------------------------------------------------------
    # Inspection helpers
    # -----------------------------------------------------------------

    def get_position(self):
        """Return the current (x, y) position."""
        return (self.x, self.y)

    def get_model_cell(self, x, y):
        """Return what the agent believes about tile (x, y)."""
        return self.model[y][x]

    def get_visited_count(self):
        """Return the number of tiles the agent has visited."""
        return sum(sum(1 for v in row if v) for row in self.visited)

    def get_cleaned_count(self):
        """Return the number of tiles the agent has cleaned."""
        return sum(1 for row in self.last_cleaned for t in row if t >= 0)