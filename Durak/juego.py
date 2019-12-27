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
        
        self.nJugadores = nJugadores # num de jugadores, max 6, min ??
        self.jugadores = self.crearJugadores(nJugadores) # Crea a los n jugadores (incluyendo al usuario como jugador 0) y los guarda en una lista
        
        self.baraja = Baraja() # Crea la baraja para la partida
        self.repartirCartas() # Reparte las cartas para la mano de los jugadores 1 por 1 usando recursión
        self.trump = self.getTrump() # Muestra la primera carta de la baraja para conseguir el trump

        self.jugadorActual = -1 # Almacena el indice del jugador actual
        self.atacantes = []
        self.cartasJugadas = {"ataque": [], "defensa": []} # Almacena las cartas en juego

        self.mostrarInfo()# test, debug de consola


        #u1, u2 y u3 son las 3 cartas visibles del usuario

        self.manoVisible = self.jugadores[0].manoAcotada() # Retorna una lista con 3 o menos elementos de la mano del jugador (funciona con slicing)
        self.imagesName = self.getImagesName() # Lista con el nombre de los archivos de las imagenes correspondientes para cada carta en manoVisible

        self.manoHumano = self.buildHand()
        self.u1 = self.manoHumano[0] # primera carta
        self.u2 = self.manoHumano[1] # segunda carta
        self.u3 = self.manoHumano[2] # tercera carta

        
        # Mano de cada cpu, False indica que no se puede clickear, al menos en mi intento de botoncarta
        self.c1 = BotonCarta(38, 250, 62, 92 ,"Blue_1.png", False)
        self.c2 = BotonCarta(38, 130, 62, 92 ,"Blue_1.png", False)
        self.c3 = BotonCarta(369, 38, 62, 92 ,"Blue_1.png", False)
        self.c4 = BotonCarta(700, 130, 62, 92 ,"Blue_1.png", False)
        self.c5 = BotonCarta(700, 250, 62, 92 ,"Blue_1.png", False)

        # Me acorde que al jugar de 6 no hay deck, igual es facil de implementar, si aumentamos el n de players se incluira.
        #b1 corresponde a la imagen que se mostrara para representar la baraja
        #self.b1 = pygame.Rect(102, 154, 135, 181)

        #t1 es la carta trump
        self.t1 = BotonCarta(550, 38, 62, 92, self.trump.fileNaipe(), False) 
    
    def crearJugadores(self, nJugadores):
        jugadores = [JugadorCPU() for id in range(1, nJugadores)]
        jugadores.append(JugadorHumano())
        jugadores.reverse() # Jugador humano siempre en indice 0
        return jugadores
    
    def repartirCartas(self): # Repartir cartas al inicio de la partida
        repartir = False
        for i in range(len(self.jugadores)): # Reparte 1 carta para cada 1, 6 veces, con recursion
            if self.baraja.mostrarCantidad() > 0:
                if self.jugadores[i].mostrarCantidad() < 6:
                    repartir = True
                    self.jugadores[i].sacarCarta(self.baraja.sacarDeBaraja())
            else:
                repartir = False

        if repartir == True:
            self.repartirCartas()

    def getTrump(self):
        if self.nJugadores >= 6: # Si son 6 jugadores, no quedaran cartas en la baraja despues de repartir
            return self.baraja.sacarTrumpCon6Jugadores()
        else:
            return self.baraja.sacarTrump()
    
    def getJugadores(self):
        return self.jugadores

    def getCartasJugadas(self):
        return self.cartasJugadas

    def getBaraja(self): 
        return self.baraja
    
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
        w = 62
        h = 92
        manoHumano = []
        for img in self.imagesName:
            manoHumano.append(BotonCarta(x, y, w, h, img, True))
            x += 102
        while len(manoHumano) != 3:
            manoHumano.append(BotonCarta(x, y, w, h, "NULL.png", True))
            x += 102
        return manoHumano





    def clean (self):
        pass

    def get_event(self, event, keys):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.u1.getRekt().collidepoint(pygame.mouse.get_pos()):
                self.st_done = True
                self.next = "CARTA_1" # F
            
            if self.u2.getRekt().collidepoint(pygame.mouse.get_pos()):
                self.st_done = True
                self.next = "CARTA_2" # F, cuando haya combate, vincular a esa funcion
            
            if self.u3.getRekt().collidepoint(pygame.mouse.get_pos()):
                self.st_done = True
                self.next = "CARTA_3" # F, same as 2

        elif event.type == pygame.QUIT:
            self.quit = True
            pygame.quit()

    def render(self, clock, screen, p):
        screen.fill(self.background_color)

        # Prepara para dibujar

        # Mano del humano muestra 3 cartas
        carta1 = self.u1.getImg()
        carta2 = self.u2.getImg()
        carta3 = self.u3.getImg()

        # Mano cpu muestra una carta dada vuelta
        cpu1 = self.c1.getImg()
        cpu2 = self.c2.getImg()
        cpu3 = self.c3.getImg()
        cpu4 = self.c4.getImg()
        cpu5 = self.c5.getImg()

        # Trump
        trumpImg = self.t1.getImg()


        # queda super feo al incluir el nombre de cada carta, quizas con un formato lindo se arregle
        """ 
       # Hacer funcion para esto más tarde para evitar error out of bounds
        carta1_text = tt.render_text("S", self.manoVisible[0].printNaipe(), self.white) # temporal
        carta2_text = tt.render_text("S", self.manoVisible[1].printNaipe(), self.white) # temporal
        carta3_text = tt.render_text("S", self.manoVisible[2].printNaipe(), self.white) # temporal

        screen.blit(carta1_text, (self.u1.getX() - 30, self.u1.getY() + 100)) # Texto para la carta 1, arreglar posicion
        screen.blit(carta2_text, (self.u2.getX() - 10, self.u2.getY() + 100)) # Texto para la carta 1, arreglar posicion
        screen.blit(carta3_text, (self.u3.getX() , self.u3.getY() + 100)) # Texto para la carta 1, arreglar posicion """

        # Prepara para mostrar en pantalla el numero de cartas en cada mano, hardcodeado para 6 players, para usar una cantidad variable hay q usar una funcion

        cantidadHumano_text = tt.render_text("S", str(self.jugadores[0].mostrarCantidad()), self.white) # temporal

        cantidadCpu1_text = tt.render_text("S", str(self.jugadores[1].mostrarCantidad()), self.white) # temporal
        cantidadCpu2_text = tt.render_text("S", str(self.jugadores[2].mostrarCantidad()), self.white) # temporal
        cantidadCpu3_text = tt.render_text("S", str(self.jugadores[3].mostrarCantidad()), self.white) # temporal
        cantidadCpu4_text = tt.render_text("S", str(self.jugadores[4].mostrarCantidad()), self.white) # temporal
        cantidadCpu5_text = tt.render_text("S", str(self.jugadores[5].mostrarCantidad()), self.white) # temporal

        # Info para mostrar el trump
        trump_text = tt.render_text("S", "Trump: " + self.trump.printNaipe(), self.white) # imprime el nombre del trump

        # Dibuja en pantalla la cantidad de cartas de cada jugador
        screen.blit(cantidadHumano_text, (self.u2.getX() + 27, self.u2.getY() + 94))

        screen.blit(cantidadCpu1_text, (self.c1.getX() + 27, self.c1.getY() + 94))
        screen.blit(cantidadCpu2_text, (self.c2.getX() + 27, self.c2.getY() + 94))
        screen.blit(cantidadCpu3_text, (self.c3.getX() + 27, self.c3.getY() + 94))
        screen.blit(cantidadCpu4_text, (self.c4.getX() + 27, self.c4.getY() + 94))
        screen.blit(cantidadCpu5_text, (self.c5.getX() + 27, self.c5.getY() + 94))

        # Dibuja en pantalla la cantidad de cartas del deck

        # Dibuja en pantalla la info del trump
        screen.blit(trump_text, (self.t1.getX() - 65, self.t1.getY() - 18))

        
        while not self.st_done:
            
            # Dibuja las manos de los jugadores
            screen.blit(carta1, (self.u1.getX(), self.u1.getY()))
            screen.blit(carta2, (self.u2.getX(), self.u2.getY()))
            screen.blit(carta3, (self.u3.getX(), self.u3.getY()))

            screen.blit(cpu1, (self.c1.getX(), self.c1.getY()))
            screen.blit(cpu2, (self.c2.getX(), self.c2.getY()))
            screen.blit(cpu3, (self.c3.getX(), self.c3.getY()))
            screen.blit(cpu4, (self.c4.getX(), self.c4.getY()))
            screen.blit(cpu5, (self.c5.getX(), self.c5.getY()))

            # Dibuja el trump
            screen.blit(trumpImg, (self.t1.getX(), self.t1.getY()))



            pygame.display.update()
            carta1 = self.u1.getImg()
            carta2 = self.u2.getImg()
            carta3 = self.u3.getImg()


            [self.get_event(event, pygame.key.get_pressed())
             for event in pygame.event.get()]
