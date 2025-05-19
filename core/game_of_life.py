# TODO: game logic


class GameOfLife:
    def __init__(self, width, height, wrap=False):
        self.width = width
        self.height = height
        self.wrap = wrap
        self.generation = 0
        self.grid = [[False for _ in range(width)] for _ in range(height)]

    def toggle_cell(self, x, y):
        self.grid[y][x] = not self.grid[y][x]

    def next_generation(self):
        new_grid = [[False for _ in range(self.width)] for _ in range(self.height)]

        for y in range(self.height):
            for x in range(self.width):
                alive_neighbors = self.count_alive_neighbors(x, y)
                cell_alive = self.grid[y][x]

                if cell_alive:
                    if alive_neighbors in (2, 3):
                        new_grid[y][x] = True
                else:
                    if alive_neighbors == 3:
                        new_grid[y][x] = True

        self.grid = new_grid
        self.generation += 1

    def count_alive_neighbors(self, x, y):
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1), (0, 1),
                      (1, -1), (1, 0), (1, 1)]
        count = 0

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if self.wrap:
                nx %= self.width
                ny %= self.height
                if self.grid[ny][nx]:
                    count += 1
            elif 0 <= nx < self.width and 0 <= ny < self.height:
                if self.grid[ny][nx]:
                    count += 1

        return count

    def clear(self):
        self.grid = [[False for _ in range(self.width)] for _ in range(self.height)]
        self.generation = 0