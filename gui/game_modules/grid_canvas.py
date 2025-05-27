from PyQt5.QtWidgets import QWidget, QSizePolicy
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QMouseEvent, QWheelEvent, QColor

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
    def __init__(self, game, fixed_view_callable, zoom, offset, colors, parent=None):
        """
        Initialize the grid canvas.

        Args:
            game: GameOfLife instance to visualize
            fixed_view_callable: Function that returns whether the view is fixed
            zoom: Initial zoom level
            offset: Initial view offset
            colors: Dictionary with color scheme (bg, grid, dead, live)
            parent: Parent widget
        """
        super().__init__(parent)
        self.game = game
        self.fixed_view_callable = fixed_view_callable
        self.zoom = zoom
        self.offset = offset
        self.colors = colors
        self.base_cell_size = 20
        self.last_mouse_pos = None

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def paintEvent(self, event):
        """Paint the grid and live cells based on current state."""
        qp = QPainter(self)
        qp.fillRect(self.rect(), self.colors['bg'])

        width, height = self.width(), self.height()

        if self.fixed_view_callable():
            cell_px = min(width // self.game.width, height // self.game.height)
            cols, rows = self.game.width, self.game.height

            x_offset = (width - cols * cell_px) // 2
            y_offset = (height - rows * cell_px) // 2

            for gx in range(cols):
                for gy in range(rows):
                    sx = x_offset + gx * cell_px
                    sy = y_offset + gy * cell_px

                    qp.setPen(self.colors['grid'])
                    qp.setBrush(self.colors['dead'])
                    qp.drawRect(sx, sy, cell_px, cell_px)

                    if self.game.grid[gy][gx]:
                        qp.setBrush(self.colors['live'])
                        qp.setPen(Qt.NoPen)
                        qp.drawRect(sx + 1, sy + 1, cell_px - 2, cell_px - 2)
        else:
            cell_px = max(5, int(self.base_cell_size * self.zoom))
            start_x = self.offset.x() // cell_px
            start_y = self.offset.y() // cell_px
            cols = width // cell_px + 2
            rows = height // cell_px + 2

            for i in range(cols):
                for j in range(rows):
                    gx = start_x + i
                    gy = start_y + j
                    sx = i * cell_px - (self.offset.x() % cell_px)
                    sy = j * cell_px - (self.offset.y() % cell_px)

                    qp.setPen(self.colors['grid'])
                    qp.setBrush(self.colors['dead'])
                    qp.drawRect(sx, sy, cell_px, cell_px)

                    if 0 <= gx < self.game.width and 0 <= gy < self.game.height:
                        if self.game.grid[gy][gx]:
                            qp.setBrush(self.colors['live'])
                            qp.setPen(Qt.NoPen)
                            qp.drawRect(sx + 1, sy + 1, cell_px - 2, cell_px - 2)

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
        Maintains the point under cursor during zoom.
        """
        delta = event.angleDelta().y()
        if delta == 0:
            return

        zoom_factor = 1.0 + (delta / 120)
        new_zoom = min(max(0.2, self.zoom * zoom_factor), 5.0)
        mouse_x, mouse_y = event.pos().x(), event.pos().y()
        pre_zoom_x = (self.offset.x() + mouse_x) / self.zoom
        pre_zoom_y = (self.offset.y() + mouse_y) / self.zoom

        self.zoom = new_zoom
        self.offset.setX(int(pre_zoom_x * self.zoom - mouse_x))
        self.offset.setY(int(pre_zoom_y * self.zoom - mouse_y))

        self.update()

    def _get_cell_coords(self, pos):
        """Convert screen coordinates to cell grid coordinates."""
        width, height = self.width(), self.height()

        if self.fixed_view_callable():
            cell_px = min(width // self.game.width, height // self.game.height)
            x_offset = (width - self.game.width * cell_px) // 2
            y_offset = (height - self.game.height * cell_px) // 2

            x = (pos.x() - x_offset) // cell_px
            y = (pos.y() - y_offset) // cell_px

            if not (0 <= x < self.game.width and 0 <= y < self.game.height):
                return None
        else:
            cell_px = max(5, int(self.base_cell_size * self.zoom))
            x = (pos.x() + self.offset.x()) // cell_px
            y = (pos.y() + self.offset.y()) // cell_px

        return int(x), int(y)

    def _draw_line_between_points(self, x1, y1, x2, y2):
        """Draw a continuous line of live cells between two points using Bresenham's algorithm."""
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        while True:
            if 0 <= x1 < self.game.width and 0 <= y1 < self.game.height:
                self.game.grid[y1][x1] = 1
            if x1 == x2 and y1 == y2:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy