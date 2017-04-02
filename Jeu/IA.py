import neat
from math import log2
from time import sleep


def faire_jouer_IA(genome, config_path, puzzle, interface):
    assert interface == 'visuelle' or 'console'

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    net = neat.nn.FeedForwardNetwork.create(genome, config)

    actions = {0: 'up', 1: 'down', 2: 'right', 3: 'left'}

    continuer = True

    while continuer:
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
