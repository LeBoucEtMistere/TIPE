from Genome import Genome
from Espece import SetEspece


class Population:

    def __init__(self, config, taille):
        self.population = []
        for i in range(taille):
            self.population.append(Genome.creer_connecte(i, config))

        self.set_especes = SetEspece(config)
        self.set_especes.speciation(self.population)

    def evoluer(self, fitness_fonction, nbr_generation_max):
        pass

    def reproduction(self):
        pass
