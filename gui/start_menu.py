from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt

from gui.game_gui import GameOfLifeGUI


class MainMenu(QWidget):
    """
    Main menu window for the Game of Life application.

    Provides navigation options to start the game, open settings, view game info, or exit.
    """
    def __init__(self):
        super().__init__()
        self.wrap_enabled = False
        self.custom_size = False
        self.speed = 5
        self.grid_width = 30
        self.grid_height = 20
        self.setWindowTitle("Menu")
        self.setMinimumSize(600, 400)
        self.build_ui()

    def build_ui(self):
        """Build and arrange UI elements in the main menu."""
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("Conway's Game of Life")
        title.setObjectName("MainTitle")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        start_btn = QPushButton("Start New Game")
        start_btn.clicked.connect(self.start_game)
        layout.addWidget(start_btn)

        settings_btn = QPushButton("Game Settings")
        settings_btn.clicked.connect(self.show_settings)
        layout.addWidget(settings_btn)

        info_btn = QPushButton("About Game of Life")
        info_btn.clicked.connect(self.show_info)
        layout.addWidget(info_btn)

        exit_btn = QPushButton("Exit")
        exit_btn.clicked.connect(self.close)
        layout.addWidget(exit_btn)

    def start_game(self):
        """Start the game with the selected settings."""
        self.hide()
        width = self.grid_width if self.custom_size else 50
        height = self.grid_height if self.custom_size else 50

        self.game_window = GameOfLifeGUI(
            width=width,
            height=height,
            wrap=self.wrap_enabled,
            menu_window=self,
            speed=self.speed,
            fixed_view=self.custom_size
        )

        with open("gui/styles/dark_theme.qss", "r") as f:
            self.game_window.setStyleSheet(f.read())
        self.game_window.show()

    def show_settings(self):
        """Display game settings dialog for grid and speed configuration."""
        from PyQt5.QtWidgets import QDialog, QFormLayout, QComboBox, QSpinBox, QDialogButtonBox

        dialog = QDialog(self)
        dialog.setWindowTitle("Game Settings")
        layout = QFormLayout(dialog)

        size_box = QComboBox()
        size_box.addItems(["Infinite", "Fixed size"])
        layout.addRow("Grid Size:", size_box)

        wrap_box = QComboBox()
        wrap_box.addItems(["Disabled", "Enabled"])
        layout.addRow("Grid Wrapping:", wrap_box)

        width_box = QSpinBox()
        width_box.setRange(10, 500)
        width_box.setValue(self.grid_width)
        layout.addRow("Grid Width:", width_box)

        height_box = QSpinBox()
        height_box.setRange(10, 500)
        height_box.setValue(self.grid_height)
        layout.addRow("Grid Height:", height_box)

        def toggle_size_inputs(index):
            """Enable or disable inputs based on grid size selection."""
            custom = size_box.currentText() == "Fixed size"
            width_box.setEnabled(custom)
            height_box.setEnabled(custom)
            wrap_box.setEnabled(custom)

        size_box.currentIndexChanged.connect(toggle_size_inputs)
        toggle_size_inputs(size_box.currentIndex())

        speed_box = QSpinBox()
        speed_box.setRange(1, 20)
        speed_box.setValue(self.speed)
        layout.addRow("Initial Speed (gen/sec):", speed_box)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout.addRow(buttons)

        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)

        if dialog.exec_() == QDialog.Accepted:
            self.wrap_enabled = wrap_box.currentText() == "Enabled"
            self.custom_size = size_box.currentText() == "Fixed size"
            self.grid_width = width_box.value()
            self.grid_height = height_box.value()
            self.speed = speed_box.value()

    def show_info(self):
        """Display information about Conway's Game of Life."""
        QMessageBox.information(
            self, "About Game of Life",
            "Conway's Game of Life is not your typical computer game. It is a cellular automaton where patterns evolve based on initial states.\n\n"
            "This game became widely known when it was mentioned in an article published by Scientific American in 1970. It consists of a grid of cells which, based on a few mathematical rules, can live, die or multiply. Depending on the initial conditions, the cells form various patterns throughout the course of the game.\n\n"
            "Rules:\n\n"
            "1. Each cell with one or no neighbors dies, as if by solitude.\n\n"
            "2. Each cell with four or more neighbors dies, as if by overpopulation.\n\n"
            "3. Each cell with two or three neighbors survives.\n\n"
            "4. Each cell with three neighbors becomes populated.\n\n"
        )
