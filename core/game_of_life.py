"""
Game of Life Logic Module

This module defines the core logic for customizable version of Conway's Game of Life.
It provides grid state management and rules for updating generations.

Author: Shehabeldin Mohamed
Version: 1.0
"""

class GameOfLife:
    """
    Supports wraparound edges and configurable rules as follows:
    A live cell survives if alive neighbors are within under/overpopulation limits.
    A dead cell becomes alive if it has exactly `custom_reproduction_number` neighbors.

    Args:
        width (int): Width of the grid in cells.
        height (int): Height of the grid in cells.
        wrap (bool): Whether the grid wraps around the edges.
    """

    def __init__(self, width: int, height: int, wrap: bool = False):
        self.width = width
        self.height = height
        self.wrap = wrap
        self.generation = 0
        self.grid = [[False for _ in range(width)] for _ in range(height)]
        self.custom_overpopulation_limit = 7
        self.custom_underpopulation_limit = 1
        self.custom_reproduction_number = 4

    def toggle_cell(self, x: int, y: int):
        """
        Toggle the alive/dead state of a cell.

        Args:
            x (int): X-coordinate of the cell.
            y (int): Y-coordinate of the cell.
        """
        self.grid[y][x] = not self.grid[y][x]

    def next_generation(self):
        """
        Advance the simulation by one generation using standard Game of Life rules.
        """
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

    def next_generation_custom(self):
        """
        Advance the simulation by one generation using custom rules.
        """
        new_grid = [[False for _ in range(self.width)] for _ in range(self.height)]

        for y in range(self.height):
            for x in range(self.width):
                alive_neighbors = self.count_alive_neighbors(x, y)
                cell_alive = self.grid[y][x]

                if cell_alive:
                    if self.custom_underpopulation_limit <= alive_neighbors <= self.custom_overpopulation_limit:
                        new_grid[y][x] = True
                else:
                    if alive_neighbors == self.custom_reproduction_number:
                        new_grid[y][x] = True

        self.grid = new_grid
        self.generation += 1

    def count_alive_neighbors(self, x: int, y: int) -> int:
        """
        Count the number of alive neighbors for the cell at (x, y).

        Args:
            x (int): X-coordinate of the cell.
            y (int): Y-coordinate of the cell.

        Returns:
            (int) Number of alive neighboring cells.
        """
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1), (0, 1),
                      (1, -1), (1, 0), (1, 1)]
        count = 0

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if self.wrap:
                nx %= self.width
                ny %= self.height
            if 0 <= nx < self.width and 0 <= ny < self.height:
                if self.grid[ny][nx]:
                    count += 1

        return count

    def set_custom_rules(self, overpop: int, underpop: int, repro: int):
        """
        Set custom rules for cell survival and reproduction.

        Args:
            overpop (int): Maximum neighbors before a cell dies from overpopulation.
            underpop (int): Minimum neighbors for a live cell to survive.
            repro (int): Exact number of neighbors required for a dead cell to reproduce.
        """
        self.custom_overpopulation_limit = overpop
        self.custom_underpopulation_limit = underpop
        self.custom_reproduction_number = repro

    def reset_custom_rules(self):
        """
        Reset the rules to standard Game of Life rules
        """
        self.custom_overpopulation_limit = 3
        self.custom_underpopulation_limit = 2
        self.custom_reproduction_number = 3

    def clear(self):
        """
        Reset the grid to all dead cells and reset generation count.
        """
        self.grid = [[False for _ in range(self.width)] for _ in range(self.height)]
        self.generation = 0

    def get_generation(self) -> int:
        """
        Returns the current generation number.
        """
        return self.generation