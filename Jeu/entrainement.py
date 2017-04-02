import neat
from math import log2

import Jeu.puzzleIA

import Jeu.visualize
from Jeu.reporters import VarReporter

def eval_fitness_simple(genome, config):
    pzl = Jeu.puzzleIA.IAGameGrid()
    net = neat.nn.FeedForwardNetwork.create(genome, config)

    actions = {0: 'up', 1: 'down', 2: 'right', 3: 'left'}

    continuer = True
    vides = 0

    while continuer:

        # On récupère les entrées et on les normalise
        vides += pzl.compter_vides()
        mat = pzl.matrix
        entrees = []
        for x in mat:
            for y in x:
                entrees.append(int(log2(y)) if y != 0 else 0)
        maximum = max(entrees)
        entrees = [x / maximum for x in entrees]

        # On active le réseau de neurone sur les entrees
        out = net.activate(entrees)

        # On récupère les mouvements dans l'ordre et on les teste tous
        sorties = {i: x for i, x in zip(range(4), out)}
        sorties = sorted(sorties.items(), key=lambda x: x[1], reverse=True)

        i = 0
        b = pzl.ia_key_down(actions[sorties[0][0]])

        if b == 0 or b == 1: break

        while b == -1:
            i += 1
            if i > 3:
                # aucun mouvement n'est légal
                continuer = False
                break

            b = pzl.ia_key_down(actions[sorties[i][0]])

        if b == 0 or b == 1: break

    somme = pzl.compter_somme()
    return somme + 50 * vides

def eval_fitness(genomes, config):
    for genome_id, genome in genomes:
        genome.fitness = eval_fitness_simple(genome, config)


def run(config_path, nbrGen, report_var, parallele, callback):


    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    #p.add_reporter(neat.StdOutReporter(True))
    p.add_reporter(VarReporter(False, report_var))
    #stats = neat.StatisticsReporter()
    #p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(100))

    winner = None

    if parallele:
        pe = neat.ParallelEvaluator(4, eval_fitness_simple)
        winner = p.run(pe.evaluate, nbrGen)
    else:
        # Run for up to n generations.
        winner = p.run(eval_fitness, nbrGen)
    
    #Jeu.visualize.plot_stats(stats, ylog=False)
    #Jeu.visualize.plot_species(stats)

    return callback(winner)

