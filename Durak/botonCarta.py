import pygame
import sys_tools as st
import text_tools as tt 
from naipe import Naipe

# recibe una img extra, "activa", si la imagen debe cambiar.
# pensar en que jackets de los AI's se ponen azules al estar activos.


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


    def mouseOverButton(self, mode, h):
        if self.enabled == True:
            #mover la carta hacia arriba
            if mode:
                self.tall = h
            else:
                self.tall = self.tall_aux
        else:
            #nada lol
            pass
            print("No se puede utilizar la carta seleccionada.")

    # se usara para cambiar de jacket para los jugadores NPC
    # y en menu
    def isActivePlayer(self, param):
        if param:
            self.imagen = self.imagen_activa
        else:
            self.imagen = self.imagen_inactiva

    def turnOffBoton(self):
        self.enabled = False

    def turnOnBoton(self):
        self.enabled = True

    def getRekt(self):
        return self.u1

    def getImg(self):
        return self.imagen

    def getX(self):
        return self.long

    def getY(self):
        return self.tall

    def getNombre(self):
        return self.name

    def makeNaipe(self):
        # Se usa para crear un naipe, el cual sera retornado cuando el usuario haga click 
        # en la carta que quiere jugar
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

