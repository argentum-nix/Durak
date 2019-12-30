
import sys_tools as st
import pygame
from botonCarta import BotonCarta


class Question(st.Estados_Juego):
    def __init__(self):
        print("Instancee exitosamente clase Question")
        st.Estados_Juego.__init__(self)
        self.fondo = BotonCarta(200, 100, 407, 251, "qbox.png", False, False)
        self.skip = BotonCarta(260, 240, 90, 90, "skip.png", False, True)
        self.show_tut = BotonCarta(
            450, 240, 90, 90, "continue.png", False, True)

    def clean(self):
        pass

    def get_event(self, event, keys):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.skip.getRekt().collidepoint(pygame.mouse.get_pos()):
                self.st_done = True
                self.next = "JUEGO"

            elif self.show_tut.getRekt().collidepoint(pygame.mouse.get_pos()):
                self.st_done = True
                print("Eligio showtut ")
                # self.next = "TUTORIAL"

    def render(self, clock, screen, p):
        screen.fill(self.background_color)

        while not self.st_done:
            pygame.display.update()
            screen.blit(self.fondo.getImg(),
                        (self.fondo.getX(), self.fondo.getY()))
            screen.blit(self.skip.getImg(),
                        (self.skip.getX(), self.skip.getY()))
            screen.blit(self.show_tut.getImg(),
                        (self.show_tut.getX(), self.show_tut.getY()))
            [self.get_event(event, pygame.key.get_pressed())
             for event in pygame.event.get()]
