from Genome import Genome
from Espece import SetEspece

from random import choice
from operator import attrgetter

import matplotlib.pyplot as plt
import numpy as np
import time as tm


def update_line(hl, new_data_x, new_data_y):
    hl.set_xdata(np.append(hl.get_xdata(), new_data_x))
    hl.set_ydata(np.append(hl.get_ydata(), new_data_y))
    plt.pause(0.05)


class Population:

    def __init__(self, config, taille_pop):
        self.population = []
        self.indexer = 0
        self.taille_pop = taille_pop
        for i in range(self.taille_pop):
            self.population.append(Genome.creer_connecte(self.nouvel_index(), config))

        self.set_especes = SetEspece(config)
        self.set_especes.speciation(self.population)

    def nouvel_index(self):
        self.indexer += 1
        return self.indexer - 1

    def evoluer(self, fitness_fonction, nbr_generation_max, log=0):

        self.evaluer_fitness(fitness_fonction)

        meilleur = None

        plt.ion()

        f, axarr = plt.subplots(3, sharex=True, figsize=(15, 9))

        max_line = axarr[0].plot([], [], 'r', label='Fitness Maximale')
        moy_line = axarr[0].plot([], [], 'b', label='Fitness Moyenne')
        axarr[0].set_title('Evolution de la Fitness')
        axarr[0].axis([0, nbr_generation_max, 0, 5])
        axarr[0].set_ylabel("Fitness")
        axarr[0].legend()

        pop_line = axarr[1].plot([], [], 'g', label='Population Totale')
        axarr[1].axis([0, nbr_generation_max, 0, len(self.population)*3/2])
        axarr[1].set_ylabel("Population")
        axarr[1].legend()

        espece_line = axarr[2].plot([], [], 'y', label='Nombre d\'especes')
        axarr[2].axis([0, nbr_generation_max, 0, 20])
        axarr[2].set_xlabel("Generations")
        axarr[2].set_ylabel("Especes")
        axarr[2].legend()

        f.canvas.set_window_title('Evolution de l\'algorithme')



        tref = tm.clock()

        for i in range(nbr_generation_max):
            repro_stat = self.reproduction()
            self.evaluer_fitness(fitness_fonction)
            tab_fitness = [m.fitness for m in self.population]
            max_fitness = max(tab_fitness)
            moy_fitness = sum(tab_fitness)/len(tab_fitness)

            if log != 0:
                if i%10 == 0:
                    print("Temps de travail : {}s".format(int(tm.clock()-tref)))
                    print("Generation : {} / fitness maximale : {} / fitness moyenne : {}".format(i+1, max_fitness, moy_fitness))
                    print(repro_stat)

            update_line(max_line[0], i, max_fitness)
            update_line(moy_line[0], i, moy_fitness)
            update_line(pop_line[0], i, len(self.population))
            update_line(espece_line[0], i, self.set_especes.nbr_espece)

            for g in self.population:
                if g.fitness == max_fitness:
                    if meilleur is None:
                        meilleur = g
                    elif g.fitness > meilleur.fitness:
                        meilleur = g

        plt.ioff()
        plt.show()

        return meilleur

    def reproduction(self):

        fitness_ajustee = {}
        for espece in self.set_especes.especes:
            fitness_ajustee[espece] = sum([m.fitness for m in espece.membres]) / len(espece.membres)

        fitness_ajustee_moyenne = sum(fitness_ajustee.values()) / len(fitness_ajustee)

        qte_spawn = {}
        for s, sfitness in fitness_ajustee.items():
            spawn = len(s.membres)
            if sfitness > fitness_ajustee_moyenne:
                spawn = max(spawn + 2, spawn * 1.2)
            else:
                spawn = max(spawn * 0.8, 2)
            qte_spawn[s] = spawn

        total_spawn = sum(qte_spawn.values())
        norm = self.taille_pop / total_spawn

        a_spawner = {espece: int(round(n * norm)) for espece, n in qte_spawn.items()}

        #affichage debug
        s="/----\n"
        s+="        -- fitness moyenne ajustee {} -- total spawn {} -- \n".format(fitness_ajustee_moyenne,total_spawn)
        for espece,qte in a_spawner.items():
            s+="----- Espece n{}, fitness ajustee {}, a spawner {}\n".format(espece.ID, fitness_ajustee[espece], qte)
        s+='----/\n'


        self.population = []

        for espece in self.set_especes.especes:
            if len(espece.membres) <= 0 : continue
            membre_trie = sorted(espece.membres, reverse=True, key=lambda x: x.fitness)
            a_garder = int(0.6 * len(membre_trie))
            if a_garder == 0 : continue
            pour_repro = membre_trie[:a_garder]
            nouvelle_espece = []
            for i in range(a_spawner[espece]):
                parent1 = choice(pour_repro)
                parent2 = choice(pour_repro)
                enfant = parent1.crossover(parent2, self.nouvel_index())
                enfant.muter()
                nouvelle_espece.append(enfant)

            self.population.extend(nouvelle_espece)

        self.set_especes.speciation(self.population)

        return s

    def evaluer_fitness(self, fitness_fonction):
        for p in self.population:
            fitness_fonction(p)
