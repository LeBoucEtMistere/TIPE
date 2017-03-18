from Jeu.logique import *
from random import *

GRID_LEN = 4


class IAGameGrid:
    def __init__(self):

        self.commands = {'up': up, 'down': down, 'left': left, 'right': right}

        self.grid_cells = []
        self.init_matrix()

        self.coeffs = {2:1, 4:1, 8:1.2, 16:1.2, 32:1.4, 64:1.4, 128:1.8, 256:2, 512:3, 1024:4, 2048:6}


    def init_matrix(self):
        self.matrix = new_game(4)

        generate_next(self.matrix)
        generate_next(self.matrix)


    def etat(self):
        return game_state(self.matrix)


    def compter_vides(self):
        vides = 0
        for x in self.matrix:
            for y in x:
                vides += 1 if y == 0 else 0
        return vides

    def compter_somme(self):
        somme = 0
        for x in self.matrix:
            for y in x:
                somme += y
        return somme


    def ia_key_down(self, key):
        if key in self.commands:
            self.matrix, done = self.commands[key](self.matrix)
            if done:
                generate_next(self.matrix)
                done = False
                if self.etat == 'win':
                    return 1
                elif self.etat == 'lose':
                    return 0
            else:
                return -1

