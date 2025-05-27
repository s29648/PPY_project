from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton


class HeaderBar(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout()

        # icon
        self.icon_label = QSvgWidget("assets/game-of-life.svg")
        self.icon_label.setObjectName("IconLabel")
        self.icon_label.setFixedSize(100, 100)
        layout.addWidget(self.icon_label)

        # Title text
        self.title_label = QLabel("The Game of Life")
        self.title_label.setObjectName("TitleLabel")
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)

        layout.addStretch()

        # generation counter
        self.generation_label = QLabel("Generation: 0")
        layout.addWidget(self.generation_label)

        # exit button
        self.exit_btn = QPushButton()
        self.exit_btn.setObjectName("ExitButton")
        self.exit_btn.setIcon(QIcon("assets/exit.svg"))
        layout.addWidget(self.exit_btn)

        self.setLayout(layout)


    def set_generation(self, generation):
        """Update the generation label text."""
        self.generation_label.setText(f"Generation: {generation}")
