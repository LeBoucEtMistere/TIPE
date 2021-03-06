import FonctionsActivation
from random import random, gauss

class Noeud(object):
    """
    Cette classe represente un gene de type Noeud

    :argument
    ID(int) : un ID unique
    type : au choix parmi ["entree", "sortie", "cache"]
    activation : la fonction d'activation du noeud

    """
    def __init__(self, ID, couche, type, biais=0.0, facteur=4.924273, activation=FonctionsActivation.sigmoid_activation):
        assert type in ('ENTREE', 'SORTIE', 'CACHE')
        self.ID = ID
        self.couche = couche
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

    def reproduire_avec(self, autre):
        """ Retourne un nouveau Noeud possedant les caracteres de ses 2 parents choisis aleatoirement."""

        biais = self.biais if random() > 0.5 else autre.biais
        facteur = self.facteur if random() > 0.5 else autre.facteur
        activation = self.activation if random() > 0.5 else autre.activation

        return Noeud(self.ID, self.couche, self.type, biais, facteur, activation)

    def copier(self):
        return Noeud(self.ID, self.couche, self.type, self.biais, self.facteur, self.activation)

    def __str__(self):
        return 'Noeud(id={0}, couche={1}, type={2}, biais={3}, facteur={4} activation={5})'.format(self.ID, self.couche, self.type, self.biais, self.facteur, self.activation)


class Connexion(object):
    """
    Cette classe represente un gene de type connexion

    :argument
    entree(int) : Noeud d'entree
    sortie(int) : Noeud de sortie
    poids(float) : le poids de la liaison
    actif(bool) : le statut du gene
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

    def separer(self, id_noeud):
        """ Separe une connexion, en cree deux autres, et desactive l'originale """
        self.actif = False

        nouvelle_connexion_1 = Connexion(self.entree, id_noeud, 1.0, True)
        nouvelle_connexion_2 = Connexion(id_noeud, self.sortie, self.poids, True)

        return nouvelle_connexion_1, nouvelle_connexion_2

    def reproduire_avec(self, autre):
        """ Retourne une nouvelle connexion possedant les caracteres de ses 2 parents choisis aleatoirement."""
        assert (self.cle == autre.cle)  # on doit avoir le meme numero d'innovation

        poids = self.poids if random() > 0.5 else autre.poids
        actif = self.actif if random() > 0.5 else autre.actif

        return Connexion(self.entree, self.sortie, poids, actif)

    def copier(self):
        return Connexion(self.entree, self.sortie, self.poids, self.actif)

    def __lt__(self, autre_connexion):
        return self.cle < autre_connexion.cle

    def __str__(self):
        return 'connexion({0} -> {1} , poids={2}, activee={3}, cle_innovation={4})'.format(self.entree, self.sortie, self.poids, self.actif, self.cle)

