from PyQt5.QtWidgets import QWidget, QSizePolicy
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QMouseEvent, QWheelEvent, QColor
from math import floor

class GridCanvas(QWidget):
    """
    Interactive canvas for displaying and manipulating the Game of Life grid.
    
    Supports:
    - Cell toggling with left mouse button
    - Grid panning with right mouse button
    - Zoom with mouse wheel
    - Fixed and infinite grid modes
    - Custom color schemes
    """
    def __init__(self, game, fixed_view_callable, zoom, offset, colors):
        """
        Initialize the grid canvas.

        Args:
            game: GameOfLife instance to visualize
            fixed_view_callable: Function that returns whether the view is fixed
            zoom: Initial zoom level
            offset: Initial view offset
            colors: Dictionary with color scheme (bg, grid, dead, live)
        """
        super().__init__()
        self.game = game
        self.fixed_view_callable = fixed_view_callable
        self.zoom = zoom
        self.offset = offset
        self.colors = colors
        self.base_cell_size = 20
        self.last_mouse_pos = None

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    # redefine QWidget paintEvent() to be called when paint event is issued (QWidget.update())
    def paintEvent(self, event):
        """Paint the grid and live cells based on current state."""
        qp = QPainter(self)
        qp.setRenderHint(QPainter.Antialiasing)
        qp.fillRect(self.rect(), self.colors['bg'])

        width, height = self.width(), self.height()
        cell_px = max(5, int(self.base_cell_size * self.zoom))

        if self.fixed_view_callable():
            cols, rows = self.game.width, self.game.height
            cell_px = min(width // cols, height // rows)
            x_offset = (width - cols * cell_px) // 2
            y_offset = (height - rows * cell_px) // 2

            for gx in range(cols):
                for gy in range(rows):
                    sx = x_offset + gx * cell_px
                    sy = y_offset + gy * cell_px

                    if self.game.grid[gy][gx]:
                        self._draw_live_cell(qp, sx, sy, cell_px)
                    else:
                        self._draw_dead_cell(qp, sx, sy, cell_px)
        else:
            dx = -(self.offset.x() % cell_px)
            dy = -(self.offset.y() % cell_px)
            
            start_x = self.offset.x() // cell_px
            start_y = self.offset.y() // cell_px

            # +1 additional cell in addition to all full cells
            cols = width // cell_px + 1
            rows = height // cell_px + 1

            # draw grid
            for i in range(cols):
                for j in range(rows):
                    # game coords
                    gx = start_x + i
                    gy = start_y + j

                    # screen coords
                    sx = i * cell_px + dx
                    sy = j * cell_px + dy

                    if (gx, gy) in self.game.live_cells:
                        self._draw_live_cell(qp, sx, sy, cell_px)
                    else:
                        self._draw_dead_cell(qp, sx, sy, cell_px)

    def mousePressEvent(self, event: QMouseEvent):
        """
        Handle cell toggling and drag start.
        
        Left button: Toggle cell state
        Right button: Start grid panning
        """
        if event.button() == Qt.LeftButton:
            coords = self._get_cell_coords(event.pos())
            if coords:
                self.game.toggle_cell(*coords)
                self.update()
            self.last_mouse_pos = event.pos()
        elif event.button() == Qt.RightButton:
            self.last_mouse_pos = event.pos()

    def mouseMoveEvent(self, event: QMouseEvent):
        """
        Handle panning of the view when dragging and enables drawing between cells.
        
        Right button: Pan the grid view
        Left button: Draw continuous line of live cells
        """
        if event.buttons() & Qt.RightButton and self.last_mouse_pos:
            delta = event.pos() - self.last_mouse_pos
            self.offset -= delta
            self.last_mouse_pos = event.pos()
            self.update()
        elif event.buttons() & Qt.LeftButton:
            current_pos = event.pos()
            coords1 = self._get_cell_coords(self.last_mouse_pos)
            coords2 = self._get_cell_coords(current_pos)

            if coords1 and coords2:
                self._draw_line_between_points(*coords1, *coords2)

            self.last_mouse_pos = current_pos
            self.update()

    def mouseReleaseEvent(self, event):
        """Reset drag state on mouse button release."""
        self.last_mouse_pos = None

    def wheelEvent(self, event: QWheelEvent):
        """
        Handle zoom in/out using mouse wheel.
        Maintains the center point during zoom.
        """
        if self.fixed_view_callable():
            return
            
        delta = event.angleDelta().y()
        if delta == 0:
            return

        old_zoom = self.zoom
        zoom_factor = 1.0 + (delta / 120)
        new_zoom = min(max(0.2, self.zoom * zoom_factor), 5.0)

        center_x = self.width() / 2
        center_y = self.height() / 2
        
        # convert center point to grid coordinates
        cell_px = max(5, int(self.base_cell_size * old_zoom))
        grid_x = (center_x + self.offset.x()) / cell_px
        grid_y = (center_y + self.offset.y()) / cell_px

        self.zoom = new_zoom
        
        # convert grid coordinates back to screen
        cell_px = max(5, int(self.base_cell_size * new_zoom))
        new_screen_x = grid_x * cell_px - center_x
        new_screen_y = grid_y * cell_px - center_y
        
        self.offset = QPoint(int(round(new_screen_x)), int(round(new_screen_y)))
        self.update()

    def _get_cell_coords(self, pos):
        """
        Convert screen coordinates to cell grid coordinates.
        
        Args:
            pos: QPoint with screen coordinates
            
        Returns:
            Tuple (x, y) with grid coordinates or None if outside grid
        """
        if not pos:
            return None
            
        width, height = self.width(), self.height()
        cell_px = max(5, int(self.base_cell_size * self.zoom))

        if self.fixed_view_callable():
            cell_px = min(width // self.game.width, height // self.game.height)
            x_offset = (width - self.game.width * cell_px) // 2
            y_offset = (height - self.game.height * cell_px) // 2

            x = (pos.x() - x_offset) // cell_px
            y = (pos.y() - y_offset) // cell_px

            if not (0 <= x < self.game.width and 0 <= y < self.game.height):
                return None
        else:
            x = (pos.x() + self.offset.x()) // cell_px
            y = (pos.y() + self.offset.y()) // cell_px

        return x, y

    def _draw_live_cell(self, qp, x, y, cell_px):
        """Helper method to draw a single cell."""
        qp.setBrush(self.colors['live'])
        # no border
        qp.setPen(Qt.NoPen)
        # move by 1px from start, size adjusted
        qp.drawRect(x + 1, y + 1, cell_px - 2, cell_px - 2)

    def _draw_dead_cell(self, qp, x, y, cell_px):
        """Helper method to draw a grid for cell."""
        qp.setPen(self.colors['grid'])
        qp.setBrush(self.colors['dead'])
        qp.drawRect(x, y, cell_px, cell_px)

    def _draw_line_between_points(self, x1, y1, x2, y2):
        """Draw a continuous line of live cells between two points using Bresenham's algorithm."""
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        while True:
            if self.fixed_view_callable():
                if 0 <= x1 < self.game.width and 0 <= y1 < self.game.height:
                    self.game.grid[y1][x1] = 1
            else:
                self.game.live_cells[(x1, y1)] = 1
                
            if x1 == x2 and y1 == y2:
                break
                
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy