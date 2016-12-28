import Genome


class Reseau(object):
    def __init__(self, nbr_noeud, entrees, sorties, noeud_eval):
        self.noeud_eval = noeud_eval
        self.noeuds_entree = entrees
        self.noeuds_sortie = sorties
        self.valeurs = [0.0] * (1 + nbr_noeud)

    def activer(self, entrees):
        if len(self.noeuds_entree) != len(entrees):
            raise Exception("Entrees obtenues : {0} , entrees attendues : {1}".format(len(self.noeuds_entree), len(entrees)))

        for i, v in zip(self.noeuds_entree, entrees):
            self.valeurs[i] = v

        for noeud, fonc, biais, facteur, entrees in self.noeud_eval:
            s = 0.0
            for i, w in entrees:
                s += self.valeurs[i] * w
            self.valeurs[noeud] = fonc(biais + facteur * s)

        return [self.valeurs[i] for i in self.noeuds_sortie]


def trouver_couches_FF(entrees, connexions):
    '''
    Collecte les couches dont les membres peuvent etre evalues en parallele dans un reseau feed forward.
    :param entrees: liste des noeuds d'entree du reseau
    :param connexions: liste des (entrees, sorties) connexions dans le reseau.
    retourne une liste de couches, avec chaque couche constituee d'un set d'ID de noeuds
    '''

    couches = []
    S = set(entrees)
    while 1:
        # Trouver les noeuds candidats C pour la prochaine couche.
        # Ces noeuds doivent connecter un noeud dans S et un noeud qui n'est pas dans S.
        C = set(b for (a, b) in connexions if a in S and b not in S)
        # Garder seulement les noeuds dont toutes les entrees sont contenues dans S
        T = set()
        for n in C:
            if all(a in S for (a, b) in connexions if b == n):
                T.add(n)
        if not T:
            break
        couches.append(T)
        S = S.union(T)
    return couches

def creer_phenotype(genome):
    """ Recoie un genome et renvoie son phenotype, un reseau de neurone feed forward. """

    # Liste des noeuds et des connections actives
    noeuds_entree = [ng.ID for ng in genome.noeuds.values() if ng.type == 'ENTREE']
    noeuds_sortie = [ng.ID for ng in genome.noeuds.values() if ng.type == 'SORTIE']
    connexions = [(cg.entree, cg.sortie) for cg in genome.connexions.values() if cg.actif]

    couches = trouver_couches_FF(noeuds_entree, connexions)
    noeuds_eval = []
    noeuds_utilises = set(noeuds_entree + noeuds_sortie)
    for couche in couches:
        for noeud in couche:
            entrees = []
            for cg in genome.connexions.values():
                if cg.sortie == noeud and cg.actif:
                    entrees.append((cg.entree, cg.poids))
                    noeuds_utilises.add(cg.entree)

            noeuds_utilises.add(noeud)
            ng = genome.noeuds[noeud]
            noeuds_eval.append((noeud, ng.activation, ng.biais, ng.facteur, entrees))

    return Reseau(max(noeuds_utilises), noeuds_entree, noeuds_sortie, noeuds_eval)



