from naipe import Naipe
from random import shuffle


class Baraja:
    def __init__(self):
        self.naipes = []
        self.calificaciones = ["Picas", "Corazones", "Tréboles", "Diamantes"]
        self.crearBaraja()
        # Si son 6 jugadores, no quedaran cartas en la baraja despues de repartir
        self.trumpPara6 = self.naipes[0]

    def mostarCartas(self):
        [carta.printNaipe() for carta in self.naipes]

    def mostrarCantidad(self):
        return len(self.naipes)

    def barajar(self):
        shuffle(self.naipes)
        # self.mostarCartas() - imprime la baraja con shuffle

    def crearBaraja(self):
        for calif in self.calificaciones:
            [self.naipes.append(Naipe(calif, v)) for v in range(6, 15)]
        self.barajar()
        self.cantidad = len(self.naipes)

    def sacarDeBaraja(self):
        return self.naipes.pop()

    def sacarTrump(self):  # trump es la carta que queda arriba de la baraja despues de repartir las 6 cartas de cada jugador
        trump = self.naipes.pop()  # saca la carta del top de la baraja
        self.naipes.reverse()
        self.naipes.append(trump)  # coloca la carta al comienzo de la baraja
        self.naipes.reverse()
        return trump  # retorna la carta trump que ahora esta al inicio de la baraja

    # trump es la carta que queda arriba de la baraja despues de repartir las 6 cartas de cada jugador
    def sacarTrumpCon6Jugadores(self):
        return self.trumpPara6
