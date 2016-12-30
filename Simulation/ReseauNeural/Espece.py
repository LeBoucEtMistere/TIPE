from random import choice


class Espece:
    """ Regroupement d'individus genetiquement similaires."""

    def __init__(self, representant, ID):
        assert type(ID) == int
        self.representant = representant
        self.ID = ID
        self.age = 0
        self.membres = []

        self.ajouter(representant)

    def ajouter(self, individu):
        self.membres.append(individu)
        individu.espece_id = self.ID


class SetEspece:
    """ Encapsule le schema de speciation et stocke les especes. """

    def __init__(self, config):
        self.config = config
        self.especes = []
        self.nbr_espece = 0

    def speciation(self, population):

        for individu in population:
            # Trouver l'espece qui a le representant le plus proche
            distance_min = None
            plus_proche_espece = None
            for s in self.especes:
                distance = individu.distance(s.representant)
                if distance < self.config.seuil_compatibilite and (distance_min is None or distance < distance_min):
                    plus_proche_espece = s
                    distance_min = distance

            if plus_proche_espece is not None:
                plus_proche_espece.ajouter(individu)
            else:
                # Aucune espece n'est assez proche, on doit en creer une nouvelle pour l'individu
                self.especes.append(Espece(individu, self.nbr_espece))
                self.nbr_espece += 1

        # On supprime les especes vides d'individus
        self.especes = [s for s in self.especes if s.membres]

        # On choisi un individu au hasard en tant que nouveau representant de l'espece
        for s in self.especes:
            s.representant = choice(s.membres)
