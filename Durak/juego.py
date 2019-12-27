import pygame
import os
from random import shuffle
import random
import shutil

import sys_tools as st
import text_tools as tt

from baraja import Baraja
from naipe import Naipe
from jugador import Jugador, JugadorCPU, JugadorHumano
from botonCarta import BotonCarta


class Juego(st.Estados_Juego):
    def __init__(self, nJugadores):

        st.Estados_Juego.__init__(self)
        self.nJugadores = nJugadores
        # Crea a los n jugadores (incluyendo al usuario como jugador 0) y los guarda en una lista
        self.jugadores = self.crearJugadores(nJugadores)
        self.next = "MENU"
        self.st_done = False

        self.baraja = Baraja()  # Crea la baraja para la partida
        self.repartirCartas()
        # Muestra la primera carta de la baraja para conseguir el trump
        self.trump = self.getTrump()

        self.jugadorActual = -1  # Almacena el indice del jugador actual
        self.atacantes = []
        self.cartasJugadas = {"ataque": [], "defensa": []}

        # u1, u2 y u3 son las 3 cartas visibles del usuario

        # Retorna una lista con 3 o menos elementos de la mano del jugador (funciona con slicing)
        self.listpos = 0
        self.manoVisible = self.jugadores[0].manoAcotada(listpos)

        # Lista con el nombre de los archivos de las imagenes correspondientes para cada carta en manoVisible
        self.imagesName = self.getImagesName()

        self.manoHumano = self.buildHand()
        self.u1 = self.manoHumano[0]  # primera carta
        self.u2 = self.manoHumano[1]  # segunda carta
        self.u3 = self.manoHumano[2]  # tercera carta

        # genera posiciones para cartas fijas, y crea lista de botones no interactivos
        # que corresponden a los jugadores AI de 1 a 5
        self.pos = [(20, 200), (20, 20), (369, 20), (700, 20), (700, 200)]
        self.bot_ai = list(map(lambda i: BotonCarta(
            self.pos[i][0], self.pos[i][1], 70, 103, "Grey_1.png", "Blue_1.png", False), [i for i in range(5)]))

        # t1 es la carta trump
        self.t1 = BotonCarta(100, 400, 50, 67, self.trump.fileNaipe(), False, False)

        #para desplazarse en la lista
        self.arrow_up = BotonCarta(700,200,30,40,st.current_dir + "/data/icon/up.png", False, False)
        self.arrow_down = BotonCarta(700,200,30,40,st.current_dir + "/data/icon/down.png", False, False)
        self.arrows = list(arrow_up,arrow_down)
      
    def crearJugadores(self, nJugadores):
        jugadores = [JugadorCPU() for id in range(1, nJugadores)]
        jugadores.append(JugadorHumano())
        jugadores.reverse()  # Jugador humano siempre en indice 0
        return jugadores

    def repartirCartas(self):  # Repartir cartas al inicio de la partida
        repartir = False
        for i in range(len(self.jugadores)):
            if self.baraja.mostrarCantidad() > 0:
                if self.jugadores[i].mostrarCantidad() < 6:
                    repartir = True
                    self.jugadores[i].sacarCarta(self.baraja.sacarDeBaraja())
            else:
                repartir = False

        if repartir == True:
            self.repartirCartas()


    def getTrump(self):
        if self.nJugadores >= 6:  # Si son 6 jugadores, no quedaran cartas en la baraja despues de repartir
            return self.baraja.sacarTrumpCon6Jugadores()
        else:
            return self.baraja.sacarTrump()

    # test, debug de consola
    def mostrarInfo(self):
        print("hay " + str(len(self.jugadores)) + "jugadores")
        print("Manos:")
        i = 0
        for jugador in self.jugadores:
            print("player " + str(i))
            jugador.mostrarMano()
            print("\n")
            i += 1
        print("trump:")
        self.trump.printNaipe()

    def getImagesName(self):
        return [carta.fileNaipe() for carta in self.manoVisible]

    def buildHand(self):
        x = 267
        y = 370
        w = 70
        h = 103
        manoHumano = []
        for img in self.imagesName:
            manoHumano.append(BotonCarta(x, y, w, h, img, False, True))
            x += 102
        while len(manoHumano) != 3:
            manoHumano.append(BotonCarta(x, y, w, h, "NULL.png", False, True))
            x += 102
        return manoHumano

    def clean(self):
        pass

    def get_event(self, event, keys):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.arrow_up.getRekt().collidepoint(pygame.mouse.get_pos()):
                self.listpos += 1 #!!!!agregar una funcion para hacer esto, para que revise rango de lista, hasta 6
                self.manoVisible = self.jugadores[0].manoAcotada(self.listpos)

            if self.arrow_down.getRekt().collidepoint(pygame.mouse.get_pos()):
                self.listpos -= 1
                self.manoVisible = self.jugadores[0].manoAcotada(listpos)

            if self.u1.getRekt().collidepoint(pygame.mouse.get_pos()):
                self.st_done = True
                #self.next = "CARTA_1"  # F

            if self.u2.getRekt().collidepoint(pygame.mouse.get_pos()):
                self.st_done = True
                #self.next = "CARTA_2"  # F, cuando haya combate, vincular a esa funcion

            if self.u3.getRekt().collidepoint(pygame.mouse.get_pos()):
                self.st_done = True
                #self.next = "CARTA_3"  # F, same as 2

        elif event.type == pygame.QUIT:
            self.quit = True
            pygame.quit()
            quit()


    def mostrarTrump(self, screen):
        trumpImg = self.t1.getImg()
        trump_text = tt.render_text(
            "T", "Trump: " + self.trump.printNaipe(), self.white)
        screen.blit(trump_text, (self.t1.getX() - 65, self.t1.getY() - 18))
        screen.blit(trumpImg, (self.t1.getX(), self.t1.getY()))


    def mostrarCantidadNaipes(self, screen, listaTextos):
        screen.blit(listaTextos[0],
                    (self.u2.getX() + 33, self.u2.getY() + 107))
        list(map(lambda i: screen.blit(listaTextos[i + 1], (self.bot_ai[i].getX(
        ) + 33, self.bot_ai[i].getY() + 107)), [i for i in range(5)]))

    def mostrarOponentes(self, screen):
        list(map(lambda i: screen.blit(self.bot_ai[i].getImg(), (self.bot_ai[i].getX(), self.bot_ai[i].getY())), [i for i in range(5)]))


    def render(self, clock, screen, p):
        screen.fill(self.background_color)

        # Prepara para dibujar

        # Mano del humano muestra 3 cartas
        carta1 = self.u1.getImg()
        carta2 = self.u2.getImg()
        carta3 = self.u3.getImg()

        cant_Textos = list(map(lambda i: tt.render_text("T", str(
            self.jugadores[i].mostrarCantidad()), self.white), [i for i in range(1, 6)]))
        cant_Textos.insert(0, tt.render_text(
            "S", str(self.jugadores[0].mostrarCantidad()), self.white))

        while not self.st_done:
            # Dibuja las manos de los jugadores
            screen.blit(carta1, (self.u1.getX(), self.u1.getY()))
            screen.blit(carta2, (self.u2.getX(), self.u2.getY()))
            screen.blit(carta3, (self.u3.getX(), self.u3.getY()))

            self.mostrarOponentes(screen)
            # Debajo de cada carta, se imprime la cantidad de naipes de cada jugador.
            self.mostrarCantidadNaipes(screen, cant_Textos)
            # Muestra la trump
            self.mostrarTrump(screen)
            

            pygame.display.update()
            carta1 = self.u1.getImg()
            carta2 = self.u2.getImg()
            carta3 = self.u3.getImg()

            [self.get_event(event, pygame.key.get_pressed())
             for event in pygame.event.get()]
