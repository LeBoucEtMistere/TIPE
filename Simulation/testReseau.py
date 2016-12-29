from ReseauNeural.Genome import Genome
import ReseauNeural.ReseauNeural as nn
from Config import Config

c = Config()
c.parser_config("Config.xml")

genomeRef = Genome.creer_connecte(0, c)
print(genomeRef)

reseau = nn.creer_phenotype(genomeRef)
# print(reseau.activer([1, 0]))

n=100
d=0
for i in range(1,n+1):
    genome = Genome.creer_connecte(i, c)
    if genomeRef.distance(genome)<= c.seuil_compatibilite :
        d += 1
print(str(100*d/n) + '% compatibles avec la reference')
