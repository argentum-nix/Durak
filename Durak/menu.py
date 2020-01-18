import pygame
import sys_tools as st
import text_tools as tt
from botonCarta import BotonCarta
import sys

'''
class Menu(st.Estados_Juego)
 |  Clase, responsable de instanciar la pantalla de menu.
 |  Recibe st.Estados_Juego, que contiene algunos de los parametros, 
 |  comunes para cada clase-fase de juego.
 |
 |  Muestra 3 botones interactivos, de los cuales el primer lleva a la fase
 |  de juego, el segundo a los créditos, y el tercero permite salir de juego.
 |
 |  Se utiliza una clase propia, llamada BotonCarta, la cual genera botones con 
 |  cierta imágen y posición asociada. En esta clase se ocupa tres funciones lambda,
 |  en makeBotones(self) y render(self, clock, screen, p). En el primer caso lambda 
 |  es un generador de lista de los tres botones, y el el segundo se lo usa para mostrar el texto
 |  y los botones en la pantalla del jugador.
'''


class Menu(st.Estados_Juego):
    def __init__(self):
        st.Estados_Juego.__init__(self)
        self.makeBotones()

    '''
    makeBotones(self)
    |
    |   Funcion, responsable de crear una lista de tres botones,
    |   en las posiciones, indicadas por las tuplas de pos, de tipo (width, height)
    |   CONCEPTOS DE CURSO: Formas funcionales: lambda. Comprensión de listas.  
    '''

    def makeBotones(self):
        pos = [(102, 154), (322, 154), (552, 154)]
        self.botones = list(map(lambda x: BotonCarta(
            pos[x][0], pos[x][1], 130, 190, "Grey_1.png", "Blue_1.png", True), [x for x in range(0, 3)]))

    '''
    get_event(self, event, keys)
    |   Función, que analiza los eventos de juego. Al cerrar la ventana (ESC),
    |   el evento corresponde a pygame.QUIT y se termina la ejecución del código.
    |   En caso de presionar botón 1 (1 o con el mouse), se pasa a la fase, en la 
    |   cual se pregunta al jugador si este quiere ver tutorial. Al usar botón 2,
    |   el jugador accede a la pantalla de créditos. En caso de usar el botón 3,
    |   el jugador sale del juego.
    '''

    def get_event(self, event, keys):
        if self.botones[0].getRekt().collidepoint(pygame.mouse.get_pos()):
            self.botones[0].isActivePlayer(True)
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.touchCard.play()
                self.st_done = True
                self.next = "QUESTION_BOX"
        else:
            self.botones[0].isActivePlayer(False)

        if self.botones[1].getRekt().collidepoint(pygame.mouse.get_pos()):
            self.botones[1].isActivePlayer(True)
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.touchCard.play()
                self.st_done = True
                self.next = "CREDITOS"
        else:
            self.botones[1].isActivePlayer(False)

        if self.botones[2].getRekt().collidepoint(pygame.mouse.get_pos()):
            self.botones[2].isActivePlayer(True)
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.touchCard.play()
                self.st_done = True
                self.quit = True
                pygame.quit()
                exit()
        else:
            self.botones[2].isActivePlayer(False)

        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            self.quit = True
            pygame.quit()
            exit()

    '''
    render(self)
    |   Funcion render, utilizada para mostrar la media y texto en la pantalla.
    |   Se usa un arreglo strings, para guardar las tuplas, de tipo (texto, pos_X),
    |   lo cual permite automatizar la generación de textos, que se muestran en la pantalla.
    |   El texto corresponde a los nombres de botones, indicando su funcioón.
    |   USO DE CONCEPTOS: Formas funcionales: lambda. Comprensión de listas.
    '''

    def render(self, clock, screen, p):
        screen.fill(self.background_color)
        self.touchCard = pygame.mixer.Sound('data/other/card-flip.wav')
        # Muestra los strings en posiciones indicadas
        strings = [(">JUGAR", 112), (">CREDITOS", 330), (">SALIR", 562)]
        [(lambda t: screen.blit(tt.render_text("S", t[0], self.white), (t[1], 135)))(t)
         for t in strings]

        while not self.st_done:
            # Muestra los naipes - botones en posiciones indicadas
            [(lambda b: screen.blit(b.getImg(), (b.getX(), b.getY())))(b)
             for b in self.botones]
            pygame.display.update()
            [self.get_event(event, pygame.key.get_pressed())
             for event in pygame.event.get()]
