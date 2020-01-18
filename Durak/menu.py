import pygame
import sys_tools as st
import text_tools as tt
from botonCarta import BotonCarta


class Menu(st.Estados_Juego):
    def __init__(self):
        st.Estados_Juego.__init__(self)
        self.makeBotones()

    def clean(self):
        pass

    def makeBotones(self):
        pos = [(102, 154), (322, 154), (552, 154)]
        self.botones = list(map(lambda x: BotonCarta(
            pos[x][0], pos[x][1], 130, 190, "Grey_1.png", "Blue_1.png", True), [x for x in range(0, 3)]))

    def get_event(self, event, keys):
        if self.botones[0].getRekt().collidepoint(pygame.mouse.get_pos()):
            self.botones[0].isActivePlayer(True)
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.st_done = True
                self.next = "QUESTION_BOX"
        else:
            self.botones[0].isActivePlayer(False)

        if self.botones[1].getRekt().collidepoint(pygame.mouse.get_pos()):
            self.botones[1].isActivePlayer(True)
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.st_done = True
                self.next = "CREDITOS"
        else:
            self.botones[1].isActivePlayer(False)

        if self.botones[2].getRekt().collidepoint(pygame.mouse.get_pos()):
            self.botones[2].isActivePlayer(True)
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.quit = True
                pygame.quit()
        else:
            self.botones[2].isActivePlayer(False)

        if event.type == pygame.QUIT:
            self.quit = True
            self.st_done = True
            pygame.quit()

    def render(self, clock, screen, p):
        screen.fill(self.background_color)
        #Muestra los strings en posiciones indicadas
        strings = [(">JUGAR", 112), (">CREDITOS", 330), (">SALIR", 562)]
        [(lambda t: screen.blit(tt.render_text("S", t[0], self.white),(t[1], 135)))(t) for t in strings]

        while not self.st_done:
            #Muestra los naipes - botones en posiciones indicadas
            [(lambda b: screen.blit(b.getImg(), (b.getX(), b.getY())))(b)
             for b in self.botones]
            pygame.display.update()
            [self.get_event(event, pygame.key.get_pressed())
             for event in pygame.event.get()]
