"""
Game of Life GUI using PyQt5

A zoomable, pannable, interactive GUI for Conway's Game of Life.
Integrates both fixed and infinite grid implementations.

Author: Darya Sharnevich
Version: 1.1
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QMessageBox)
from PyQt5.QtCore import QTimer, QPoint
from PyQt5.QtGui import QColor

from core.game_of_life import GameOfLife
from core.infinite_game import InfiniteGameOfLife
from gui.game_modules.header_bar import HeaderBar
from gui.game_modules.control_panel import ControlPanel
from gui.game_modules.grid_canvas import GridCanvas


class GameOfLifeGUI(QWidget):
    """
    GUI for the Game of Life.

    Args:
        menu_window (QWidget): Reference to menu window (optional).
        speed (int): Initial simulation speed (generations / second).
        fixed_view (bool): If True, grid has fixed width and height, panning/zoom is disabled.
        width (int, optional): Width of the grid in cells (required for fixed grid mode).
        height (int, optional): Height of the grid in cells (required for fixed grid mode).
        wrap (bool, optional): Enable grid wrapping (only for fixed grid mode).
    """
    def __init__(self, menu_window=None, speed=10, fixed_view=False, width=None, height=None, wrap=False):
        super().__init__()
        self.fixed_view = fixed_view
        self.menu_window = menu_window
        self.speed = speed
        
        if fixed_view:
            self.width = width
            self.height = height
            self.wrap = wrap
            self.game = GameOfLife(width, height, wrap)
        else:
            self.game = InfiniteGameOfLife()

        self.setWindowTitle("The Game of Life")
        self.setMinimumSize(800, 800)

        self.base_cell_size = 20
        self.zoom = 1.0
        self.offset = QPoint(0, 0)
        self.last_mouse_pos = None

        self.timer = QTimer()
        self.timer.timeout.connect(self.next_generation)

        self.current_theme = "dark"
        self.bg_color = QColor("#2d3133")
        self.grid_line_color = QColor("#3c3c3c")
        self.dead_color = QColor("#2c2c2c")
        self.live_color = QColor("#458557")

        self.build_gui()

    def build_gui(self):
        """Build header, canvas, and controls layout."""
        layout = QVBoxLayout(self)

        self.header = HeaderBar()
        self.header.exit_btn.clicked.connect(self.confirm_exit_to_menu)
        
        self.canvas = GridCanvas(
            game=self.game,
            fixed_view_callable=lambda: self.fixed_view,
            zoom=self.zoom,
            offset=self.offset,
            colors={
                'bg': self.bg_color,
                'grid': self.grid_line_color,
                'dead': self.dead_color,
                'live': self.live_color
            }
        )
        
        self.controls = ControlPanel(
            start_callback=self.toggle_timer,
            next_callback=self.next_generation,
            clear_callback=self.clear_grid,
            theme_callback=self.toggle_theme,
            speed_change_callback=self.change_speed,
            initial_speed=self.speed
        )
        self.controls.theme_btn.setText("Light Mode")

        layout.addWidget(self.header)
        layout.addWidget(self.canvas)
        layout.addWidget(self.controls)

    def toggle_timer(self):
        """Start or pause simulation timer."""
        if self.timer.isActive():
            self.timer.stop()
            self.controls.start_btn.setText("Start")
        else:
            self._start_timer_with_current_speed()
            self.controls.start_btn.setText("Pause")

    def change_speed(self):
        """Adjust simulation speed from slider."""
        if self.timer.isActive():
            self._start_timer_with_current_speed()

    def _start_timer_with_current_speed(self):
        """Start timer with current speed setting."""
        # generations per second
        delay = int(1000 / self.controls.speed_slider.value())
        self.timer.start(delay)

    def clear_grid(self):
        """Clear grid and reset generation count."""
        self.game.clear()
        self.header.set_generation(self.game.generation)
        self.canvas.update()

    def next_generation(self):
        """Update the game_window state by one generation."""
        self.game.next_generation()
        self.header.set_generation(self.game.generation)
        self.canvas.update()

    def confirm_exit_to_menu(self):
        """Shows confirmation dialog to return to the game_window menu."""
        msg = QMessageBox(self)
        msg.setStyleSheet("QLabel{font-size: 20px;} QPushButton{font-size: 16px;}")
        msg.setWindowTitle("Confirm Exit")
        msg.setText("Are you sure you want to end the game_window?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        if msg.exec_() == QMessageBox.Yes:
            self.close()
            if self.menu_window:
                self.menu_window.show()

    def toggle_theme(self):
        """Switch between light and dark GUI themes."""
        if self.current_theme == "dark":
            self.current_theme = "light"
            self.apply_light_theme()
        else:
            self.current_theme = "dark"
            self.apply_dark_theme()
        self.canvas.update()

    def apply_dark_theme(self):
        """Apply dark theme colors and QSS."""
        with open("gui/styles/dark_theme.qss", "r") as f:
            self.setStyleSheet(f.read())
        self.controls.theme_btn.setText("Light Mode")
        self.bg_color = QColor("#2d3133")
        self.grid_line_color = QColor("#3c3c3c")
        self.dead_color = QColor("#2c2c2c")
        self.live_color = QColor("#458557")
        self.canvas.colors = {
            'bg': self.bg_color,
            'grid': self.grid_line_color,
            'dead': self.dead_color,
            'live': self.live_color
        }

    def apply_light_theme(self):
        """Apply light theme colors and QSS."""
        with open("gui/styles/light_theme.qss", "r") as f:
            self.setStyleSheet(f.read())
        self.controls.theme_btn.setText("Dark Mode")
        self.bg_color = QColor("#d8e4f0")
        self.grid_line_color = QColor("#a7adb5")
        self.dead_color = QColor("#bec7d1")
        self.live_color = QColor("#224061")
        self.canvas.colors = {
            'bg': self.bg_color,
            'grid': self.grid_line_color,
            'dead': self.dead_color,
            'live': self.live_color
        }