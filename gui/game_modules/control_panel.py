from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QVBoxLayout, QSlider, QLabel


class ControlPanel(QWidget):
    """Control panel with simulation controls and speed slider."""
    def __init__(self, start_callback, next_callback, clear_callback, theme_callback, speed_change_callback, initial_speed=5):
        super().__init__()

        controls = QHBoxLayout()
        controls.setSpacing(20)

        # theme button
        self.theme_btn = QPushButton()
        self.theme_btn.clicked.connect(theme_callback)
        controls.addWidget(self.theme_btn)
        controls.addStretch()

        # clear button
        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(clear_callback)
        controls.addWidget(clear_btn)

        # start button
        self.start_btn = QPushButton("Start")
        self.start_btn.clicked.connect(start_callback)
        controls.addWidget(self.start_btn)

        # next button
        next_btn = QPushButton("Next")
        next_btn.clicked.connect(next_callback)
        controls.addWidget(next_btn)
        controls.addStretch()

        # speed slider
        self.speed_layout = QVBoxLayout()
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setFixedSize(QSize(200, 10))
        self.speed_slider.setRange(1, 20)
        self.speed_slider.setValue(initial_speed)
        self.speed_slider.setTickInterval(1)
        self.speed_slider.setTickPosition(QSlider.TicksBelow)
        self.speed_slider.valueChanged.connect(speed_change_callback)
        self.speed_label = QLabel(f"Speed: {initial_speed}x")
        self.speed_label.setAlignment(Qt.AlignCenter)
        self.speed_layout.addWidget(self.speed_label)
        self.speed_layout.addWidget(self.speed_slider)
        self.speed_value_label = QLabel(f"{initial_speed}x")
        self.speed_slider.valueChanged.connect(
            lambda: self.speed_label.setText(f"Speed: {self.speed_slider.value()}x")
        )

        controls.addLayout(self.speed_layout)

        self.setLayout(controls)

