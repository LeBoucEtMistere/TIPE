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

        # Fonctions Activation

        self.fonctions_activation = FA.FonctionActivationSet()

    def parser_config(self, chemin_fichier_config):
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




