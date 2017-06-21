from ReseauNeural.Population import Population
from ReseauNeural.ReseauNeural import creer_phenotype
from Config import Config


c = Config()
c.parser_config_xml("Config.xml")

xor_inputs = [(0.0, 0.0), (0.0, 1.0), (1.0, 0.0), (1.0, 1.0)]
xor_outputs = [   (0.0,),     (1.0,),     (1.0,),     (0.0,)]


def eval_genomes(genome):
    genome.fitness = 4.0
    reseau = creer_phenotype(genome)
    for xi, xo in zip(xor_inputs, xor_outputs):
        output = reseau.activer(xi)
        genome.fitness -= (output[0] - xo[0]) ** 2

population = Population(c, 150)
m = population.evoluer(eval_genomes, 500, 1)

print("Genome gagnant : fitness = {}".format(m.fitness))
print(m)





