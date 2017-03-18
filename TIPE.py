# Ce fichier gere le programme de simulation dans son ensemble, en lancant le jeu et en controlant l'AI

import tkinter as tk
import tkinter.filedialog as fd
import Jeu.puzzle as pzl
import Jeu.puzzleIA as iapzl

import numpy as np

import Jeu.entrainement

import os

import neat


class Demo1:
    def __init__(self, master):

        self.file_opt = options = {}
        options['parent'] = master
        options['title'] = 'Choisissez un genome'

        self.master = master

        self.master.title("Simulation de 2048")

        f1 = tk.Frame(self.master)
        f1.pack(side=tk.LEFT)

        l1 = tk.LabelFrame(f1, text="Commandes generales", padx=20, pady=20)
        l1.pack(fill="both", expand="yes")

        l2 = tk.LabelFrame(f1, text="Controles de l'AI", padx=20, pady=20)
        l2.pack(fill="both", expand="yes")

        l3 = tk.LabelFrame(self.master, text="Statistiques", padx=20, pady=20)
        l3.pack(fill="both", expand="yes", side=tk.LEFT)

        tk.Label(l2, text="A l'interieure de la frame 2").pack()
        tk.Label(l3, text="A l'interieure de la frame 3").pack()

        self.bouton_simulation = tk.Button(l1, text='Lancer la simulation', width=20, command = self.entrainer_IA)
        self.bouton_simulation.pack()

        self.bouton_jouer_2048 = tk.Button(l1, text = 'Jouer au 2048', width = 20, command = self.jouer_2048)
        self.bouton_jouer_2048.pack()

        self.bouton_jouer_2048_IA = tk.Button(l1, text='Faire jouer l\'IA au 2048', width=20, command=self.IA_jouer_2048)
        self.bouton_jouer_2048_IA.pack()

        self.bouton_quitter = tk.Button(l1, text='Quitter', width=20, command=self.quitter)
        self.bouton_quitter.pack()


    def jouer_2048(self):
        self.fenetre = tk.Toplevel(self.master)
        self.app = pzl.GraphicGameGrid(self.fenetre)

    def IA_jouer_2048(self):
        f = fd.askopenfile(mode='r', **self.file_opt)
        if f:
            self.app = iapzl.IAGameGrid()

        f.close()

    def entrainer_IA(self):
        print('entrainement IA')

        local_dir = os.path.dirname(__file__)
        config_path = os.path.join(local_dir, 'config-feedforward')

        config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                             neat.DefaultSpeciesSet, neat.DefaultStagnation,
                             config_path)

        winner = Jeu.entrainement.run(config)

        pzl=Jeu.entrainement.faire_jouer_genome(winner,config)
        print(np.array(pzl.matrix))
        print(pzl.compter_somme())

        pzl2 = Jeu.entrainement.faire_jouer_genome(winner, config)
        print(np.array(pzl2.matrix))
        print(pzl2.compter_somme())

    def quitter(self):

        self.master.destroy()


def main():
    root = tk.Tk()
    app = Demo1(root)
    root.mainloop()

if __name__ == '__main__':
    main()

