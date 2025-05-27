import sys
from PyQt5.QtWidgets import QApplication
from gui.start_menu import MainMenu

if __name__ == "__main__":
    # QApplication expects a list of command-line arguments; pass an empty list
    app = QApplication([])

    with open("gui/styles/menu.qss", "r") as f:
        app.setStyleSheet(f.read())

    menu = MainMenu()
    menu.show()

    sys.exit(app.exec_())
