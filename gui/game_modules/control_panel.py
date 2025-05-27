from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QVBoxLayout, QSlider, QLabel


class ControlPanel(QWidget):
    """
    Control panel for game controls:
    - Start/Pause button
    - Next generation button
    - Clear grid button
    - Theme toggle button
    - Speed control slider with labels
    """
    def __init__(self, start_callback, next_callback, clear_callback, theme_callback, speed_change_callback, initial_speed=5):
        """
        Initialize the control panel.
        
        Args:
            start_callback: Function to call when start/pause button is clicked
            next_callback: Function to call when next generation button is clicked
            clear_callback: Function to call when clear button is clicked
            theme_callback: Function to call when theme button is clicked
            speed_change_callback: Function to call when speed slider value changes
            initial_speed: Initial simulation speed (generations per second)
        """
        super().__init__()
        self.start_callback = start_callback
        self.next_callback = next_callback
        self.clear_callback = clear_callback
        self.theme_callback = theme_callback
        self.speed_change_callback = speed_change_callback
        self.initial_speed = initial_speed
        self.build_ui()

    def build_ui(self):
        """Build and arrange control panel UI elements with proper spacing and layout."""
        controls = QHBoxLayout()
        controls.setSpacing(20)

        # Theme button on the left
        self.theme_btn = QPushButton("Light Mode")
        self.theme_btn.clicked.connect(self.theme_callback)
        controls.addWidget(self.theme_btn)
        controls.addStretch()

        # Clear button
        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(self.clear_callback)
        controls.addWidget(clear_btn)

        # Start button
        self.start_btn = QPushButton("Start")
        self.start_btn.clicked.connect(self.start_callback)
        controls.addWidget(self.start_btn)

        # Next button
        next_btn = QPushButton("Next")
        next_btn.clicked.connect(self.next_callback)
        controls.addWidget(next_btn)
        controls.addStretch()

        # Speed control with labels
        self.speed_layout = QVBoxLayout()
        
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setFixedSize(QSize(200, 10))
        self.speed_slider.setRange(1, 20)
        self.speed_slider.setValue(self.initial_speed)
        self.speed_slider.setTickInterval(1)
        self.speed_slider.setTickPosition(QSlider.TicksBelow)
        self.speed_slider.valueChanged.connect(self.speed_change_callback)
        
        self.speed_label = QLabel(f"Speed: {self.initial_speed}x")
        self.speed_label.setAlignment(Qt.AlignCenter)
        
        self.speed_layout.addWidget(self.speed_label)
        self.speed_layout.addWidget(self.speed_slider)
        
        # Update speed label when slider value changes
        self.speed_slider.valueChanged.connect(
            lambda: self.speed_label.setText(f"Speed: {self.speed_slider.value()}x")
        )

        controls.addLayout(self.speed_layout)

        self.setLayout(controls)

