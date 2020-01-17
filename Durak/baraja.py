from naipe import Naipe
from random import shuffle

'''
class Baraja
 |  Clase, que simula el comportamiento de una
 |  baraja de naipes ingleses. Además, en la baraja
 |  siempre existe una carta de triunfo - la pinta, que
 |  gana a cualquier otra.
'''


class Baraja:
    def __init__(self):
        self.naipes = []
        self.calificaciones = ["Picas", "Corazones", "Tréboles", "Diamantes"]
        self.crearBaraja()
        self.trumpPara6 = self.naipes[0]
    '''
    mostrarCantidad(self)
    |   Función, que analiza los eventos de juego. Al cerrar la ventana (ESC),
    |   el evento corresponde a pygame.QUIT y se termina la ejecución del código.
    |   En caso de presionar cualquier botón, el jugador acceda al menu.
    '''

    def mostrarCantidad(self):
        return len(self.naipes)
    '''
    barajar(self)
    |   Función, que baraja los naipes, usando el modulo 
    |   random y su función shuffle.
    '''

    def barajar(self):
        shuffle(self.naipes)
    '''
    crearBaraja(self)
    |   Función, que analiza los eventos de juego. Al cerrar la ventana (ESC),
    |   el evento corresponde a pygame.QUIT y se termina la ejecución del código.
    |   En caso de presionar cualquier botón, el jugador acceda al menu.
    |   CONCEPTOS DE CURSO: Comprensión de listas.
    '''

    def crearBaraja(self):
        for calif in self.calificaciones:
            [self.naipes.append(Naipe(calif, v)) for v in range(6, 15)]
        self.barajar()
        self.cantidad = len(self.naipes)
    '''
    sacarDeBaraja(self)
    |  Saca una naipe de la baraja, usando función pop()
    '''

    def sacarDeBaraja(self):
        return self.naipes.pop()
    '''
    sacarTrump(self)
    |  Función, que permita sacar la carta de triunfo. Dado que esta queda 
    |  arriba de la baraja despues de repartir de 6 cartas, se reversa el orden y se 
    |  coloca la trump al inicio de la baraja. La función retorna la carta de triunfo.
    '''

    def sacarTrump(self):
        trump = self.naipes.pop()
        self.naipes.reverse()
        self.naipes.append(trump)
        self.naipes.reverse()
        return trump
    '''
    sacarTrumpCon6Jugadores(self)
    |   Función de tipo get() que retorna la carta de triunfo para baraja, que se 
    |   reparte entre 6 jugadores por defecto.
    '''

    def sacarTrumpCon6Jugadores(self):
        return self.trumpPara6
