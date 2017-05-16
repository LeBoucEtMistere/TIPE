import neat
from math import log2

import Jeu.puzzleIA

import Jeu.visualize
from Jeu.reporters import VarReporter

def eval_fitness_n_fois(genome,config):
    stats = []
    for i in range(1):
        stats.append(eval_fitness_simple(genome,config))
    return sum(stats)/len(stats)

def eval_fitness_simple(genome, config):
    pzl = Jeu.puzzleIA.IAGameGrid()
    net = neat.nn.FeedForwardNetwork.create(genome, config)

    actions = {0: 'up', 1: 'down', 2: 'right', 3: 'left'}

    continuer = True
    vides = 0
    bonus_bords = 0
    malus_monotone = 0
    bonus_adjacents = 0

    poids_malus = 0.1


    while continuer:

        # On récupère les entrées et on les normalise

        mat = pzl.matrix
        entrees = []
        for x in mat:
            for y in x:
                entrees.append(int(log2(y)) if y != 0 else 0)
        maximum = max(entrees)
        entrees = [x / maximum for x in entrees]

        # On compte les cases vides

        vides += pzl.compter_vides()

        # On donne des bonus aux tuiles qui sont sur les bords et qui sont grandes et malus aux petites sur les bords

        n = len(mat)
        for i in range(n):
            for j in range(n):
                if i == 0 or i == n-1 or j==0 or j==n-1:  #Si on est sur un bord
                    if (int(log2(mat[i][j])/maximum) if mat[i][j] != 0 else 0) > 0.4:  #Si la case doit être gratifiée
                        bonus_bords += 1
                    else :
                        bonus_bords -= 1
                else:  #Si on n'est pas sur un bord
                    if (int(log2(mat[i][j])/maximum) if mat[i][j] != 0 else 0) > 0.4:  #Si la case doit être pénalisée
                        bonus_bords -= 1

        # On pénalise les lignes et colonnes non monotonnes. La pénalité dépend de la somme des valeurs

        #Lignes
        for i in range(n):
            somme_ligne = sum(mat[i])
            indice_max = 0
            for j in range(1,n):
                if mat[i][j] > mat[i][indice_max]:
                    indice_max = j
            if indice_max != 0 and indice_max != n : #La ligne ne peut pas être monotone
                malus_monotone -= poids_malus * somme_ligne
            else:
                if indice_max == 0:
                    for j in range(1,n):
                        if mat[i][j] >= mat[i][j-1]: malus_monotone -= poids_malus * somme_ligne  #La croissance n'est pas respectée
                else:
                    for j in range(1,n):
                        if mat[i][j] <= mat[i][j-1]: malus_monotone -= poids_malus * somme_ligne  #La décroissance n'est pas respectée

        #Colonnes
        for j in range(n):
            col = [mat[i][j] for i in range(n)]
            somme_col = sum(col)
            indice_max = 0
            for i in range(1, n):
                if col[j] > col[indice_max]:
                    indice_max = i
            if indice_max != 0 and indice_max != n:  # La colonne ne peut pas être monotone
                malus_monotone -= poids_malus * somme_col
            else:
                if indice_max == 0:
                    for i in range(1, n):
                        if mat[i-1][j] >= mat[i][j]: malus_monotone -= poids_malus * somme_col  # La croissance n'est pas respectée
                else: #indice_max = n
                    for i in range(1, n):
                        if mat[i-1][j] <= mat[i][j]: malus_monotone -= poids_malus * somme_col  # La décroissance n'est pas respectée


        # On donne des bonus pour les cases adjacentes qui peuvent fusioner
        for i in range(n-1):
            for j in range(n-1):
                if mat[i][j] == mat[i][j+1] :
                    bonus_adjacents += 1
                if mat[i][j] == mat[i+1][j] :
                    bonus_adjacents += 1
        for i in range(n-1):
            if mat[i][j] == mat[i+1][j] :
                bonus_adjacents += 1
        for j in range(n-1):
            if mat[i][j] == mat[i][j+1] :
                bonus_adjacents += 1




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

    return vides + 7 * bonus_bords + 0.080 * malus_monotone + 15 * bonus_adjacents

def eval_fitness(genomes, config):
    for genome_id, genome in genomes:
        genome.fitness = eval_fitness_simple(genome, config)


def run(config_path, nbrGen, parallele, callback, root, queue):


    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    #p.add_reporter(neat.StdOutReporter(True))
    p.add_reporter(VarReporter(False, root, queue))
    #stats = neat.StatisticsReporter()
    #p.add_reporter(stats)
    #p.add_reporter(neat.Checkpointer(1000))

    winner = None

    if parallele:
        pe = neat.ParallelEvaluator(4, eval_fitness_n_fois)
        winner = p.run(pe.evaluate, nbrGen)
    else:
        # Run for up to n generations.
        winner = p.run(eval_fitness, nbrGen)
    
    #Jeu.visualize.plot_stats(stats, ylog=False)
    #Jeu.visualize.plot_species(stats)

    return callback(winner)

