# Ce fichier gere le programme de simulation dans son ensemble, en lancant le jeu et en controlant l'AI

import tkinter as tk
import tkinter.filedialog as fd
import tkinter.simpledialog as sd
import Jeu.puzzle as pzl
import Jeu.puzzleIA as iapzl

import time

import numpy as np

import Jeu.entrainement

import os
from math import log2
import pickle

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
        filename = fd.askopenfilename(**self.file_opt)
        if filename != "":
            self.fenetre = tk.Toplevel(self.master)
            puzzle = pzl.GraphicGameGrid(self.fenetre)
            
            with open(filename, 'rb') as f:
                genome = pickle.load(f)
            print('Loaded genome:')
            print(genome)
            
            local_dir = os.path.dirname(__file__)
            config_path = os.path.join(local_dir, 'config-feedforward')
            config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     config_path)
            
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            
            actions = {0: 'up', 1: 'down', 2: 'right', 3: 'left'}
            
            continuer = True
            
            while continuer:
                #On récupère les entrées et on les normalise
                mat = puzzle.matrix
                entrees = []
                for x in mat:
                    for y in x:
                        entrees.append(int(log2(y)) if y!=0 else 0)
                maximum = max(entrees)
                entrees = [x/maximum for x in entrees]
        
                #On active le réseau de neurone sur les entrees
                out = net.activate(entrees)
        
                #On récupère les mouvements dans l'ordre et on les teste tous
                sorties = {i: x for i, x in zip(range(4), out)}
                sorties = sorted(sorties.items(), key=lambda x: x[1], reverse=True)
        
                i = 0
                puzzle.master.update()
                time.sleep(0.2)
                b = puzzle.key_down(actions[sorties[0][0]],IA=True)
        
                if b == 0 or b == 1: break
        
                while b == -1:
                    i += 1
                    if i > 3:
                        # aucun mouvement n'est légal
                        continuer = False
                        print("Partie Finie")
                        break
        
                    b = puzzle.key_down(actions[sorties[i][0]],IA=True)
        
                if b == 0 or b == 1: break

    def entrainer_IA(self):
        print('entrainement IA')
        
        nbrGen = sd.askinteger('Nombre de générations', 'Combien de générations ?')

        local_dir = os.path.dirname(__file__)
        config_path = os.path.join(local_dir, 'config-feedforward')

        config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                             neat.DefaultSpeciesSet, neat.DefaultStagnation,
                             config_path)

        winner = Jeu.entrainement.run(config,nbrGen)

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

