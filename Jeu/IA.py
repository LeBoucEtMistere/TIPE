import neat
from math import log2
from time import sleep, clock

# Ce fichier gere les heuristiques et l'algorithme de jeu de l'IA au 2048


def faire_jouer_IA(genome, config_path, puzzle, interface):
    assert interface == 'visuelle' or 'console'

    # configuration de NEAT
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    # Creation du réseau
    net = neat.nn.FeedForwardNetwork.create(genome, config)

    actions = {0: 'up', 1: 'down', 2: 'right', 3: 'left'}

    continuer = True

    # Declaration des heuristiques
    vides = 0
    bonus_bords = 0
    malus_monotone = 0
    bonus_adjacents = 0

    poids_malus = 0.1

    while continuer:

        # On récupère les entrées et on les normalise
        mat = puzzle.matrix
        entrees = []
        for x in mat:
            for y in x:
                entrees.append(int(log2(y)) if y != 0 else 0)
        maximum = max(entrees)
        entrees = [x / maximum for x in entrees]

        ## HEURISTIQUE 1 ##
        # On compte les cases vides

        vides += puzzle.compter_vides()

        ## HEURISTIQUE 2 ##
        # On donne des bonus aux tuiles qui sont sur les bords et qui sont grandes

        n = len(mat)
        for i in range(n):
            for j in range(n):
                if i == 0 or i == n - 1 or j == 0 or j == n - 1:  # Si on est sur un bord
                    if (int(log2(mat[i][j]) / maximum) if mat[i][j] != 0 else 0) > 0.4:  # Si la case doit être gratifiée
                        bonus_bords += 1
                else:  # Si on n'est pas sur un bord
                    if (int(log2(mat[i][j]) / maximum) if mat[i][j] != 0 else 0) > 0.4:  # Si la case doit être pénalisée
                        bonus_bords -= 3


        ## HEURISTIQUE 3 ##
        # On pénalise les lignes et colonnes non monotonnes. La pénalité dépend de la somme des valeurs

        # Lignes
        for i in range(n):
            somme_ligne = sum(mat[i])
            indice_max = 0
            for j in range(1, n):
                if mat[i][j] > mat[i][indice_max]:
                    indice_max = j
            if indice_max != 0 and indice_max != n:  # La ligne ne peut pas être monotone
                malus_monotone -= poids_malus * somme_ligne
            else:
                if indice_max == 0:
                    for j in range(1, n):
                        if mat[i][j] >= mat[i][j - 1]: malus_monotone -= poids_malus * somme_ligne  # La croissance n'est pas respectée
                else:
                    for j in range(1, n):
                        if mat[i][j] <= mat[i][j - 1]: malus_monotone -= poids_malus * somme_ligne  # La décroissance n'est pas respectée

        # Colonnes
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
                        if mat[i - 1][j] >= mat[i][j]: malus_monotone -= poids_malus * somme_col  # La croissance n'est pas respectée
                else:  # indice_max = n
                    for i in range(1, n):
                        if mat[i - 1][j] <= mat[i][j]: malus_monotone -= poids_malus * somme_col  # La décroissance n'est pas respectée


        ## HEURISTIQUE 4 ##
        # On donne des bonus pour les cases adjacentes qui peuvent fusioner
        for i in range(n - 1):
            for j in range(n - 1):
                if mat[i][j] == mat[i][j + 1]:
                    bonus_adjacents += 1
                if mat[i][j] == mat[i + 1][j]:
                    bonus_adjacents += 1
        for i in range(n - 1):
            if mat[i][j] == mat[i + 1][j]:
                bonus_adjacents += 1
        for j in range(n - 1):
            if mat[i][j] == mat[i][j + 1]:
                bonus_adjacents += 1

        # On active le réseau de neurone sur les entrees
        out = net.activate(entrees)

        # On récupère les mouvements dans l'ordre et on les teste tous
        sorties = {i: x for i, x in zip(range(4), out)}
        sorties = sorted(sorties.items(), key=lambda x: x[1], reverse=True)

        i = 0
        b = None

        if interface == 'visuelle':
            puzzle.master.update()
            sleep(0.2)
            b = puzzle.key_down(actions[sorties[0][0]], IA=True)
        elif interface == 'console':
            b = puzzle.ia_key_down(actions[sorties[0][0]])

        if b == 0 or b == 1:
            break

        while b == -1:
            i += 1
            if i > 3:
                # aucun mouvement n'est légal
                continuer = False
                break

            if interface == 'visuelle':
                puzzle.master.update()
                sleep(0.2)
                b = puzzle.key_down(actions[sorties[i][0]], IA=True)
            elif interface == 'console':
                b = puzzle.ia_key_down(actions[sorties[i][0]])

        if b == 0 or b == 1:
            break

    return vides, bonus_bords, malus_monotone, bonus_adjacents


# version mesurant les performances
def faire_jouer_IA_perf(genome, config_path, puzzle):

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    net = neat.nn.FeedForwardNetwork.create(genome, config)

    actions = {0: 'up', 1: 'down', 2: 'right', 3: 'left'}

    continuer = True

    stats = []

    while continuer:
        t1 = clock()

        # On récupère les entrées et on les normalise
        mat = puzzle.matrix
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

        b = puzzle.ia_key_down(actions[sorties[0][0]])

        if b == 0 or b == 1:
            stats.append(clock()-t1)
            break

        while b == -1:
            i += 1
            if i > 3:
                # aucun mouvement n'est légal
                continuer = False
                stats.append(clock() - t1)
                break

            b = puzzle.ia_key_down(actions[sorties[i][0]])

        if b == 0 or b == 1:
            stats.append(clock() - t1)
            break

        stats.append(clock() - t1)

    return sum(stats)/len(stats)
