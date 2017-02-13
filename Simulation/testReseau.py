from ReseauNeural.Population import Population
from Config import Config

import matplotlib.pyplot as plt
import numpy as np

c = Config()
c.parser_config_xml("Config.xml")


T = [k for k in np.arange(0.8,1.6,0.1)]
L = []

for k in T:
    c.seuil_compatibilite = k
    population = Population(c, 1000)
    L.append(population.set_especes.nbr_espece)

plt.plot(T, L)
plt.show()



