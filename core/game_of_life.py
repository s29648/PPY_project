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
        self.generation += 1
        # no logic yet — just increments generation

    def clear(self):
        self.grid = [[False for _ in range(self.width)] for _ in range(self.height)]
        self.generation = 0