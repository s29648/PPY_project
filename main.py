import sys
from PyQt5.QtWidgets import QApplication
from gui.start_menu import MainMenu

if __name__ == "__main__":
    app = QApplication(sys.argv)

    with open("gui/styles/menu.qss", "r") as f:
        app.setStyleSheet(f.read())

    window = MainMenu()
    window.show()

    sys.exit(app.exec_())
