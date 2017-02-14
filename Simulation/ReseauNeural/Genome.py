import Gene

import sys

from random import shuffle, gauss, choice, randint, random
from math import fabs

# Instead of adding six as a dependency, this code was copied from the six
# implementation, six is Copyright (c) 2010-2015 Benjamin Peterson
if sys.version_info[0] == 3:
    def itervalues(d, **kw):
        return iter(d.values(**kw))

    def iteritems(d, **kw):
        return iter(d.items(**kw))
else:
    def itervalues(d, **kw):
        return iter(d.itervalues(**kw))

    def iteritems(d, **kw):
        return iter(d.iteritems(**kw))


class Genome(object):

    def __init__(self, ID, config, parent1_id, parent2_id):
        self.config = config
        self.ID = ID
        self.nbr_entrees = 0
        self.nbr_sorties = 0
        self.nbr_caches = 0

        # dictionnaires de la forme pair(id,gene)
        self.connexions = {}
        self.noeuds = {}

        self.fitness = None
        self.espece_id = None

        # IDs des genomes parents, utilises pour garder une trace de la genealogie
        self.parent1_id = parent1_id
        self.parent2_id = parent2_id

    def crossover(self, autre, id_enfant):
        """ Renvoie l'enfant issue du crossover des deux parents """

        # Les parents doivent appartenir a la meme espece
        assert self.espece_id == autre.espece_id, 'Parents de 2 especes differnetes : {0} vs {1}'.format(self.espece_id, autre.espece_id)

        if self.fitness > autre.fitness:
            parent1 = self
            parent2 = autre
        else:
            parent1 = autre
            parent2 = self

        # creer un nouvel enfant
        enfant = Genome(id_enfant, self.config, self.ID, autre.ID)

        enfant.heriter_genes(parent1, parent2)

        enfant.espece_id = parent1.espece_id

        return enfant

    def heriter_genes(self, parent1, parent2):
        """ Applique l'operateur de crossover """
        assert (parent1.fitness >= parent2.fitness)
        # le parent 1 est le meilleur au sens de la fitness

        # Crossover des genes de connexion
        for cg1 in parent1.connexions.values():
            try:
                cg2 = parent2.connexions[cg1.cle]
            except KeyError:  # le gene de meme marqueur historique n'existe pas chez le parent 2
                # On copie les genes en exces ou disjoints du parent 1
                self.connexions[cg1.cle] = cg1.copier()
            else:
                if cg2.est_meme_innovation(cg1):
                    # On a trouve un gene homologue
                    nouveau_gene = cg1.reproduire_avec(cg2)
                else:
                    nouveau_gene = cg1.copier()
                self.connexions[nouveau_gene.cle] = nouveau_gene

        # Crossover des genes noeuds
        for ng1_id, ng1 in parent1.noeuds.items():
            ng2 = parent2.noeuds.get(ng1_id)
            if ng2 is None:
                # on copie les genes en plus du parent 1
                nouveau_gene = ng1.copier()
            else:
                # sinon on fait le choix aleatoire entre les caracteristiques des 2 parents
                nouveau_gene = ng1.reproduire_avec(ng2)

            assert nouveau_gene.ID not in self.noeuds
            self.noeuds[nouveau_gene.ID] = nouveau_gene

    def ajouter_noeud_cache(self, couche):
        nouvel_id = self.nouvel_id_cache()
        self.noeuds[nouvel_id] = Gene.Noeud(nouvel_id, couche, 'CACHE', activation=self.config.fonctions_activation.get_aleatoire())
        self.nbr_caches += 1
        self.ordre_noeuds.append(nouvel_id)

    def ajouter_noeuds_caches(self, nbr, couche):
        for i in range(nbr):
            id_noeud = self.nouvel_id_cache()
            noeud = Gene.Noeud(id_noeud, couche, 'CACHE', activation=self.config.fonctions_activation.get_aleatoire())
            assert noeud.ID not in self.noeuds
            self.noeuds[noeud.ID] = noeud
            self.nbr_caches += 1

    def calculer_toutes_connexions(self):
        genes_entree = [g for g in self.noeuds.values() if g.type == 'ENTREE']
        genes_cache = [g for g in self.noeuds.values() if g.type == 'CACHE']
        genes_sortie = [g for g in self.noeuds.values() if g.type == 'SORTIE']

        # Connecter chaque noeud d'entree a tous les noeuds cache et de sortie.
        connexions = []
        for ig in genes_entree:
            for og in genes_sortie + genes_cache:
                connexions.append((ig.ID, og.ID))

        # Connecter chaque noeud cache a tous les noeuds de sortie.
        for hg in genes_cache:
            for og in genes_sortie:
                connexions.append((hg.ID, og.ID))
        return connexions

    def connecter_entierement(self):
        for input_id, output_id in self.calculer_toutes_connexions():
            poids = gauss(0,self.config.cri_distribution_poids_sigma)
            cg = Gene.Connexion(input_id, output_id, poids, True)
            self.connexions[cg.cle] = cg

    def connecter_partiellement(self, fraction):
        assert 0 <= fraction <= 1
        toutes_connexions = self.calculer_toutes_connexions()
        shuffle(toutes_connexions)
        nbr_a_ajouter = int(round(len(toutes_connexions) * fraction))
        for id_entree, id_sortie in toutes_connexions[:nbr_a_ajouter]:
            poids = gauss(0,self.config.cri_distribution_poids_sigma)
            cg = Gene.Connexion(id_entree, id_sortie, poids, True)
            self.connexions[cg.cle] = cg

    def muter(self):
        """ Fait muter ce genome """

        if random() < self.config.prob_ajout_noeud:
            self.muter_ajouter_noeud()

        if random() < self.config.prob_ajout_connexion:
            self.muter_ajouter_connection()

        if random() < self.config.prob_enlever_noeud:
            self.muter_enlever_noeud()

        if random() < self.config.prob_enlever_connexion:
            self.muter_enlever_connection()

        # Muter les genes de connexion
        for cg in self.connexions.values():
            cg.muter(self.config)

        # Muter les genes noeuds
        for ng in self.noeuds.values():
            if ng.type != 'INPUT':
                ng.muter(self.config)

        return self

    def muter_ajouter_noeud(self):
        # Si il n'y a pas de liaisons, on arrete
        if not self.connexions:
            return

        # Trouver une connexion au hasard qui sera separee
        connexion_a_separer = choice(list(self.connexions.values()))

        #preparer le noeud a inserer
        nouvel_couche_noeud = self.noeuds[connexion_a_separer.entree].couche
        nouvel_id_noeud = self.nouvel_id_cache()
        ng = Gene.Noeud(nouvel_id_noeud, nouvel_couche_noeud,  'CACHE', activation=self.config.fonctions_activation.get_aleatoire())

        assert ng.ID not in self.noeuds
        self.noeuds[ng.ID] = ng

        nouvelle_conn_1, nouvelle_conn_2 = connexion_a_separer.separer(ng.ID)
        self.connexions[nouvelle_conn_1.cle] = nouvelle_conn_1
        self.connexions[nouvelle_conn_2.cle] = nouvelle_conn_2

        # Met a jour les couches des noeuds qui suivent le noeud ajoute
        self.decaler_couche_noeud(ng)

    def muter_ajouter_connection(self):
        ''' Tente de creer une connexion, en respectant les 2 regles :
            le noeud de sortie ne peut pas etre un noeud d'entree du reseau
            la connexion doit etre feed-forward '''

        entrees_possibles = [n for n in self.noeuds.values() if n.type != 'SORTIE']
        sorties_possibles = [n for n in self.noeuds.values() if n.type != 'ENTREE']

        noeud_entree = choice(entrees_possibles)
        noeud_sortie = choice(sorties_possibles)

        while noeud_sortie == noeud_entree:
            noeud_entree = choice(entrees_possibles)
            noeud_sortie = choice(sorties_possibles)

        # Creer la connexion seulement si elle est feed-forward et qu'elle n'existe pas deja
        if noeud_entree.couche <= noeud_sortie.couche : #la connexion doit etre feed-forward

            cle = (noeud_entree.ID, noeud_sortie.ID) #la connexion ne doit pas exister
            if cle not in self.connexions:

                poids = gauss(0, self.config.cri_distribution_poids_sigma)
                active = (True if random() > 0.5 else False)

                cg = Gene.Connexion(noeud_entree.ID, noeud_sortie.ID, poids, active)

                self.connexions[cg.cle] = cg

                if noeud_entree.couche == noeud_sortie.couche: #Si la connexion s'est faite dans la meme couche
                    #Alors on decale tout ce qui est lie au noeud de sortie
                    self.decaler_couche_noeud(noeud_sortie)

    def decaler_couche_noeud(self, noeud): #recursif
        if noeud.type == 'SORTIE':
            return
        else:
            noeud.couche += 1

            #on recupere les noeuds relies a ce noeud
            id_noeuds_suivants = []
            for c in self.connexions.keys():
                if c[0] == noeud:
                    id_noeuds_suivants.append(c[1])

            #on incremente leur couche
            for n_id in id_noeuds_suivants:
                self.decaler_couche_noeud(n)

    def muter_enlever_noeud(self):
        # Ne rien faire s'il n'y a pas de noeud cache
        if len(self.noeuds) <= self.nbr_entrees + self.nbr_sorties:
            return

        # On selectionne un noeud au hasard
        idx = None
        while 1:
            idx = choice(list(self.noeuds.keys()))
            if self.noeuds[idx].type == 'CACHE':
                break

        node = self.noeuds[idx]
        id_noeud = node.ID

        cles_a_supprimer = set()
        for cle, valeur in self.connexions.items():
            if id_noeud in (valeur.entree, valeur.sortie):
                cles_a_supprimer.add(cle)

        # On verifie qu'on ne supprime pas tous les genes de connexion
        if len(cles_a_supprimer) >= len(self.connexions):
            return

        for cle in cles_a_supprimer:
            del self.connexions[cle]

        del self.noeuds[idx]

        assert len(self.connexions) > 0
        assert len(self.noeuds) >= self.nbr_entrees + self.nbr_sorties

    def muter_enlever_connection(self):
        if len(self.connexions) > 1:
            cle = choice(list(self.connexions.keys()))
            del self.connexions[cle]

            assert len(self.connexions) > 0
            assert len(self.noeuds) >= self.nbr_entrees + self.nbr_sorties

    @classmethod
    def creer_connecte(cls, ID, config):

        g = Genome.creer_genome_deconnecte(ID, config)

        if g.config.cri_nbr_caches > 0:
            g.ajouter_noeuds_caches(g.config.cri_nbr_caches, 1)

        if g.config.cri_type_connexion == 'totale':
            g.connecter_entierement()
        elif g.config.cri_type_connexion == 'partielle':
            g.connecter_partiellement(g.config.cri_connexion_frac)

        return g

    @classmethod
    def creer_genome_deconnecte(cls, ID, config):

        c = cls(ID, config, None, None)

        noeud_id = 0
        for i in range(c.config.cri_nbr_entrees):
            assert noeud_id not in c.noeuds
            c.noeuds[noeud_id] = Gene.Noeud(noeud_id, 0, 'ENTREE', activation=c.config.fonctions_activation.get_aleatoire())
            noeud_id += 1
            c.nbr_entrees += 1

        for i in range(c.config.cri_nbr_sorties):
            noeud = Gene.Noeud(noeud_id, float('Inf'), 'SORTIE', activation=c.config.fonctions_activation.get_aleatoire())
            assert noeud.ID not in c.noeuds
            c.noeuds[noeud.ID] = noeud
            noeud_id += 1
            c.nbr_sorties += 1

        assert noeud_id == len(c.noeuds)
        return c

    def nouvel_id_cache(self):
        '''Renvoie le prochain ID pour creer un noeud cache'''
        nouvel_id = 0
        while nouvel_id in self.noeuds:
            nouvel_id += 1
        return nouvel_id

    def distance(self, autre_genome):

        if len(self.connexions) > len(autre_genome.connexions):
            conn_genes1 = self.connexions
            conn_genes2 = autre_genome.connexions

        else:
            conn_genes1 = autre_genome.connexions
            conn_genes2 = self.connexions

        # conn_genes1 est plus long que conn_genes2

        distance = 0

        if conn_genes1:  # Si il y a des connexions dans le genome 1

            N = len(conn_genes1)
            diff_poids = 0
            en_commun = 0  # compteur utilise pour faire une moyenne
            disjoints = 0
            exces = 0

            max_cg_genome2 = None
            if conn_genes2:
                max_cg_genome2 = max(itervalues(conn_genes2))

            # max_cg_genome2 va nous permettre de determiner les genes en exces dans le genome 1

            for k1, cg1 in iteritems(conn_genes1):
                if k1 in conn_genes2:
                    # genes homologue, on va mesurer la difference des poids
                    cg2 = conn_genes2[k1]
                    diff_poids += fabs(cg1.poids - cg2.poids)
                    en_commun += 1

                else:
                    if max_cg_genome2 is not None and cg1 > max_cg_genome2:
                        # on a un gene en exces
                        exces += 1
                    else:
                        # on a un gene disjoint
                        disjoints += 1

            disjoints += len(conn_genes2) - en_commun
            # on rajoute les genes disjoints dans le genome 2 (il ne peut pas y avoir de genes en exces dedans)

            # on calcule la distance
            distance += self.config.coefficient_exces * float(exces) / N
            distance += self.config.coefficient_disjoints * float(disjoints) / N
            if en_commun > 0:
                distance += self.config.coefficient_poids * (diff_poids / en_commun)

        return distance

    def __lt__(self, other):
        '''Classe les genomes par fitness.'''
        return self.fitness < other.fitness

    def __str__(self):
        s = 'Genome (id={0}, nbr noeuds={1}, nbr connexions={2})'.format(self.ID, len(self.noeuds), len(self.connexions))
        s += '\n'
        for n in self.noeuds.values():
            s += str(n)
            s += '\n'
        for c in self.connexions.values():
            s += str(c)
            s += '\n'
        return s
