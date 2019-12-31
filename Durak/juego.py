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
        self.trump = self.makeTrump()
        self.w = 70
        self.h = 103

        # Se tienen dos identificadores de jugador para no perder el orden de turno al realizar ataques/defensas

        #* Estos valores son "estaticos", solo cambian al finalizar la ronda de ataques
        self.jugadorActivo = -1 # Indice del jugador al que le corresponde el turno original 
        self.defensor = -1 # Indice del jugador al que le corresponde defender

        self.atacante = -1  # Indice del jugador al que le corresponde el turno para atacar
        self.atacantes = [] # Almacena a los atacantes en orden
        self.makeFirstPlayer()

        self.cartasJugadas = {"ataque": [], "defensa": []}
        self.durak = -1 # Indice del player que termina siendo durak, -1 si la partida termina en draw
        self.gameFinished = False # Bool que determina si la partida sigue o termina
        self.game()

        # u1, u2 y u3 son las 3 cartas visibles del usuario

        # Retorna una lista con 3 o menos elementos de la mano del jugador (funciona con slicing), son clase Naipe
        self.listpos = 0
        self.manoVisible = self.jugadores[0].manoAcotada(self.listpos)

        # Lista con el nombre de los archivos de las imagenes correspondientes para cada carta en manoVisible
        self.imagesName = self.getImagesName()

       #!! rehacer con lambda x = 267, y = 370, w = 70, h = 130 - iniciales, para avanzar en 102 en lambda
        self.u1 = BotonCarta(267, 370, self.w, self.h,
                             self.manoVisible[0].fileNaipe(), False, True)
        self.u2 = BotonCarta(369, 370, self.w, self.h,
                             self.manoVisible[1].fileNaipe(), False, True)
        self.u3 = BotonCarta(471, 370, self.w, self.h,
                             self.manoVisible[2].fileNaipe(), False, True)

        # genera posiciones para cartas fijas, y crea lista de botones no interactivos
        # que corresponden a los jugadores AI de 1 a 5
        self.pos = [(20, 200), (20, 20), (369, 20), (700, 20), (700, 200)]
        self.bot_ai = list(map(lambda i: BotonCarta(
            self.pos[i][0], self.pos[i][1], self.w, self.h, "Grey_1.png", "Blue_1.png", False), [i for i in range(5)]))

        # t1 es la carta trump
        self.t1 = BotonCarta(
            100, 400, 50, 67, self.trump.fileNaipe(), False, False)

        # para desplazarse en la lista
        self.arrow_up = BotonCarta(600, 400, 30, 30, "up.png", False, False)
        self.arrow_down = BotonCarta(
            650, 400, 30, 30, "down.png", False, False)

        #!!!Rehacer la lambda una vez que tenga internet, para tener lista y no variables soltadas
    '''
    def crearListButtons(self):
        list_buttons = lista(map(lambda i: BotonCarta(x,y,w,h,self.manoVisible[i].fileNaipe()),[i for i in range(2)]))
    '''

    def crearJugadores(self, nJugadores):
        jugadores = [JugadorCPU() for id in range(1, nJugadores)]
        jugadores.append(JugadorHumano())
        jugadores.reverse()  # Jugador humano siempre en indice 0
        return jugadores

    def repartirCartas(self, atacantes = []):  # Repartir cartas al inicio de la partida o al finalizar un ataque
        if len(atacantes) == 0: 
            jugadores = self.jugadores
        else:
            jugadores = atacantes # Esto ocurrira si se tienen menos de 6 jugadores o mas de 36 cartas, future proof
        repartir = False
        for i in range(len(jugadores)):
            if self.baraja.mostrarCantidad() > 0:
                if jugadores[i].mostrarCantidad() < 6:
                    repartir = True
                    self.jugadores.index(jugadores[i]).sacarCarta(self.baraja.sacarDeBaraja()) 
            else:
                repartir = False

        if repartir == True:
            self.repartirCartas(atacantes)

    def makeTrump(self):
        if self.nJugadores >= 6:  # Si son 6 jugadores, no quedaran cartas en la baraja despues de repartir
            return self.baraja.sacarTrumpCon6Jugadores()
        else:
            return self.baraja.sacarTrump()
    
    def makeFirstPlayer(self):
        trumps = [jugador.getLowerTrump(self.trump) for jugador in self.jugadores] # lista con los menores trump de los jugadores
        self.jugadorActivo = trumps.index(min(trumps))
        self.atacante = self.jugadorActivo
        if self.jugadorActivo == (len(self.jugadores) - 1):
            self.defensor = 0
        else:
            self.defensor = self.jugadorActivo + 1
    
    def checkGame(self):
        cantNaipes = [jugador.mostrarCantidad() for jugador in self.jugadores]
        if cantNaipes.count(0) == (len(self.jugadores) - 1): # 1 jugador quedo con cartas en su mano
            self.gameFinished = True
            for i in range(len(cantNaipes)):
                if cantNaipes[i] != 0:
                    self.durak = i # Asigna el indice del durak
    


        elif cantNaipes.count(0) == len(self.jugadores): # todos los jugadores quedaron con 0 cartas (draw)
            self.gameFinished = True
        return self.gameFinished
    
    def getDurak(self):
        return self.durak

    # probando funciones en consola
    def atacar(self):
        #wip
        if self.jugadorActivo == 0: #Turno del humano
            pass
        else: #Turno de la cpu
            pass

        # Al terminar el ataque se reinician las cartas jugadas
        self.cartasJugadas = {"ataque": [], "defensa": []} 
        pass

    def game(self):
        self.atacar()
        self.checkGame()
        if gameFinished:
            print ("Game Over")
            if durak != -1:
                print ("El jugador " + self.durak + " es nuestro querido Durak, felicidades, perdedor.")
        else:
            # Future proof
            self.repartirCartas(self.atacantes)
            self.repartirCartas([self.jugadores[self.defensor]])

            self.game()

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

        '''
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
        '''

    def clean(self):
        pass

    def avanzarListPos(self, action):
        # usaremos cantidad para acotar cuantas veces se puede bajar/subir
        canti = self.jugadores[0].mostrarCantidad()
        if action:  # True = down
            print("accion down")
            print("canti % 3 es", int(canti / 3) - 1)
            if self.listpos < int(canti / 3) - 1:
                self.listpos += 1
            # estamos en ultima "pagina" de lista
            elif self.listpos == int(canti / 3) - 1:
                self.listpos = 0  # volvemos al inicio de forma circular
        else:  # False = up
            if self.listpos > 0:
                self.listpos -= 1
            elif self.listpos == 0:
                # vuelve a la ultima "pagina"
                self.listpos = int(canti / 3) - 1
        print("Posicion actual en lista de naipes de humano es: ", self.listpos)

    def get_event(self, event, keys, screen):

        # Para los hovers/ clickeos sobre las CARTAS
        # sobre carta 1

        #agregar no reaccionar a las cartas nulas
        if self.u1.getRekt().collidepoint(pygame.mouse.get_pos()):
            self.u1.mouseOverButton(True, 340)

            if event.type == pygame.MOUSEBUTTONDOWN:
                print("Clickeando sobre CARTA1")
                # hacer algo util con la carta po
        else:
            self.u1.mouseOverButton(False, 370)
            pygame.display.update()

        # sobre carta 2
        if self.u2.getRekt().collidepoint(pygame.mouse.get_pos()):
            self.u2.mouseOverButton(True, 340)

            if event.type == pygame.MOUSEBUTTONDOWN:
                print("Clickeando sobre CARTA2")
        else:
            self.u2.mouseOverButton(False, 370)

        # sobre carta 3
        if self.u3.getRekt().collidepoint(pygame.mouse.get_pos()):
            self.u3.mouseOverButton(True, 340)

            if event.type == pygame.MOUSEBUTTONDOWN:
                print("Clickeando sobre CARTA3")
                # mismo
        else:
            self.u3.mouseOverButton(False, 370)

        # Para solo clickeos sobre las FLECHAS (!!! quiza agregar movimiento con flechas de tecaldo?)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.arrow_up.getRekt().collidepoint(pygame.mouse.get_pos()):
                self.avanzarListPos(False)
                self.manoVisible = self.jugadores[0].manoAcotada(self.listpos)

            if self.arrow_down.getRekt().collidepoint(pygame.mouse.get_pos()):
                self.avanzarListPos(True)
                self.manoVisible = self.jugadores[0].manoAcotada(self.listpos)

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
        list(map(lambda i: screen.blit(self.bot_ai[i].getImg(
        ), (self.bot_ai[i].getX(), self.bot_ai[i].getY())), [i for i in range(5)]))

    def render(self, clock, screen, p):
        screen.fill(self.background_color)

        # Prepara para dibujar

        # Mano del humano muestra 3 cartas

        # funcion aparte,ojala
        down = self.arrow_down.getImg()
        up = self.arrow_up.getImg()

        # no tocar, son generadores de lista de textos de cantidades de cartas
        cant_Textos = list(map(lambda i: tt.render_text("T", str(
            self.jugadores[i].mostrarCantidad()), self.white), [i for i in range(1, 6)]))
        cant_Textos.insert(0, tt.render_text(
            "S", str(self.jugadores[0].mostrarCantidad()), self.white))

        while not self.st_done:
            #!!! como funcion
            carta1 = self.manoVisible[0].getImgNaipe(self.w, self.h)
            carta2 = self.manoVisible[1].getImgNaipe(self.w, self.h)
            carta3 = self.manoVisible[2].getImgNaipe(self.w, self.h)

            # Dibuja las manos de los jugadores
            #!!!limpiaaaar con funcion, hasta se puede hacer una sola lamda con carta1-3
            screen.blit(carta1, (self.u1.getX(), self.u1.getY()))
            screen.blit(carta2, (self.u2.getX(), self.u2.getY()))
            screen.blit(carta3, (self.u3.getX(), self.u3.getY()))

            #!!!una funcioncita aparte tmb
            screen.blit(down, (self.arrow_down.getX(), self.arrow_down.getY()))
            screen.blit(up, (self.arrow_up.getX(), self.arrow_up.getY()))

            self.mostrarOponentes(screen)
            # Debajo de cada carta, se imprime la cantidad de naipes de cada jugador.
            self.mostrarCantidadNaipes(screen, cant_Textos)
            # Muestra la trump
            self.mostrarTrump(screen)

            pygame.display.update()
            screen.fill(self.background_color)

            [self.get_event(event, pygame.key.get_pressed(), screen)
             for event in pygame.event.get()]
