import pygame
import text_tools as tt
import sys_tools as st
import intro
import menu
import juego
import creditos
import question
import tutorial
import fin


'''
class Rungame()
 |  Clase, que funciona como engine principal de juego.
 |  Es la clase responsable de iniciar pygame y la pantalla (Lineas 32-38)
 |  
 |  Para instanciar varias fases de juego, se utiliza un archivo self.st_dict,
 |  el cual contiene las clases a instanciar (sin instanciarlas), hasta que
 |  asi lo indique el flag self.st_next, el cual es un string, que almacena el
 |  nombre de la fase de juego, a cual corresponda pasar.
 |
 |  Para clases Juego y GameFinished, las instancias son con paso de parametros,
 |  siendo estos la cantidad de jugadores y el perdedor de juego terminado.
 |  (6 y self.durak, respectivamente).

'''

class RunGame():
    def __init__(self):
        #Ajustes iniciales de pygame y de la ventana.
        pygame.init()
        self.screen_param = (800, 500)
        self.screen = pygame.display.set_mode(self.screen_param)
        pygame.display.set_caption('Durak')
        icon = pygame.image.load('data/icon/icon.png')
        pygame.display.set_icon(icon)
        self.clock = pygame.time.Clock()

        self.durak = -1
        self.state_dict = {
            "INTRO": intro.Intro,
            "MENU": menu.Menu,
            "QUESTION_BOX": question.Question,
            "TUTORIAL": tutorial.Tutorial,
            "JUEGO": juego.Juego,
            "CREDITOS": creditos.Creditos,
            "FIN": fin.GameFinished
        }
        #El estado inicial de juego:
        self.state_name = "INTRO"
        self.st_done = False
        #A state se le asigna la clase a instanciar, segun su llave de diccionario.
        self.state = self.state_dict[self.state_name]
        self.key = pygame.key.get_pressed()
        self.gameFinished = False
        
    '''
    |game_loop(self)
    |
    |Funcion, responsable de analizar los eventos.
    |Usando funcion de pygame, pygame.event.get(), analiza
    |la tecla recibida (self.keys = pygame.key.get_pressed()) y el evento.
    '''
    def game_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True
                pygame.quit()
                exit()
            elif event.type in (pygame.KEYDOWN, pygame.KEYUP):
                self.keys = pygame.key.get_pressed()
                self.state.get_event(event, self.keys)

    '''
    |cambiar_de_estado(self)
    |
    |Funcion, responsable de cambio de fase (clase activa) de juego.
    |Utiliza el diccionario self.state_dict y la llave, para instanciar
    |la clase correspondiente.
    |
    |Clases Juego y gameFinished se difieren del resto, dado que 
    |reciben paramentros: nJugadores (6 por defecto) y durak_mode (self.durak)
    '''
    def cambiar_de_estado(self):
        if self.state.st_done:
            self.durak = self.state.durak
            self.state_name = self.state.next
            self.state.st_done = False
            self.state = self.state_dict[self.state_name]
            if self.state_name == "JUEGO":
                self.state = self.state(6)
            elif self.state_name == "FIN":
                self.state = self.state(self.durak)
            else: 
                self.state = self.state()

    '''
    |correr(self)
    |
    |Funcion, responsable de mantener activo el juego.
    |Se basa en las varias llamadas de funciones, propias
    |de la clase, como game_loop() y cambiar_de_estado()
    '''
    def correr(self):
        self.state = self.state_dict[self.state_name]
        self.state = self.state()
        while not self.st_done:
            if self.state.quit:
                self.st_done = True
                pygame.display.quit()
            self.game_loop()
            self.cambiar_de_estado()
            self.state.render(self.clock, self.screen, self.screen_param)
            pygame.display.update()