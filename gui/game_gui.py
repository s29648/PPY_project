"""
Game of Life GUI using PyQt5

A zoomable, pannable, interactive GUI for Conway's Game of Life.
Integrates a core GameOfLife logic class and provides real-time visualization.

Author: Darya Sharnevich
Version: 1.0
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QMessageBox)
from PyQt5.QtCore import QTimer, QPoint
from PyQt5.QtGui import QColor

from core.game_of_life import GameOfLife
from gui.game_modules.header_bar import HeaderBar
from gui.game_modules.control_panel import ControlPanel
from gui.game_modules.grid_canvas import GridCanvas


class GameOfLifeGUI(QWidget):
    """
    A PyQt5-based GUI for the Game of Life.

    Args:
        width (int): Width of the grid in cells.
        height (int): Height of the grid in cells.
        wrap (bool): Enable grid wrapping.
        menu_window (QWidget): Reference to menu window (optional).
        speed (int): Initial simulation speed (generations / second).
        fixed_view (bool):
            If False (default), grid is infinite and panning is enabled.
            If True, grid has fixed width and height, panning/zoom is disabled.
    """
    def __init__(self, width=50, height=50, wrap=False, menu_window=None, speed=10, fixed_view=False):
        super().__init__()
        # TODO: width height - separate logic and separate for infinite grid
        self.width = width
        self.height = height
        self.wrap = wrap
        self.speed = speed
        self.fixed_view = fixed_view
        self.menu_window = menu_window

        self.current_theme = "dark"

        self.setWindowTitle("The Game of Life")
        self.setMinimumSize(800, 800)

        # for fixed grid
        self.game = GameOfLife(width, height, wrap)
        self.base_cell_size = 20
        self.zoom = 1.0
        self.offset = QPoint(0, 0)
        self.last_mouse_pos = None

        # QTimer fires an event after a specified interval and calls next_generation()
        self.timer = QTimer()
        self.timer.timeout.connect(self.next_generation)

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
        #  redefines generation / sec value (1sec = 1000ms)
        delay = int(1000 / self.controls.speed_slider.value())
        self.timer.start(delay)


    def clear_grid(self):
        """Clear grid and reset generation count."""
        self.game.clear()
        self.header.set_generation(self.game.generation)
        self.canvas.update()


    def next_generation(self):
        """
        Update the game state by one generation.
        Uses custom rules if they are set, otherwise uses standard Game of Life rules.
        """
        if hasattr(self.game, 'custom_overpopulation_limit'):
            # If custom rules are set
            self.game.next_generation_custom()
        else:
            # Use standard rules
            self.game.next_generation()
        self.header.generation_label.setText(f"Generation: {self.game.generation}")
        self.canvas.update()


    def confirm_exit_to_menu(self):
        """Shows confirmation dialog to return to the game menu."""
        msg = QMessageBox(self)
        msg.setStyleSheet("QLabel{font-size: 20px;} QPushButton{font-size: 16px;}")
        msg.setWindowTitle("Confirm Exit")
        msg.setText("Are you sure you want to end the game?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        reply = msg.exec_()

        if reply == QMessageBox.Yes:
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
        self.bg_color, self.grid_line_color = QColor("#2d3133"), QColor("#3c3c3c")
        self.dead_color, self.live_color = QColor("#2c2c2c"), QColor("#458557")
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
        self.bg_color, self.grid_line_color = QColor("#d8e4f0"), QColor("#a7adb5")
        self.dead_color, self.live_color = QColor("#bec7d1"), QColor("#224061")
        self.canvas.colors = {
            'bg': self.bg_color,
            'grid': self.grid_line_color,
            'dead': self.dead_color,
            'live': self.live_color
        }