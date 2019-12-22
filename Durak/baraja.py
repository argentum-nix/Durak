from naipe import Naipe
from random import shuffle

class Baraja(object):
    def __init__(self):
        self.naipes = []
        self.cantidad = 36
        self.calificaciones = ["Picas", "Corazones", "Tréboles", "Diamantes"]
        self.figuras = ["J", "Q", "K", "A"]
        self.crearBaraja()

    def mostarCartas(self):
        [carta.printNaipe() for carta in self.naipes]

    def barajar(self):
        shuffle(self.naipes)
        # self.mostarCartas() - imprime la baraja con shuffle

    def crearBaraja(self):
        for calif in self.calificaciones:
            [self.naipes.append(Naipe(calif, v)) for v in range(6, 11)]
            [self.naipes.append(Naipe(calif, l)) for l in self.figuras]
        self.barajar()

    def sacarDeBaraja(self):
        return self.naipes.pop()