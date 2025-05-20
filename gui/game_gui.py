"""
Game of Life GUI using PyQt5

This module provides a zoomable, pannable, interactive GUI for Conway's Game of Life,
based on a GameOfLife class with methods like `toggle_cell(x, y)`, `next_generation()`, and `clear()`.

Author: Darya Sharnevich
Version: 1.0
"""
import sys
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QSlider, QSizePolicy, QMessageBox
)
from PyQt5.QtCore import Qt, QTimer, QPoint, QSize
from PyQt5.QtGui import QColor, QPainter, QMouseEvent, QWheelEvent, QIcon
from core.game_of_life import GameOfLife


class GameOfLifeGUI(QWidget):
    """
    A PyQt5 widget for displaying and interacting with the Game of Life.

    Args:
        width (int): Width of the grid in cells.
        height (int): Height of the grid in cells.
        wrap (bool): Enable grid wrapping behavior.
        menu_window (QWidget): Optional reference to main menu window.
        speed (int): Initial simulation speed (generations per second).
        fixed_view (bool): Whether to disable zoom/pan and scale grid to fit.
    """
    def __init__(self, width=50, height=50, wrap=False, menu_window=None, speed=10, fixed_view=False):
        super().__init__()
        self.width = width
        self.height = height
        self.wrap = wrap
        self.speed = speed
        self.fixed_view = fixed_view
        self.menu_window = menu_window
        self.current_theme = "dark"

        self.setWindowTitle("The Game of Life")
        self.setMinimumSize(800, 800)

        self.game = GameOfLife(width, height, wrap)
        self.base_cell_size = 20
        self.zoom = 1.0
        self.offset = QPoint(0, 0)
        self.last_mouse_pos = None

        self.timer = QTimer()
        self.timer.timeout.connect(self._next_generation)

        self._build_ui()

    def _build_ui(self):
        """Initialize and arrange UI elements: header, canvas, controls."""
        layout = QVBoxLayout(self)

        header = QHBoxLayout()
        self.icon_label = QSvgWidget("assets/game-of-life.svg")
        self.icon_label.setObjectName("IconLabel")
        self.icon_label.setFixedSize(100, 100)
        header.addWidget(self.icon_label)

        self.title_label = QLabel("The Game of Life")
        self.title_label.setObjectName("TitleLabel")
        self.title_label.setAlignment(Qt.AlignCenter)
        header.addWidget(self.title_label)

        header.addStretch()

        self.generation_label = QLabel("Generation: 0")
        header.addWidget(self.generation_label)

        exit_btn = QPushButton()
        exit_btn.setObjectName("ExitButton")
        exit_btn.setIcon(QIcon("assets/exit.svg"))
        exit_btn.clicked.connect(self._confirm_exit_to_menu)
        header.addWidget(exit_btn)

        layout.addLayout(header)

        self.canvas = QWidget()
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.canvas.paintEvent = self._paint_grid
        self.canvas.mousePressEvent = self._mouse_press
        self.canvas.mouseMoveEvent = self._mouse_drag
        self.canvas.mouseReleaseEvent = self._mouse_release
        self.canvas.wheelEvent = self._mouse_wheel
        layout.addWidget(self.canvas)

        controls = QHBoxLayout()
        controls.setSpacing(20)

        self.theme_btn = QPushButton("Switch Theme")
        self.theme_btn.clicked.connect(self._toggle_theme)
        controls.addWidget(self.theme_btn)
        controls.addStretch()

        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(self._clear_grid)
        controls.addWidget(clear_btn)

        self.start_btn = QPushButton("Start")
        self.start_btn.clicked.connect(self._toggle_timer)
        controls.addWidget(self.start_btn)

        next_btn = QPushButton("Next")
        next_btn.clicked.connect(self._next_generation)
        controls.addWidget(next_btn)
        controls.addStretch()

        self.speed_layout = QVBoxLayout()

        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setFixedSize(QSize(200, 10))
        self.speed_slider.setRange(1, 20)
        self.speed_slider.setValue(self.speed)
        self.speed_slider.setTickInterval(1)
        self.speed_slider.setTickPosition(QSlider.TicksBelow)
        self.speed_slider.valueChanged.connect(self._change_speed)

        self.speed_label = QLabel(f"Speed: {self.speed}x")
        self.speed_label.setAlignment(Qt.AlignCenter)
        self.speed_layout.addWidget(self.speed_label)
        self.speed_layout.addWidget(self.speed_slider)

        self.speed_value_label = QLabel(f"{self.speed}x")
        self.speed_slider.valueChanged.connect(
            lambda: self.speed_label.setText(f"Speed: {self.speed_slider.value()}x")
        )

        controls.addLayout(self.speed_layout)
        layout.addLayout(controls)

    def _paint_grid(self, event):
        """Paint the grid and live cells based on current state."""
        qp = QPainter(self.canvas)
        if not hasattr(self, 'bg_color'):
            self._apply_dark_theme()

        qp.fillRect(self.canvas.rect(), self.bg_color)

        width, height = self.canvas.width(), self.canvas.height()

        if self.fixed_view:
            cell_px = min(width // self.width, height // self.height)
            start_x, start_y = 0, 0
            cols, rows = self.width, self.height
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

                qp.setPen(self.grid_line_color)
                qp.setBrush(self.dead_color)
                qp.drawRect(sx, sy, cell_px, cell_px)

                if 0 <= gx < self.game.width and 0 <= gy < self.game.height:
                    if self.game.grid[gy][gx]:
                        qp.setBrush(self.live_color)
                        qp.setPen(Qt.NoPen)
                        qp.drawRect(sx + 1, sy + 1, cell_px - 2, cell_px - 2)

    def _get_cell_coords(self, pos):
        """Convert screen coordinates to cell grid coordinates."""
        width, height = self.canvas.width(), self.canvas.height()
        if self.fixed_view:
            cell_px = min(width // self.width, height // self.height)
            x = pos.x() // cell_px
            y = pos.y() // cell_px
        else:
            cell_px = max(5, int(self.base_cell_size * self.zoom))
            x = (pos.x() + self.offset.x()) // cell_px
            y = (pos.y() + self.offset.y()) // cell_px
        return int(x), int(y)

    def _mouse_press(self, event: QMouseEvent):
        """Handle cell toggling and drag start."""
        if event.button() == Qt.LeftButton:
            x, y = self._get_cell_coords(event.pos())
            if 0 <= x < self.game.width and 0 <= y < self.game.height:
                self.game.toggle_cell(x, y)
                self.canvas.update()
        elif event.button() == Qt.RightButton:
            self.last_mouse_pos = event.pos()

    def _mouse_drag(self, event: QMouseEvent):
        """Handle panning of the view during dragging."""
        if self.fixed_view:
            return

        if event.buttons() & Qt.RightButton and self.last_mouse_pos:
            delta = event.pos() - self.last_mouse_pos
            self.offset -= delta
            self.last_mouse_pos = event.pos()
            self.canvas.update()
        elif event.buttons() & Qt.LeftButton:
            x, y = self._get_cell_coords(event.pos())
            if 0 <= x < self.game.width and 0 <= y < self.game.height:
                self.game.toggle_cell(x, y)
                self.canvas.update()

    def _mouse_release(self, event: QMouseEvent):
        """Reset drag state on release."""
        self.last_mouse_pos = None

    def _mouse_wheel(self, event: QWheelEvent):
        """Zoom in or out using mouse wheel."""
        if self.fixed_view:
            return

        old_zoom = self.zoom
        factor = 1.1 if event.angleDelta().y() > 0 else 0.9
        new_zoom = max(0.2, min(5.0, self.zoom * factor))

        if new_zoom != old_zoom:
            mouse_x, mouse_y = event.pos().x(), event.pos().y()
            pre_zoom_x = (self.offset.x() + mouse_x) / old_zoom
            pre_zoom_y = (self.offset.y() + mouse_y) / old_zoom
            self.zoom = new_zoom
            self.offset.setX(int(pre_zoom_x * self.zoom - mouse_x))
            self.offset.setY(int(pre_zoom_y * self.zoom - mouse_y))
            self.canvas.update()

    def _toggle_timer(self):
        """Start or pause simulation timer."""
        if self.timer.isActive():
            self.timer.stop()
            self.start_btn.setText("Start")
        else:
            delay = int(1000 / self.speed_slider.value())
            self.timer.start(delay)
            self.start_btn.setText("Pause")

    def _change_speed(self):
        """Adjust simulation speed from slider."""
        if self.timer.isActive():
            delay = int(1000 / self.speed_slider.value())
            self.timer.start(delay)

    def _clear_grid(self):
        """Clear grid and reset generation count."""
        self.game.clear()
        self.generation_label.setText(f"Generation: {self.game.generation}")
        self.canvas.update()

    def _next_generation(self):
        """Advance the game state by one generation."""
        self.game.next_generation()
        self.generation_label.setText(f"Generation: {self.game.generation}")
        self.canvas.update()

    def _confirm_exit_to_menu(self):
        """Show confirmation dialog to return to main menu."""
        reply = QMessageBox.question(
            self,
            "Confirm Exit",
            "Are you sure you want to return to the main menu?\n\nYour current progress will be lost.",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.close()
            if self.menu_window:
                self.menu_window.show()

    def _toggle_theme(self):
        """Switch between light and dark UI themes."""
        if self.current_theme == "dark":
            self.current_theme = "light"
            self._apply_light_theme()
        else:
            self.current_theme = "dark"
            self._apply_dark_theme()
        self.canvas.update()

    def _apply_dark_theme(self):
        """Apply dark theme colors and QSS."""
        self.bg_color = QColor("#1e1e1e")
        self.grid_line_color = QColor("#3c3c3c")
        self.dead_color = QColor("#2c2c2c")
        self.live_color = QColor("#458557")
        with open("gui/styles/dark_theme.qss", "r") as f:
            self.setStyleSheet(f.read())

    def _apply_light_theme(self):
        """Apply light theme colors and QSS."""
        self.bg_color = QColor("#bec7d1")
        self.grid_line_color = QColor("#a7adb5")
        self.dead_color = QColor("#bec7d1")
        self.live_color = QColor("#224061")
        with open("gui/styles/light_theme.qss", "r") as f:
            self.setStyleSheet(f.read())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameOfLifeGUI()
    window.show()

    with open("gui/styles/main.qss", "r") as f:
        app.setStyleSheet(f.read())

    sys.exit(app.exec_())
