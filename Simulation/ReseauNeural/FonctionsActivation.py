import math
from random import choice


def sigmoid_activation(z):
    z = max(-60.0, min(60.0, z))
    return 1.0 / (1.0 + math.exp(-z))


def tanh_activation(z):
    z = max(-60.0, min(60.0, z))
    return math.tanh(z)


def sin_activation(z):
    z = max(-60.0, min(60.0, z))
    return math.sin(z)


def gauss_activation(z):
    z = max(-60.0, min(60.0, z))
    return math.exp(-0.5 * z**2) / math.sqrt(2 * math.pi)


def relu_activation(z):
    return z if z > 0.0 else 0


def identity_activation(z):
    return z


def clamped_activation(z):
    return max(-1.0, min(1.0, z))


def inv_activation(z):
    if z == 0:
        return 0.0

    return 1.0 / z


def log_activation(z):
    z = max(1e-7, z)
    return math.log(z)


def exp_activation(z):
    z = max(-60.0, min(60.0, z))
    return math.exp(z)


def abs_activation(z):
    return abs(z)


def hat_activation(z):
    return max(0.0, 1 - abs(z))


def square_activation(z):
    return z ** 2


def cube_activation(z):
    return z ** 3


class FonctionActivationInvalide(Exception):
    pass


class FonctionActivationSet(object):
    def __init__(self):
        self.fonctions = {}

    def add(self, nomConfig, fonction):
        self.fonctions[nomConfig] = fonction

    def get(self, nomConfig):
        f = self.fonctions.get(nomConfig)
        if f is None:
            raise FonctionActivationInvalide("Cette fonction d'activation n'existe pas : {0!r}".format(nomConfig))

        return f

    def get_aleatoire(self):
        return self.fonctions.get(choice(self.fonctions.keys()))

    def is_valid(self, nomConfig):
        return nomConfig in self.fonctions

