"""
Game of Life Logic Module

This module defines the core logic for Conway's Game of Life.
It provides grid state management and rules for updating generations.

Author: Shehabeldin Mohamed
Version: 1.0
"""

class GameOfLife:
    """
    Core logic for Conway's Game of Life.

    Args:
        width (int): Width of the grid in cells.
        height (int): Height of the grid in cells.
        wrap (bool): Whether the grid wraps around the edges.
        generation (int): The current generation count.
        grid (list[list[bool]]): 2D list representing the grid state (True for alive, False for dead).
    """

    def __init__(self, width: int, height: int, wrap: bool = False):
        self.width = width
        self.height = height
        self.wrap = wrap
        self.generation = 0
        self.grid = [[False for _ in range(width)] for _ in range(height)]

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
        Advance the simulation by one generation based on Game of Life rules.
        """
        new_grid = [[False for _ in range(self.width)] for _ in range(self.height)]

        for y in range(self.height):
            for x in range(self.width):
                alive_neighbors = self._count_alive_neighbors(x, y)
                cell_alive = self.grid[y][x]

                if cell_alive and alive_neighbors in (2, 3):
                    new_grid[y][x] = True
                elif not cell_alive and alive_neighbors == 3:
                    new_grid[y][x] = True

        self.grid = new_grid
        self.generation += 1

    def _count_alive_neighbors(self, x: int, y: int) -> int:
        """
        Count alive neighbors for a cell at (x, y).

        Args:
            x (int): X-coordinate of the cell.
            y (int): Y-coordinate of the cell.

        Returns:
            int: Number of alive neighboring cells.
        """
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),          (0, 1),
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

    def clear(self):
        """
        Reset the grid to all dead cells and reset generation count.
        """
        self.grid = [[False for _ in range(self.width)] for _ in range(self.height)]
        self.generation = 0

    def get_generation(self) -> int:
        """
        Get the current generation number.

        Returns:
            int: Current generation.
        """
        return self.generation