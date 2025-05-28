class InfiniteGameOfLife:
    """
    Implementation of Conway's Game of Life with infinite grid.
    Uses dictionary to store only live cells, allowing for infinite expansion.
    Coordinates can be any integer (positive or negative).

    Author: Darya Sharnevich
    Version: 1.0
    """
    def __init__(self):
        """Initialize empty infinite grid."""
        # format: {(x, y): 1}
        self.live_cells = {}
        self.generation = 0

        # default rules
        self.underpopulation_limit = 2
        self.overpopulation_limit = 3
        self.reproduction_number = 3

    def toggle_cell(self, x, y):
        """Toggle cell state at given coordinates."""
        if (x, y) in self.live_cells:
            del self.live_cells[(x, y)]
        else:
            self.live_cells[(x, y)] = 1

    def _count_neighbors(self, x, y):
        """Count live neighbors for a cell. Returns number of live neighbors"""
        count = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                if (x + dx, y + dy) in self.live_cells:
                    count += 1
        return count

    def _get_cells_to_check(self):
        """Get set of all cells that need to be checked for the next generation."""
        cells_to_check = set()
        
        # add all live cells and their neighbors
        for x, y in self.live_cells:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    cells_to_check.add((x + dx, y + dy))
                    
        return cells_to_check

    def next_generation(self):
        """Calculate the next generation of cells."""
        if not self.live_cells:
            return

        new_cells = {}
        cells_to_check = self._get_cells_to_check()

        for x, y in cells_to_check:
            neighbors = self._count_neighbors(x, y)

            # apply rules
            if (x, y) in self.live_cells:
                if self.underpopulation_limit <= neighbors <= self.overpopulation_limit:
                    new_cells[(x, y)] = 1
            else:
                if neighbors == self.reproduction_number:
                    new_cells[(x, y)] = 1

        self.live_cells = new_cells
        self.generation += 1

    def set_custom_rules(self, underpop, overpop, repro):
        """Set custom rules for cell survival and reproduction."""
        self.underpopulation_limit = underpop
        self.overpopulation_limit = overpop
        self.reproduction_number = repro

    def clear(self):
        """Clear the grid and reset generation counter."""
        self.live_cells.clear()
        self.generation = 0