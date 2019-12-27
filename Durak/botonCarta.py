import pygame
import sys_tools as st
import text_tools as tt


class BotonCarta():
    def __init__(self, x, y, width, height, nombre, enabled):

        self.imagen = pygame.image.load(st.current_dir() + "/data/cards/{}".format(nombre)).convert_alpha()

        self.b1 = pygame.Rect(x, y, width, height)

        self.long = x

        self.tall = y

        self.imagen =  pygame.transform.scale(self.imagen, (width, height))

        self.enabled = enabled



    def isPressed(self, event):
        if self.enabled == True:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    print("me estan clickeando")
                    return True
        else:
            print("No se puede utilizar la carta seleccionada.")
        
        return False

    def turnOffBoton(self):
        self.enabled = False

    def turnOnBoton(self):
        self.enabled = True
    
    def getRekt(self):
        return self.b1
    
    def getImg(self):
        return self.imagen
    
    def getX(self):
        return self.long
    
    def getY(self):
        return self.tall