from ReseauNeural.Genome import Genome
from ReseauNeural.Espece import SetEspece
from Config import Config

import matplotlib.pyplot as plt
import numpy as np

c = Config()
c.parser_config_xml("Config.xml")


T = [k for k in np.arange(0.8,1.6,0.1)]
L = [0] * len(T)
j=0

for k in T:
    c.seuil_compatibilite = k
    population = []
    for i in range(1000):
        population.append(Genome.creer_connecte(i, c))

    s = SetEspece(c)
    s.speciation(population)
    L[j] = s.nbr_espece
    j += 1

plt.plot(T,L)
plt.show()



