import pygame
import sys_tools as st
from naipe import Naipe

# recibe una img extra, "activa", si la imagen debe cambiar.
# pensar en que jackets de los AI's se ponen azules al estar activos.
'''
class BotonCarta():
|
|
'''

class BotonCarta():
    def __init__(self, x, y, width, height, nombre, activa, enabled):

        self.imagen = pygame.image.load(
            st.current_dir() + "/data/cards/{}".format(nombre)).convert_alpha()
        self.imagen = pygame.transform.scale(self.imagen, (width, height))

        if activa != False:
            self.imagen_activa = pygame.image.load(
                st.current_dir() + "/data/cards/{}".format(activa)).convert_alpha()
            self.imagen_activa = pygame.transform.scale(
                self.imagen_activa, (width, height))

        self.imagen_inactiva = self.imagen

        self.u1 = pygame.Rect(x, y, width, height)

        self.long = x

        self.tall = y

        self.tall_aux = y

        self.enabled = enabled

        self.name = nombre
    '''
    mouseOverButton(self, mode, h)
    |   Función que se usa para "subir" las cartas del usuario, 
    |   en el caso de que sea su turno de defenderse o atacar,y
    |   además, de que sean cartas posibles de usar y el 
    |   usuario tenga su mouse sobre ella.

    '''

    def mouseOverButton(self, mode, h):
        if self.enabled == True:
            # mover la carta hacia arriba
            if mode:
                self.tall = h
            else:
                self.tall = self.tall_aux

    '''
    isActivePlayer(self, param)
    |   Cambia la imagen asociada al botón por la segúnda asocidada,
    |   en caso de que el boton la tenga.
    '''

    def isActivePlayer(self, param):
        if param:
            self.imagen = self.imagen_activa
        else:
            self.imagen = self.imagen_inactiva
    '''
    getRekt(self)
    |   Función tipo get, que retorna el objeto Rect() del botón.
    '''

    def getRekt(self):
        return self.u1
    '''
    getImg(self)
    |   Función tipo get, que retorna la imagen, asociada al botón.
    '''

    def getImg(self):
        return self.imagen
    '''
    getX(self)
    |   Función tipo get, que retorna el ancho del botón.
    '''

    def getX(self):
        return self.long
    '''
    getY(self)
    |   Función tipo get, que retorna la altura del botón.
    '''

    def getY(self):
        return self.tall
    '''
    makeNaipe(self)
    |   Función que se usa para crear un naipe, el cual sera
    |   retornado cuando el usuario haga el click en la carta
    |   que quiere jugar.
    '''

    def makeNaipe(self):
        if self.name == "NULL.png":
            return Naipe("Null", 0)
        if self.name[0] == "C":
            calificacion = "Corazones"
        elif self.name[0] == "D":
            calificacion = "Diamantes"
        elif self.name[0] == "P":
            calificacion = "Picas"
        else:
            calificacion = "Tréboles"

        if len(self.name) == 7:
            rank = self.name[2]
        else:
            rank = "{}{}".format(self.name[2], self.name[3])

        return Naipe(calificacion, int(rank))
