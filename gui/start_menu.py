from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt

from gui.game_gui import GameOfLifeGUI


class MainMenu(QWidget):
    """
    Main menu window for the Game of Life application.

    Provides options to start the game_window, open settings, view game_window info, or exit.
    Also handles game_window configuration including grid size, wrapping, speed, and custom rules.
    """
    def __init__(self):
        super().__init__()

        self.wrap_enabled = False
        self.custom_size = False
        self.custom_rules_enabled = False
        self.speed = 10

        self.grid_width = 20
        self.grid_height = 20

        self.overpopulation_limit = 3
        self.underpopulation_limit = 2
        self.reproduction_number = 3
        
        self.setWindowTitle("Menu")
        self.setMinimumSize(600, 400)
        self._build_ui()

    def _build_ui(self):
        """Build and arrange GUI elements in the main menu."""
        title = QLabel("Conway's Game of Life")
        title.setObjectName("MenuTitle")

        start_btn = QPushButton("Start New Game")
        settings_btn = QPushButton("Game Settings")
        info_btn = QPushButton("About Game of Life")
        exit_btn = QPushButton("Exit")

        start_btn.clicked.connect(self.start_game)
        settings_btn.clicked.connect(self.show_settings)
        info_btn.clicked.connect(self.show_info)
        exit_btn.clicked.connect(self.close)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        layout.addWidget(start_btn)
        layout.addWidget(settings_btn)
        layout.addWidget(info_btn)
        layout.addWidget(exit_btn)

    def start_game(self):
        """Start the game_window with the selected settings."""
        # QWidget has method hide() that hides current window
        self.hide()

        game_params = {
            'menu_window': self,
            'speed': self.speed,
            'fixed_view': self.custom_size
        }

        if self.custom_size:
            game_params.update({
                'width': self.grid_width,
                'height': self.grid_height,
                'wrap': self.wrap_enabled
            })

        self.game_window = GameOfLifeGUI(**game_params)

        if self.custom_rules_enabled:
            self.game_window.game.set_custom_rules(
                overpop=self.overpopulation_limit,
                underpop=self.underpopulation_limit,
                repro=self.reproduction_number
            )

        with open("gui/styles/dark_theme.qss", "r") as f:
            self.game_window.setStyleSheet(f.read())
        self.game_window.show()

    def show_settings(self):
        """
        Display game_window settings dialog for configuration.
        
        Allows users to configure:
        - Grid size (infinite/fixed)
        - Grid wrapping
        - Grid dimensions
        - Game speed
        - Custom game_window rules (survival and reproduction conditions)
        """
        from PyQt5.QtWidgets import (QDialog, QFormLayout, QComboBox, QSpinBox, QDialogButtonBox, QGroupBox,
                                     QVBoxLayout, QCheckBox)

        dialog = QDialog(self)
        dialog.setWindowTitle("Settings")

        main_layout = QVBoxLayout(dialog)

        grid_group = QGroupBox("Grid Settings")
        layout = QFormLayout(grid_group)

        size_box = QComboBox()
        size_box.addItems(["Infinite", "Fixed size"])
        size_box.setCurrentText("Fixed size" if self.custom_size else "Infinite")
        layout.addRow("Grid Size:", size_box)

        wrap_box = QComboBox()
        wrap_box.addItems(["Disabled", "Enabled"])
        wrap_box.setCurrentText("Enabled" if self.wrap_enabled else "Disabled")
        layout.addRow("Grid Wrapping:", wrap_box)

        width_box = QSpinBox()
        width_box.setRange(10, 500)
        width_box.setValue(self.grid_width)
        layout.addRow("Grid Width:", width_box)

        height_box = QSpinBox()
        height_box.setRange(10, 500)
        height_box.setValue(self.grid_height)
        layout.addRow("Grid Height:", height_box)

        speed_box = QSpinBox()
        speed_box.setRange(1, 20)
        speed_box.setValue(self.speed)
        layout.addRow("Initial Speed (gen/sec):", speed_box)

        main_layout.addWidget(grid_group)

        rules_group = QGroupBox("Game Rules")
        rules_layout = QFormLayout(rules_group)

        custom_rules_check = QCheckBox("Enable Custom Rules")
        custom_rules_check.setChecked(self.custom_rules_enabled)
        rules_layout.addRow(custom_rules_check)

        overpop_box = QSpinBox()
        overpop_box.setRange(1, 8)
        overpop_box.setValue(self.overpopulation_limit)
        rules_layout.addRow("Overpopulation Limit:", overpop_box)

        underpop_box = QSpinBox()
        underpop_box.setRange(0, 8)
        underpop_box.setValue(self.underpopulation_limit)
        rules_layout.addRow("Underpopulation Limit:", underpop_box)

        repro_box = QSpinBox()
        repro_box.setRange(1, 8)
        repro_box.setValue(self.reproduction_number)
        rules_layout.addRow("Reproduction Number:", repro_box)

        def toggle_rules_inputs(checked):
            """Enable or disable rule inputs based on checkbox state"""
            overpop_box.setEnabled(checked)
            underpop_box.setEnabled(checked)
            repro_box.setEnabled(checked)

        custom_rules_check.toggled.connect(toggle_rules_inputs)
        toggle_rules_inputs(custom_rules_check.isChecked())

        main_layout.addWidget(rules_group)

        def toggle_size_inputs(index):
            """Enable or disable grid size inputs based on selection"""
            custom = size_box.currentText() == "Fixed size"
            width_box.setEnabled(custom)
            height_box.setEnabled(custom)
            wrap_box.setEnabled(custom)

        size_box.currentIndexChanged.connect(toggle_size_inputs)
        toggle_size_inputs(size_box.currentIndex())

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)

        main_layout.addWidget(buttons)

        if dialog.exec_() == QDialog.Accepted:
            self.wrap_enabled = wrap_box.currentText() == "Enabled"
            self.custom_size = size_box.currentText() == "Fixed size"
            self.grid_width = width_box.value()
            self.grid_height = height_box.value()
            self.speed = speed_box.value()
            self.custom_rules_enabled = custom_rules_check.isChecked()
            self.overpopulation_limit = overpop_box.value()
            self.underpopulation_limit = underpop_box.value()
            self.reproduction_number = repro_box.value()

    def show_info(self):
        """Display information about Conway's Game of Life."""
        QMessageBox.information(
            self, "About Game of Life",
            "Conway's Game of Life is not your typical computer game_window. It is a cellular automaton where patterns evolve based on initial states.\n\n"
            "This game_window became widely known when it was mentioned in an article published by Scientific American in 1970. It consists of a grid of cells which, based on a few mathematical rules, can live, die or multiply. Depending on the initial conditions, the cells form various patterns throughout the course of the game_window.\n\n"
            "Standard Rules:\n\n"
            "1. Each cell with one or no neighbors dies, as if by solitude.\n\n"
            "2. Each cell with four or more neighbors dies, as if by overpopulation.\n\n"
            "3. Each cell with two or three neighbors survives.\n\n"
            "4. Each cell with three neighbors becomes populated.\n\n"
            "You can also choose your custom set of rules in the \"settings\" section.\n\n"
        )
