from xml.etree.ElementTree import parse
import ReseauNeural.FonctionsActivation as FA


class Config:
    def __init__(self):

        # Configuration Reseau Initiale
        self.cri_nbr_entrees = None
        self.cri_nbr_sorties = None
        self.cri_nbr_caches = None
        self.cri_type_connexion = None
        self.cri_connexion_frac = None
        self.cri_distribution_poids = None
        self.cri_distribution_poids_sigma = None

        self.cri_poids = None

        # Parametres genetiques
        self.prob_muter_poids = 0
        self.prob_changer_poids = 0
        self.puissance_mutation_poids = 0
        self.poids_min = 0
        self.poids_max = 0
        self.prob_changer_etat_connexion = 0

        self.prob_muter_biais = 0
        self.puissance_mutation_biais = 0
        self.prob_muter_facteur = 0
        self.puissance_mutation_facteur = 0
        self.prob_muter_activation = 0

        self.prob_ajout_noeud = 0
        self.prob_enlever_noeud = 0
        self.prob_ajout_connexion = 0
        self.prob_enlever_connexion = 0

        # Fonctions Activation

        self.fonctions_activation = FA.FonctionActivationSet()

        # Coefficents pour le calcul de distance

        self.seuil_compatibilite = 0.0
        self.coefficient_poids = 0.0
        self.coefficient_exces = 0.0
        self.coefficient_disjoints = 0.0

    def parser_config_xml(self, chemin_fichier_config):
        tree = parse(chemin_fichier_config)
        racine = tree.getroot()

        cri = racine.find('config_reseau_initiale')
        self.cri_nbr_entrees = int(cri.find('nbr_entrees').text)
        self.cri_nbr_sorties = int(cri.find('nbr_sorties').text)
        self.cri_nbr_caches = int(cri.find('nbr_caches').text)
        self.cri_type_connexion = cri.find('type_connexion')[0].tag
        if self.cri_type_connexion == "partielle":
            self.cri_connexion_frac = float(cri.find('type_connexion')[0].attrib.values()[0])
        self.cri_distribution_poids = cri.find('distribution_poids')[0].tag
        if self.cri_distribution_poids == "gauss":
            self.cri_distribution_poids_sigma = float(cri.find('distribution_poids')[0].attrib.values()[0])

        fa = racine.find('fonctions_activation')
        for x in fa:
            if x.tag == 'sigmoid':
                self.fonctions_activation.add('sigmoid', FA.sigmoid_activation)
            elif x.tag == 'tanh':
                self.fonctions_activation.add('tanh', FA.tanh_activation)
            elif x.tag == 'sin':
                self.fonctions_activation.add('tanh', FA.sin_activation)
            elif x.tag == 'gauss':
                self.fonctions_activation.add('tanh', FA.gauss_activation)
            elif x.tag == 'relu':
                self.fonctions_activation.add('tanh', FA.relu_activation)
            elif x.tag == 'identity':
                self.fonctions_activation.add('tanh', FA.identity_activation)
            elif x.tag == 'inv':
                self.fonctions_activation.add('tanh', FA.inv_activation)
            elif x.tag == 'log':
                self.fonctions_activation.add('tanh', FA.log_activation)
            elif x.tag == 'exp':
                self.fonctions_activation.add('tanh', FA.exp_activation)
            elif x.tag == 'abs':
                self.fonctions_activation.add('tanh', FA.abs_activation)
            elif x.tag == 'hat':
                self.fonctions_activation.add('tanh', FA.hat_activation)
            elif x.tag == 'square':
                self.fonctions_activation.add('tanh', FA.square_activation)
            elif x.tag == 'cube':
                self.fonctions_activation.add('tanh', FA.cube_activation)

        # parametres genetiques
        pg = racine.find('parametres_genetiques')
        self.prob_muter_poids = float(pg.find('prob_muter_poids').text)
        self.prob_changer_poids = float(pg.find('prob_changer_poids').text)
        self.puissance_mutation_poids = float(pg.find('puissance_mutation_poids').text)
        self.poids_min = float(pg.find('poids_min').text)
        self.poids_max = float(pg.find('poids_max').text)
        self.prob_changer_etat_connexion = float(pg.find('prob_changer_etat_connexion').text)

        self.prob_muter_biais = float(pg.find('prob_muter_biais').text)
        self.puissance_mutation_biais = float(pg.find('puissance_mutation_biais').text)
        self.prob_muter_facteur = float(pg.find('prob_muter_facteur').text)
        self.puissance_mutation_facteur = float(pg.find('puissance_mutation_facteur').text)
        self.prob_muter_activation = float(pg.find('prob_muter_activation').text)

        self.prob_ajout_noeud = float(pg.find('prob_ajout_noeud').text)
        self.prob_enlever_noeud = float(pg.find('prob_enlever_noeud').text)
        self.prob_ajout_connexion = float(pg.find('prob_ajout_connexion').text)
        self.prob_enlever_connexion = float(pg.find('prob_enlever_connexion').text)

        # compatibilite genotypes

        cg = racine.find('compatibilite_genotypes')
        self.seuil_compatibilite = float(cg.find('seuil_compatibilite').text)
        self.coefficient_poids = float(cg.find('coeff_poids').text)
        self.coefficient_exces = float(cg.find('coeff_exces').text)
        self.coefficient_disjoints = float(cg.find('coeff_disjoints').text)

    def __str__(self):
        s = 'Config : \n'
        s += '- Nbr entrees : {0}, nbr sorties : {1}, nbr caches : {2} \n'.format(self.cri_nbr_entrees, self.cri_nbr_sorties, self.cri_nbr_caches)
        s += '- Type connexion : ' + self.cri_type_connexion
        if self.cri_type_connexion == "partielle":
            s += ' (fraction : {0}) \n'.format(self.cri_connexion_frac)
        s += '- Distribution de poids : ' + self.cri_distribution_poids
        if self.cri_distribution_poids == 'gauss':
            s += ' (sigma : {0}) \n'.format(self.cri_distribution_poids_sigma)
        s += '- Fonctions d\'activation : \n'
        for f in self.fonctions_activation.fonctions.keys():
            s += '    - {0}\n'.format(f)
        return s




