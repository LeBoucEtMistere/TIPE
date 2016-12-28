from ReseauNeural.Genome import Genome
import ReseauNeural.ReseauNeural as nn
from Config import Config

c = Config()
c.parser_config("Config.xml")

genome = Genome.creer_connecte(0, c)

reseau = nn.creer_phenotype(genome)
print(reseau.activer([1, 0]))

