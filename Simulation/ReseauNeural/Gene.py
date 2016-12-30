import FonctionsActivation
from random import random, gauss

class Noeud(object):
    #TODO reproduction
    """
    Cette classe represente un gene de type Noeud

    :argument
    ID(int) : un ID unique
    type : au choix parmi ["entree", "sortie", "cache"]
    activation : la fonction d'activation du noeud

    """
    def __init__(self, ID, type, biais=0.0, facteur=4.924273, activation=FonctionsActivation.sigmoid_activation):
        assert type in ('ENTREE', 'SORTIE', 'CACHE')
        self.ID = ID
        self.type = type
        self.biais = biais
        self.facteur = facteur
        self.activation = activation

    def muter_biais(self, config):
        nouveau_biais = self.biais + gauss(0, 1) * config.puissance_mutation_biais
        self.biais = max(config.poids_min, min(config.poids_max, nouveau_biais))

    def muter_facteur(self, config):
        nouveau_facteur = self.facteur + gauss(0, 1) * config.puissance_mutation_facteur
        self.facteur = max(config.poids_min, min(config.poids_max, nouveau_facteur))

    def muter_activation(self, config):
        self.activation = config.fonctions_activation.get_aleatoire()

    def muter(self, config):
        if random() < config.prob_muter_biais:
            self.muter_biais(config)
        if random() < config.prob_muter_facteur:
            self.muter_facteur(config)
        if random() < config.prob_muter_activation:
            self.muter_activation(config)

    def __str__(self):
        return 'Noeud(id={0}, type={1}, biais={2}, facteur={3} activation={4})'.format(self.ID, self.type, self.biais, self.facteur, self.activation)

class Connexion(object):
    #TODO reproduction / division en deux connexions
    """
    Cette classe represente un gene de type connexion

    :argument
    entree(int) : Noeud d'entree
    sortie(int) : Noeud de sortie
    poids(float) : le poids de la liaison
    actif(bool) : le statut du gene
    innovation(int) : le numero d'innovation
    """
    def __init__(self, entree, sortie, poids, actif):

        assert type(entree) is int
        assert type(sortie) is int
        assert type(poids) is float
        assert type(actif) is bool
        self.entree = entree
        self.sortie = sortie
        self.poids = poids
        self.actif = actif

        # utilise dans les comparaisons, pour les tris dans les dictionnaires
        # sert aussi de numero d'innovation (le couple est unique pour chaque innovation)
        self.cle = (self.entree, self.sortie)

    def muter(self, config):
        if random() < config.prob_muter_poids:
            if random() < config.prob_changer_poids:
                # Remplace le poids avec une valeur aleatoire
                self.poids = gauss(0, config.cri_distribution_poids_sigma)
            else:
                # perturbe le poids
                nouveau_poids = self.poids + gauss(0, 1) * config.puissance_mutation_poids
                self.poids = max(config.poids_min, min(config.poids_max, nouveau_poids))

        if random() < config.prob_changer_etat_connexion:
            self.actif = not self.actif

    def activer(self):
        self.actif = True

    def est_meme_innovation(self, autre):
        return self.cle == autre.cle

    def __lt__(self, autre_connexion):
        return self.cle < autre_connexion.cle

    def __str__(self):
        return 'connexion({0} -> {1} , poids={2}, activee={3}, innovation={4})'.format(self.entree, self.sortie, self.poids, self.actif, self.innovation)

