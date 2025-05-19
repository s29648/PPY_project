from tkinter import Tk
from gui.gui import GameGUI
from core.game_of_life import GameOfLife

root = Tk()
game = GameOfLife(width=30, height=20)  # adjust size as needed
app = GameGUI(root, game)
root.mainloop()