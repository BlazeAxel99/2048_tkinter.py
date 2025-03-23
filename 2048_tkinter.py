import tkinter as tk
from tkinter import messagebox
import random

# Constants
BOARD_SIZE = 4
TILE_SIZE = 100
TILE_COLORS = {
    0: "#cdc1b4",
    2: "#eee4da",
    4: "#ede0c8",
    8: "#f2b179",
    16: "#f59563",
    32: "#f67c5f",
    64: "#f65e3b",
    128: "#edcf72",
    256: "#edcc61",
    512: "#edc850",
    1024: "#edc53f",
    2048: "#edc22e"
}

class Game2048:
    def __init__(self, root):
        self.root = root
        self.root.title("2048")
        self.score = 0
        self.board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.tiles = []
        self.init_ui()
        self.start_game()

    def init_ui(self):
        self.score_label = tk.Label(self.root, text="Score: 0", font=("Arial", 16))
        self.score_label.grid(row=0, column=0, columnspan=BOARD_SIZE)

        self.frame = tk.Frame(self.root, bg="#bbada0")
        self.frame.grid(row=1, column=0, columnspan=BOARD_SIZE)

        for i in range(BOARD_SIZE):
            row = []
            for j in range(BOARD_SIZE):
                tile = tk.Label(self.frame, text="", font=("Arial", 24, "bold"),
                                width=4, height=2, bg=TILE_COLORS[0])
                tile.grid(row=i, column=j, padx=5, pady=5)
                row.append(tile)
            self.tiles.append(row)

        # Bind arrow keys to move functions
        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)
        self.root.bind("<Up>", self.move_up)
        self.root.bind("<Down>", self.move_down)

        # Ensure the frame has focus to receive key events
        self.frame.focus_set()

    def start_game(self):
        self.add_tile()
        self.add_tile()

    def add_tile(self):
        empty_cells = [(i, j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE) if self.board[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.board[i][j] = random.choice([2, 2, 2, 4])
            self.update_ui()

    def update_ui(self):
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                value = self.board[i][j]
                self.tiles[i][j].config(text=str(value) if value != 0 else "",
                                       bg=TILE_COLORS.get(value, "#cdc1b4"),
                                       fg="#776e65" if value in [2, 4] else "#ffffff")
        self.score_label.config(text=f"Score: {self.score}")

    def move_left(self, event=None):
        if self.move(self.board):
            self.add_tile()
            self.check_game_over()

    def move_right(self, event=None):
        new_board = [row[::-1] for row in self.board]
        if self.move(new_board):
            self.board = [row[::-1] for row in new_board]
            self.add_tile()
            self.check_game_over()

    def move_up(self, event=None):
        new_board = [list(row) for row in zip(*self.board)]
        if self.move(new_board):
            self.board = [list(row) for row in zip(*new_board)]
            self.add_tile()
            self.check_game_over()

    def move_down(self, event=None):
        new_board = [list(row) for row in zip(*self.board)][::-1]
        if self.move(new_board):
            self.board = [list(row) for row in zip(*new_board[::-1])]
            self.add_tile()
            self.check_game_over()

    def move(self, board):
        moved = False
        for row in board:
            new_row = self.merge(row)
            if new_row != row:
                moved = True
            row[:] = new_row
        return moved

    def merge(self, row):
        new_row = [tile for tile in row if tile != 0]
        merged_row = []
        i = 0
        while i < len(new_row):
            if i + 1 < len(new_row) and new_row[i] == new_row[i + 1]:
                merged_row.append(new_row[i] * 2)
                self.score += new_row[i] * 2
                i += 2
            else:
                merged_row.append(new_row[i])
                i += 1
        return merged_row + [0] * (BOARD_SIZE - len(merged_row))

    def check_game_over(self):
        if not any(0 in row for row in self.board) and not self.can_merge():
            messagebox.showinfo("Game Over", f"Final Score: {self.score}")
            self.root.quit()

    def can_merge(self):
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if i < BOARD_SIZE - 1 and self.board[i][j] == self.board[i + 1][j]:
                    return True
                if j < BOARD_SIZE - 1 and self.board[i][j] == self.board[i][j + 1]:
                    return True
        return False

if __name__ == "__main__":
    root = tk.Tk()
    game = Game2048(root)
    root.mainloop()