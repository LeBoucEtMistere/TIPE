import FonctionsActivation


class Noeud(object):
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

    def __str__(self):
        return 'Noeud(id={0}, type={1}, biais={2}, facteur={3} activation={4})'.format(self.ID, self.type, self.biais, self.facteur, self.activation)


class Connexion(object):
    """
    Cette classe represente un gene de type connexion

    :argument
    entree(int) : Noeud d'entree
    sortie(int) : Noeud de sortie
    poids(float) : le poids de la liaison
    actif(bool) : le statut du gene
    innovation(int) : le numero d'innovation
    """
    def __init__(self, entree, sortie, poids, actif, innovation):

        assert type(entree) is int
        assert type(sortie) is int
        assert type(poids) is float
        assert type(actif) is bool
        self.entree = entree
        self.sortie = sortie
        self.poids = poids
        self.actif = actif
        self.innovation = innovation

        # utilise dans les comparaisons, pour les tris dans les dictionnaires
        self.cle = (self.entree, self.sortie)

    def __lt__(self, autreConnexion):
        return self.cle < autreConnexion.cle

    def __str__(self):
        return 'connexion({0} -> {1} , poids={2}, activee={3}, innovation={4})'.format(self.entree, self.sortie, self.poids, self.actif, self.innovation)

    innovation_num = 0

    @staticmethod
    def nouveau_num_innov():
        '''Renvoie le prochain numero d'innovation'''
        Connexion.innovation_num += 1
        return Connexion.innovation_num - 1

