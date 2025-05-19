import tkinter as tk
from tkinter import ttk

class GameGUI:
    def __init__(self, root, game, cell_size=20, speed=100):
        self.root = root
        self.game = game
        self.cell_size = cell_size
        self.speed = speed
        self.running = False
        self.after_id = None

        self.grid_width = game.width
        self.grid_height = game.height

        self._build_gui()

    def _build_gui(self):
        controls = ttk.Frame(self.root)
        controls.pack(side="top", fill="x")

        self.play_btn = ttk.Button(controls, text="Play", command=self.toggle_run)
        self.play_btn.pack(side="left", padx=5)

        ttk.Button(controls, text="Reset", command=self.reset).pack(side="left", padx=5)

        self.generation_label = ttk.Label(controls, text="Generation: 0")
        self.generation_label.pack(side="right", padx=10)

        canvas_width = self.grid_width * self.cell_size
        canvas_height = self.grid_height * self.cell_size
        self.canvas = tk.Canvas(self.root, width=canvas_width, height=canvas_height, bg="white")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.handle_click)

        self.draw_grid()

    def draw_grid(self):
        self.canvas.delete("all")
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                color = "black" if self.game.grid[y][x] else "white"
                x1 = x * self.cell_size
                y1 = y * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

    def handle_click(self, event):
        if self.running:
            return
        x = event.x // self.cell_size
        y = event.y // self.cell_size
        if 0 <= x < self.grid_width and 0 <= y < self.grid_height:
            self.game.toggle_cell(x, y)
            self.draw_grid()

    def toggle_run(self):
        self.running = not self.running
        self.play_btn.config(text="⏸ Pause" if self.running else "▶️ Play")
        if self.running:
            self.run_loop()
        else:
            if self.after_id:
                self.root.after_cancel(self.after_id)

    def run_loop(self):
        self.game.next_generation()
        self.draw_grid()
        self.update_generation_label()
        if self.running:
            self.after_id = self.root.after(self.speed, self.run_loop)

    def reset(self):
        self.running = False
        self.play_btn.config(text="▶️ Play")
        self.game.clear()  # Assumes core has a clear/reset method
        self.update_generation_label(reset=True)
        self.draw_grid()

    def update_generation_label(self, reset=False):
        generation = 0 if reset else getattr(self.game, "generation", "?")
        self.generation_label.config(text=f"Generation: {generation}")

# test
if __name__ == "__main__":
    from core.game_of_life import GameOfLife

    root = tk.Tk()
    game = GameOfLife(width=30, height=20)
    app = GameGUI(root, game)
    root.mainloop()
