from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtSvg import QSvgWidget


class HeaderBar(QWidget):
    """Header bar widget for displaying game_window information."""

    def __init__(self):
        super().__init__()
        self.build_ui()

    def build_ui(self):
        """Build and arrange header bar GUI elements."""
        layout = QHBoxLayout(self)

        self.icon_label = QSvgWidget("assets/game-of-life.svg")
        self.icon_label.setObjectName("IconLabel")
        self.icon_label.setFixedSize(100, 100)
        layout.addWidget(self.icon_label)

        self.title_label = QLabel("The Game of Life")
        self.title_label.setObjectName("TitleLabel")
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)

        layout.addStretch()

        # generation counter
        self.generation_label = QLabel("Generation: 0")
        self.generation_label.setObjectName("GenerationLabel")
        layout.addWidget(self.generation_label)

        self.exit_btn = QPushButton()
        self.exit_btn.setObjectName("ExitButton")
        self.exit_btn.setIcon(QIcon("assets/exit.svg"))
        layout.addWidget(self.exit_btn)

    def set_generation(self, gen_number):
        """Update the generation counter display."""
        self.generation_label.setText(f"Generation: {gen_number}")
