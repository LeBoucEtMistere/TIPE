# Ce fichier gere le programme de simulation dans son ensemble, en lancant le jeu et en controlant l'AI

import tkinter as tk
from tkinter import font
import tkinter.filedialog as fd
import tkinter.simpledialog as sd

import queue
import threading

import Jeu.puzzle as pzl
import Jeu.puzzleIA as iapzl

from numpy import array

from time import gmtime, strftime

import Jeu.entrainement
import Jeu.IA

import os
import pickle
from platform import system as platform

import neat

class Demo1:
    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, d):
        self.__dict__.update(d)

    def __init__(self, master):

        ## UI RELATED ##

        self.file_opt = options = {}
        options['parent'] = master
        options['title'] = 'Choisissez un genome'

        self.master = master

        self.master.title("Simulation de 2048")

        l1 = tk.LabelFrame(self.master, text="Commandes générales", padx=20, pady=20)
        l1.grid(row=0, column=0, sticky=tk.W+tk.E+tk.N+tk.S, padx=10, pady=10)

        l2 = tk.LabelFrame(self.master, text="Contrôles de l'AI", padx=20, pady=20)
        l2.grid(row=1, column=0, sticky=tk.W+tk.E+tk.N+tk.S, padx=10, pady=10)

        l3 = tk.LabelFrame(self.master, text="Informations sur le génome", padx=20, pady=20)
        l3.grid(row=0, column=1, sticky=tk.W+tk.E+tk.N+tk.S, padx=10, pady=10)
        
        l4 = tk.LabelFrame(self.master, text="Informations sur l'entraînement", padx=20, pady=20)
        l4.grid(row=1, column=1, sticky=tk.W+tk.E+tk.N+tk.S, padx=10, pady=10)


        self.bouton_simulation = tk.Button(l1, text='Lancer la simulation', width=20, command = self.entrainer_IA)
        self.bouton_simulation.pack()

        self.bouton_jouer_2048 = tk.Button(l1, text = 'Jouer au 2048', width = 20, command = self.jouer_2048)
        self.bouton_jouer_2048.pack()

        self.bouton_quitter = tk.Button(l1, text='Quitter', width=20, command=self.quitter)
        self.bouton_quitter.pack()

        self.var_checkbox_calculs_paralleles = tk.IntVar()
        self.checkbox_calculs_paralleles = tk.Checkbutton(l1, text="Calculs en parallèle", variable =self.var_checkbox_calculs_paralleles)
        self.checkbox_calculs_paralleles.pack()
        self.var_checkbox_calculs_paralleles.set(1)


        self.var_nom_genome = tk.StringVar(value="Pas de génome chargé")
        self.label_ia_charge = tk.Label(l2, textvar=self.var_nom_genome)
        self.label_ia_charge.pack()

        self.bouton_charger_genome = tk.Button(l2, text='Charger un genome', width=20, command=self.demande_charger_genome)
        self.bouton_charger_genome.pack()

        self.bouton_jouer_2048_IA = tk.Button(l2, text='Faire jouer l\'IA au 2048', width=20, command=self.IA_jouer_2048)
        self.bouton_jouer_2048_IA.pack()

        self.var_checkbox_ia_visuelle = tk.IntVar()
        self.checkbox_ia_visuelle = tk.Checkbutton(l2, text="Jouer en mode visuel", variable=self.var_checkbox_ia_visuelle)
        self.checkbox_ia_visuelle.pack()

        self.var_fitness = tk.StringVar(value="Fitness du génome : NA")
        self.fitness_label = tk.Label(l3, textvar=self.var_fitness)
        self.fitness_label.pack()

        self.var_nbr_noeuds = tk.StringVar(value="Nombre de nœuds : NA")
        self.nbr_noeuds_label = tk.Label(l3, textvar=self.var_nbr_noeuds)
        self.nbr_noeuds_label.pack()

        self.var_nbr_connections = tk.StringVar(value="Nombre de connexions : NA")
        self.nbr_connections_label = tk.Label(l3, textvar=self.var_nbr_connections)
        self.nbr_connections_label.pack()

        self.var_entrainement_etat = tk.StringVar(value="Pas d'entraînement en cours")
        self.entrainement_report_etat = tk.Label(l4, textvar=self.var_entrainement_etat)
        f = font.Font(self.entrainement_report_etat, self.entrainement_report_etat.cget("font"))
        f.configure(underline=True)
        self.entrainement_report_etat.configure(font=f)
        self.entrainement_report_etat.pack()

        self.var_entrainement_pre = tk.StringVar(value="")
        self.entrainement_report_pre = tk.Label(l4, textvar = self.var_entrainement_pre)
        self.entrainement_report_pre.pack()

        self.var_entrainement_post = tk.StringVar(value="")
        self.entrainement_report_post = tk.Label(l4, textvar=self.var_entrainement_post)
        self.entrainement_report_post.pack()

        self.var_entrainement_end = tk.StringVar(value="")
        self.entrainement_report_end = tk.Label(l4, textvar=self.var_entrainement_end)
        self.entrainement_report_end.pack()

        self.var_entrainement_msg = tk.StringVar(value="")
        self.entrainement_report_msg = tk.Label(l4, textvar=self.var_entrainement_msg)
        self.entrainement_report_msg.pack()





        ## DATA RELATED ##

        self.genome_charge = None

        self.thread_entrainement = None

        self.textQueue = queue.Queue()

        self.master.bind('<<PreTextChanged>>', self.maj_text_pre)
        self.master.bind('<<PostTextChanged>>', self.maj_text_post)
        self.master.bind('<<EndTextChanged>>', self.maj_text_end)


    def maj_text_pre(self, event):
        self.var_entrainement_pre.set(self.textQueue.get())

    def maj_text_post(self, event):
        self.var_entrainement_post.set(self.textQueue.get())

    def maj_text_end(self, event):
        self.var_entrainement_end.set(self.textQueue.get())

    def demande_charger_genome(self):
        filename = fd.askopenfilename(**self.file_opt)
        self.charger_genome_depuis_fichier(filename)

    def charger_genome_depuis_fichier(self, fichier):
        if fichier != "":
            with open(fichier, 'rb') as f:
                self.genome_charge = pickle.load(f)
            nom_genome = os.path.splitext(os.path.basename(fichier))[0]

            self.var_nom_genome.set("Génome chargé : " + nom_genome)
            self.var_fitness.set("Fitness du génome : {}".format(self.genome_charge.fitness))
            self.var_nbr_noeuds.set("Nombre de nœud(s) : {}".format(len(self.genome_charge.connections)))
            self.var_nbr_connections.set("Nombre de connexion(s) : {}".format(len(self.genome_charge.nodes)))
        else:
            raise Exception("Chemin de fichier invalide")

    def jouer_2048(self):
        self.fenetre = tk.Toplevel(self.master)
        self.app = pzl.GraphicGameGrid(self.fenetre)

    def IA_jouer_2048(self):

        interface = 'visuelle' if self.var_checkbox_ia_visuelle.get() else 'console'

        if interface == 'visuelle':
            self.fenetre = tk.Toplevel(self.master)
            puzzle = pzl.GraphicGameGrid(self.fenetre)
        elif interface == 'console':
            puzzle = iapzl.IAGameGrid()

        if self.genome_charge == None:
            self.demande_charger_genome()
            if self.genome_charge == None :
                raise Exception("Impossible de charger un genome")

        local_dir = os.path.dirname(__file__)
        config_path = os.path.join(local_dir, 'config-feedforward')


        stats = Jeu.IA.faire_jouer_IA(self.genome_charge, config_path, puzzle, interface)

        if interface == "console":
            print(array(puzzle.matrix))
            print("Score pour cette grille : {}".format(puzzle.compter_somme()))
            print("Stats : cases vides : {}, bonus bords : {}, malus monotonie : {}, bonus adjaceant : {}".format(stats[0], stats[1], stats[2], stats[3]))


    def entrainer_IA(self):
        
        nbrGen = sd.askinteger('Nombre de générations', 'Combien de générations ?')

        dossier_local = os.path.dirname(__file__)
        chemin_config = os.path.join(dossier_local, 'config-feedforward')

        self.thread_entrainement = threading.Thread(target = Jeu.entrainement.run, args= (chemin_config,
                                                                                          nbrGen,
                                                                                          self.var_checkbox_calculs_paralleles,
                                                                                          self.entrainement_fini,
                                                                                          self.master,
                                                                                          self.textQueue))
        self.thread_entrainement.start()
        self.var_entrainement_etat.set("Entraînement en cours")
        self.bouton_simulation.config(state="disabled")
        self.bouton_quitter.config(state="disabled")


    def entrainement_fini(self, winner):

        self.var_entrainement_etat.set("Entraînement fini")

        dossier_local = os.path.dirname(__file__)

        dossier = os.path.join(dossier_local,'Genomes')
        nom_fichier = 'winner-feedforward({})_'.format(winner.fitness) + strftime("%Y-%m-%d %H_%M_%S", gmtime()) + '.genome'
        chemin = os.path.join(dossier, nom_fichier)

        with open(chemin, 'wb') as f:
            pickle.dump(winner, f)
            self.var_entrainement_msg.set("Génome sauvegardé sous : \n{0}".format(os.path.join('Genome',nom_fichier)))

        self.charger_genome_depuis_fichier(chemin)

        self.bouton_simulation.config(state="normal")
        self.bouton_quitter.config(state="normal")

        interface = 'visuelle' if self.var_checkbox_ia_visuelle.get() else 'console'
        chemin_config = os.path.join(dossier_local, 'config-feedforward')

        if interface == "console":
            puzzle = Jeu.puzzleIA.IAGameGrid()
            stats = Jeu.IA.faire_jouer_IA(winner, chemin_config, puzzle, interface)
            print(array(puzzle.matrix))
            print("Score pour cette grille : {}".format(puzzle.compter_somme()))
            print("Stats : cases vides : {}, bonus bords : {}, malus monotonie : {}, bonus adjaceant : {}".format(stats[0], stats[1], stats[2], stats[3]))
        elif interface == 'visuelle':
            self.fenetre = tk.Toplevel(self.master)
            puzzle = pzl.GraphicGameGrid(self.fenetre)
            Jeu.IA.faire_jouer_IA(winner, chemin_config, puzzle, interface)

    def quitter(self):

        self.master.destroy()

def main():
    root = tk.Tk()
    app = Demo1(root)
    if platform() == 'Darwin':  # How Mac OS X is identified by Python
        os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')
    root.mainloop()

if __name__ == '__main__':
    main()

