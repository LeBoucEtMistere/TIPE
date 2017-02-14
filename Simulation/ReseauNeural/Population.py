from Genome import Genome
from Espece import SetEspece

from random import choice
from operator import attrgetter


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

    def evoluer(self, fitness_fonction, nbr_generation_max):
        for _ in range(nbr_generation_max):
            self.evaluer_fitness(fitness_fonction)
            self.reproduction()

    def reproduction(self):

        fitness_ajustee = {}
        for espece in self.set_especes.especes:
            fitness_ajustee[espece] = sum([m.fitness for m in espece.membres]) / len(espece.membres)

        fitness_ajustee_moyenne = sum(fitness_ajustee.values()) / len(fitness_ajustee)

        qte_spawn = {}
        for s, sfitness in fitness_ajustee.items():
            spawn = len(s.membres)
            if sfitness > fitness_ajustee_moyenne:
                spawn = max(spawn + 2, spawn * 1.1)
            else:
                spawn = max(spawn * 0.9, 2)
            qte_spawn[s] = spawn

        total_spawn = sum(qte_spawn.values())
        norm = self.taille_pop / total_spawn

        a_spawner = {espece: int(round(n * norm)) for espece, n in qte_spawn.items()}

        self.population = []

        for espece in self.set_especes.especes:
            membre_trie = sorted(espece.membres, key=attrgetter('fitness'))
            a_enlever = int(0.2 * len(membre_trie))
            pour_repro = membre_trie[:len(membre_trie)-a_enlever]
            nouvelle_espece = []
            for i in range(a_spawner[espece]):
                parent1 = choice(pour_repro)
                parent2 = choice(pour_repro)
                enfant = parent1.crossover(parent2, self.nouvel_index())
                enfant.muter()
                nouvelle_espece.append(enfant)

            self.population.extend(nouvelle_espece)

        self.set_especes.speciation(self.population)

    def evaluer_fitness(self, fitness_fonction):
        for p in self.population:
            p.fitness = fitness_fonction(p)
