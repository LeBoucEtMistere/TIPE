# Ce fichier gère le programme de simulation dans son ensemble, en lançant le jeu et en contrôlant l'AI

import tkinter as tk
import Jeu.puzzle as pzl

class Demo1:
    def __init__(self, master):
        self.master = master

        self.master.title("Simulation de 2048")

        f1 = tk.Frame(self.master)
        f1.pack(side=tk.LEFT)

        l1 = tk.LabelFrame(f1, text="Commandes générales", padx=20, pady=20)
        l1.pack(fill="both", expand="yes")

        l2 = tk.LabelFrame(f1, text="Contrôles de l'AI", padx=20, pady=20)
        l2.pack(fill="both", expand="yes")

        l3 = tk.LabelFrame(self.master, text="Statistiques", padx=20, pady=20)
        l3.pack(fill="both", expand="yes", side=tk.LEFT)

        tk.Label(l2, text="A l'intérieure de la frame 2").pack()
        tk.Label(l3, text="A l'intérieure de la frame 3").pack()

        self.bouton_simulation = tk.Button(l1, text='Lancer la simulation', width=20)
        self.bouton_simulation.pack()

        self.bouton_jouer_2048 = tk.Button(l1, text = 'Jouer au 2048', width = 20, command = self.jouer_2048)
        self.bouton_jouer_2048.pack()

        self.bouton_quitter = tk.Button(l1, text='Quitter', width=20, command=self.quitter)
        self.bouton_quitter.pack()


    def jouer_2048(self):
        self.fenetre = tk.Toplevel(self.master)
        self.app = pzl.GameGrid(self.fenetre)

    def quitter(self):

        self.master.destroy()


def main():
    root = tk.Tk()
    app = Demo1(root)
    root.mainloop()

if __name__ == '__main__':
    main()

