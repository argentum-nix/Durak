import pygame
import sys_tools as st

'''
class Naipe
 |  Clase, que modela el comportamiento de naipe inglés.
 |  Cada naipe tiene dos parametros : valor y pinta 
 |  (calificación). Los valores parten de 6 y terminan en 14 (A's),
 |  dado que en durak para 6 personas se juega con baraja de 36 cartas,
 |  con 6 como valor más chico.
'''


class Naipe:
    def __init__(self, calificacion, valor):
        self.calificacion = calificacion
        self.valor = valor
        # Valor numérico, de 6 a 14.
    '''
    isTrump(self, trumpSuit)
    |   Función, que revisa, cual de las pintas es de triunfo.
    '''

    def isTrump(self, trumpSuit):
        if self.calificacion == trumpSuit:
            return True
        else:
            return False
    '''
    printNaipe(self)
    |  Función, que, basado en calificación de naipe, retorna 
    |  un string de tipo "valor" de "pinta".
    '''

    def printNaipe(self):
        if self.valor == 11:
            return "J de {}".format(self.calificacion)
        elif self.valor == 12:
            return "Q de {}".format(self.calificacion)
        elif self.valor == 13:
            return "K de {}".format(self.calificacion)
        elif self.valor == 14:
            return "A de {}".format(self.calificacion)
        else:
            return "{} de {}".format(self.valor, self.calificacion)
    '''
    fileNaipe(self)
    |   Función, que retorna nombre de la carta, en formato 
    |   {Pinta}_{numero}. Este nombre corresponde al nombre de imagen
    |   de cada carta, presente de data/cards.
    '''

    def fileNaipe(self):
        if self.calificacion == "Picas":
            return "P_{}.png".format(self.valor)

        elif self.calificacion == "Corazones":
            return "C_{}.png".format(self.valor)

        elif self.calificacion == "Tréboles":
            return "T_{}.png".format(self.valor)
        elif self.calificacion == "Diamantes":
            return "D_{}.png".format(self.valor)
        else:
            return "NULL.png"
    '''
    valorNaipe(self)
    |   Función de tipo get. Retorna el valor de la naipe.
    '''

    def valorNaipe(self):
        return self.valor
    '''
    calificacionNaupe(self)
    |   Función de tipo get. Retorna la calificación.
    '''

    def calificacionNaipe(self):
        return self.calificacion

    '''
    getImgNaipe(self, w, h)
    |   Retorna la imagen del naipe, según los parametros w (ancho) y h (altura).
    |   Se ocupa para mostrar las cartas en la pantalla.
    '''

    def getImgNaipe(self, w, h):
        imagen = pygame.image.load(st.current_dir() +
                                   "/data/cards/{}".format(self.fileNaipe())).convert_alpha()
        imagen = pygame.transform.scale(imagen, (w, h))
        return imagen
