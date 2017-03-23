import neat
from math import log2
from time import gmtime, strftime

NBR_GENERATIONS = 2

import Jeu.puzzleIA

import Jeu.visualize

import os
import pickle

def eval_genome(genome, puzzle, config):
    net = neat.nn.FeedForwardNetwork.create(genome, config)

    actions = {0: 'up', 1: 'down', 2: 'right', 3: 'left'}

    continuer = True

    while continuer:

        #On récupère les entrées et on les normalise
        mat = puzzle.matrix
        entrees = []
        for x in mat:
            for y in x:
                entrees.append(int(log2(y)) if y!=0 else 0)
        maximum = max(entrees)
        entrees = [x/maximum for x in entrees]

        #On active le réseau de neurone sur les entrees
        out = net.activate(entrees)

        #On récupère les mouvements dans l'ordre et on les teste tous
        sorties = {i: x for i, x in zip(range(4), out)}
        sorties = sorted(sorties.items(), key=lambda x: x[1], reverse=True)

        i = 0
        b = puzzle.ia_key_down(actions[sorties[0][0]])

        if b == 0 or b == 1: break

        while b == -1:
            i += 1
            if i > 3:
                # aucun mouvement n'est légal
                continuer = False
                break

            b = puzzle.ia_key_down(actions[sorties[i][0]])

        if b == 0 or b == 1: break

def eval_fitness(genomes, config):

    for genome_id, genome in genomes:
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
        genome.fitness = somme + 50 * vides

def run(config, nbrGen):

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(100))

    # Run for up to n generations.
    winner = p.run(eval_fitness, nbrGen)

    path = 'winner-feedforward({})_'.format(winner.fitness) + strftime("%Y-%m-%d %H_%M_%S", gmtime()) + '.genome'
    with open(path, 'wb') as f:
        pickle.dump(winner, f)
    
    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))
    
    #Jeu.visualize.plot_stats(stats, ylog=False)
    #Jeu.visualize.plot_species(stats)

    return winner

def faire_jouer_genome(genome, config):
    pzl = Jeu.puzzleIA.IAGameGrid()
    eval_genome(genome, pzl, config)
    return pzl
