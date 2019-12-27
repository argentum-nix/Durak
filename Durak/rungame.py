import pygame
import text_tools as tt

import intro
import menu
import juego
import creditos

from naipe import Naipe 
from baraja import Baraja 
from jugador import Jugador, JugadorHumano, JugadorCPU



class RunGame():
    def __init__(self):
        print("Inicializa PyGame")
        pygame.init()
        self.screen_param = (800, 500)
        self.screen = pygame.display.set_mode(self.screen_param)
        # Ventana creada 
        
        pygame.display.set_caption('Durak') # Escribe Durak en el borde de la ventana
        icon = pygame.image.load('data/icon/icon.png')
        pygame.display.set_icon(icon)
        self.clock = pygame.time.Clock()
        self.state_dict = {
            "INTRO": intro.Intro(),
            "MENU" : menu.Menu(),
            "JUEGO" : juego.Juego(6), # Se puede poner cualquier numero de jugadores
            "CREDITOS" :creditos.Creditos()
            }
        # el estado actual (en que stage esta el juego)
        self.state_name = "INTRO"
        self.st_done = False
        # usando el stage, a state se asigna la clase actual la que va a correr
        self.state = self.state_dict[self.state_name]
        # tecla recibida
        self.key = pygame.key.get_pressed()
        print("Instancee excitosamente la clase RunGame de rungame.py")
        # si recibe salida, termina
        # si recibe cualquier accion,

    #def Player(self):

    def game_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True
                pygame.quit()
                exit()
            elif event.type in (pygame.KEYDOWN, pygame.KEYUP):
                # analiza que tecla se recibio
                self.keys = pygame.key.get_pressed()
                # hace get event usando la tecla y llama a metodo de get event de clase de stage actual
                self.state.get_event(event, self.keys)

    def cambiar_de_estado(self):
        if self.state.st_done:
            self.state.clean()
            # cambia de estado, si es que el actual termino
            # reasigna su estado a False (no terminado)
            self.state_name = self.state.next
            self.state.st_done = False
            # instancia la clase de instante
            self.state = self.state_dict[self.state_name]
           # self.state.entry() - para musica

        # funcion de main loop, la que se llamara en main
    def correr(self):
        # mientras estado no este terminado
        while not self.st_done:
            # revisa si se cierra la ventana, para terminar
            if self.state.quit:
                self.st_done = True
                pygame.display.quit()
            # en caso de estar en el stage
            # now = pygame.time.get_ticks()
            self.game_loop()
            self.cambiar_de_estado()
            #self.state.update(now, self.keys)
            self.state.render(self.clock, self.screen, self.screen_param)
            pygame.display.update()
            # self.clock.tick(self.fps)
