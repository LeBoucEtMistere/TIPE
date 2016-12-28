import Gene

from random import shuffle, gauss


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

    def ajouter_noeud_cache(self):
        nouvel_id = self.nouvel_id_cache()
        self.noeuds[nouvel_id] = Gene.Noeud(nouvel_id, 'CACHE', self.config.fonctions_activation.get_aleatoire())
        self.nbr_caches += 1

    def ajouter_noeuds_caches(self, nbr):
        id_noeud = self.nouvel_id_cache()
        for i in range(nbr):
            noeud = Gene.Noeud(id_noeud, 'CACHE', self.config.fonctions_activation.get_aleatoire())
            assert noeud.ID not in self.noeuds
            self.noeuds[noeud.ID] = noeud
            id_noeud += 1
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
            cg = Gene.Connexion(input_id, output_id, poids, True, Gene.Connexion.nouveau_num_innov())
            self.connexions[cg.cle] = cg

    def connecter_partiellement(self, fraction):
        assert 0 <= fraction <= 1
        toutes_connexions = self.calculer_toutes_connexions()
        shuffle(toutes_connexions)
        nbr_a_ajouter = int(round(len(toutes_connexions) * fraction))
        for id_entree, id_sortie in toutes_connexions[:nbr_a_ajouter]:
            poids = gauss(0,self.config.cri_distribution_poids_sigma)
            cg = Gene.Connexion(id_entree, id_sortie, poids, True, Gene.Connexion.nouveau_num_innov())
            self.connexions[cg.cle] = cg

    @classmethod
    def creer_connecte(cls, ID, config):

        g = Genome.creer_genome_deconnecte(ID, config)

        if g.config.cri_nbr_caches > 0:
            g.ajouter_noeuds_caches(g.config.cri_nbr_caches)

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
            c.noeuds[noeud_id] = Gene.Noeud(noeud_id, 'ENTREE', c.config.fonctions_activation.get_aleatoire())
            noeud_id += 1
            c.nbr_entrees += 1

        for i in range(c.config.cri_nbr_sorties):
            noeud = Gene.Noeud(noeud_id, 'SORTIE', c.config.fonctions_activation.get_aleatoire())
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



