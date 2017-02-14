from ReseauNeural.Population import Population
from Config import Config

c = Config()
c.parser_config_xml("Config.xml")

population = Population(c, 100)
population.evoluer(lambda p: 1, 20)

print(population.population[0])




