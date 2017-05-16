import tkinter as tk
from Jeu.logique import *

SIZE = 500
GRID_LEN = 4
GRID_PADDING = 10

BACKGROUND_COLOR_GAME = "#92877d"
BACKGROUND_COLOR_CELL_EMPTY = "#9e948a"
BACKGROUND_COLOR_DICT = {2: "#eee4da", 4: "#ede0c8", 8: "#f2b179", 16: "#f59563",
                         32: "#f67c5f", 64: "#f65e3b", 128: "#edcf72", 256: "#edcc61",
                         512: "#edc850", 1024: "#edc53f", 2048: "#edc22e"}
CELL_COLOR_DICT = {2: "#776e65", 4: "#776e65", 8: "#f9f6f2", 16: "#f9f6f2",
                   32: "#f9f6f2", 64: "#f9f6f2", 128: "#f9f6f2", 256: "#f9f6f2",
                   512: "#f9f6f2", 1024: "#f9f6f2", 2048: "#f9f6f2"}
FONT = ("Verdana", 40, "bold")

KEY_UP_ALT = "\'\\uf700\'"
KEY_DOWN_ALT = "\'\\uf701\'"
KEY_LEFT_ALT = "\'\\uf702\'"
KEY_RIGHT_ALT = "\'\\uf703\'"

KEY_UP = "'z'"
KEY_DOWN = "'s'"
KEY_LEFT = "'q'"
KEY_RIGHT = "'d'"


class GraphicGameGrid:
    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, d):
        self.__dict__.update(d)

    def __init__(self, master):

        self.master = master
        self.master.title("2048")

        self.frame = tk.Frame(self.master, bg=BACKGROUND_COLOR_GAME, width=SIZE, height=SIZE)


        self.frame.bind_all("<Key>", self.key_down)

        self.commands = {KEY_UP: up, KEY_DOWN: down, KEY_LEFT: left, KEY_RIGHT: right,
                         KEY_UP_ALT: up, KEY_DOWN_ALT: down, KEY_LEFT_ALT: left, KEY_RIGHT_ALT: right}
                         
        self.commandsIA = {'up': up, 'down': down, 'left': left, 'right': right}

        self.grid_cells = []
        self.init_grid()
        self.init_matrix()
        self.update_grid_cells()
        self.placerFenetre()

    def etat(self):
        return game_state(self.matrix)

    def placerFenetre(self):

        self.master.update_idletasks()
        width = self.master.winfo_width()
        frm_width = self.master.winfo_rootx() - self.master.winfo_x()
        self.master_width = width + 2 * frm_width
        height = self.master.winfo_height()
        titlebar_height = self.master.winfo_rooty() - self.master.winfo_y()
        self.master_height = height + titlebar_height + frm_width
        x = self.master.winfo_screenwidth() // 2 - self.master_width // 2
        y = self.master.winfo_screenheight() // 2 - self.master_height // 2
        self.master.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        self.master.deiconify()

    def init_grid(self):

        self.frame.grid()
        for i in range(GRID_LEN):
            grid_row = []
            for j in range(GRID_LEN):
                cell = tk.Frame(self.frame, bg=BACKGROUND_COLOR_CELL_EMPTY, width=SIZE / GRID_LEN, height=SIZE / GRID_LEN)
                cell.grid(row=i, column=j, padx=GRID_PADDING, pady=GRID_PADDING)
                # font = Font(size=FONT_SIZE, family=FONT_FAMILY, weight=FONT_WEIGHT)
                t = tk.Label(master=cell, text="", bg=BACKGROUND_COLOR_CELL_EMPTY, justify=tk.CENTER, font=FONT, width=4,
                          height=2)
                t.grid()
                grid_row.append(t)

            self.grid_cells.append(grid_row)


    def init_matrix(self):
        self.matrix = new_game(4)

        generate_next(self.matrix)
        generate_next(self.matrix)

    def update_grid_cells(self):
        for i in range(GRID_LEN):
            for j in range(GRID_LEN):
                new_number = self.matrix[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(text="", bg=BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(text=str(new_number), bg=BACKGROUND_COLOR_DICT[new_number],
                                                    fg=CELL_COLOR_DICT[new_number])
        self.frame.update_idletasks()

    def key_down(self, event, IA=False):
        if not IA:
            key = repr(event.char)
            if key in self.commands:
                self.matrix, done = self.commands[repr(event.char)](self.matrix)
                if done:
                    generate_next(self.matrix)
                    self.update_grid_cells()
                    done = False
                    if game_state(self.matrix) == 'win':
                        self.grid_cells[1][1].configure(text="You", bg=BACKGROUND_COLOR_CELL_EMPTY)
                        self.grid_cells[1][2].configure(text="Win!", bg=BACKGROUND_COLOR_CELL_EMPTY)
                        return 1
                    if game_state(self.matrix) == 'lose':
                        self.grid_cells[1][1].configure(text="You", bg=BACKGROUND_COLOR_CELL_EMPTY)
                        self.grid_cells[1][2].configure(text="Lose!", bg=BACKGROUND_COLOR_CELL_EMPTY)
                        return 0
                else: return -1
        else:
            if event in self.commandsIA:
                self.matrix, done = self.commandsIA[event](self.matrix)
                if done:
                    generate_next(self.matrix)
                    self.update_grid_cells()
                    done = False
                    if self.etat == 'win':
                        self.grid_cells[1][1].configure(text="You", bg=BACKGROUND_COLOR_CELL_EMPTY)
                        self.grid_cells[1][2].configure(text="Win!", bg=BACKGROUND_COLOR_CELL_EMPTY)
                        return 1
                    elif self.etat == 'lose':
                        self.grid_cells[1][1].configure(text="You", bg=BACKGROUND_COLOR_CELL_EMPTY)
                        self.grid_cells[1][2].configure(text="Lose!", bg=BACKGROUND_COLOR_CELL_EMPTY)
                        return 0
                else:
                    return -1



