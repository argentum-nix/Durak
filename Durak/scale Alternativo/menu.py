import pygame
import sys_tools as st
import text_tools as tt


class Menu(st.Estados_Juego):
    def __init__(self):
        st.Estados_Juego.__init__(self)
        self.jacket_button1 = pygame.image.load(
            st.current_dir() + "/data/cards/jacket_1.png").convert_alpha()

        self.jacket_button2 = pygame.image.load(
            st.current_dir() + "/data/cards/jacket_2.png").convert_alpha()

        """ self.b1 = pygame.Rect(102, 154, 135, 181)
        self.b2 = pygame.Rect(322, 154, 135, 181)
        self.b3 = pygame.Rect(552, 154, 135, 181)

        self.jacket_button1 = pygame.transform.scale(self.jacket_button1, (160, 226))
        self.jacket_button2 = pygame.transform.scale(self.jacket_button2, (160, 226))

        self.images = [self.jacket_button1, self.jacket_button2] """

    def clean(self): 
        pass

    def get_event(self, event, keys):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.b1.collidepoint(pygame.mouse.get_pos()):
                self.st_done = True
                self.next = "QUESTION_BOX"

            elif self.b2.collidepoint(pygame.mouse.get_pos()):
                self.st_done = True
                self.next = "CREDITOS"

            elif self.b3.collidepoint(pygame.mouse.get_pos()):
                self.quit = True
                pygame.quit()

        elif event.type == pygame.QUIT:
            self.quit = True
            pygame.quit()

    def render(self, clock, screen, p):

        self.b1 = pygame.Rect(int(0.13 * p[0]), int(0.31 * p[1]), int(0.17 * p[0]), int(0.36 * p[1]))
        self.b2 = pygame.Rect(int(0.4 * p[0]), int(0.31 * p[1]), int(0.17 * p[0]), int(0.36 * p[1]))
        self.b3 = pygame.Rect(int(0.69 * p[0]), int(0.31 * p[1]), int(0.17 * p[0]), int(0.36 * p[1]))

        self.jacket_button1 = pygame.transform.scale(self.jacket_button1, (int(0.2 * p[0]), int(0.45 * p[1])))
        self.jacket_button2 = pygame.transform.scale(self.jacket_button2, (int(0.2 * p[0]), int(0.45 * p[1])))

        self.images = [self.jacket_button1, self.jacket_button2]


        screen.fill(self.background_color)
        # dibuja zonas donde funcionan los clicks
        #pygame.draw.rect(screen, (255,255,255),(102,154,135,181))
        #pygame.draw.rect(screen, (255,255,255),(322,154,135,181))
        #pygame.draw.rect(screen, (255,255,255),(552,154,135,181))
        boton1 = self.images[1]
        boton2 = self.images[1]
        boton3 = self.images[1]

        boton1_text = tt.render_text("S", ">JUGAR", self.white)
        boton2_text = tt.render_text("S", ">CREDITOS", self.white)
        boton3_text = tt.render_text("S", ">SALIR", self.white)

        screen.blit(boton1_text, (int(0.18 * p[0]), int(0.27 * p[1])))
        screen.blit(boton2_text, (int(0.45 * p[0]), int(0.27 * p[1])))
        screen.blit(boton3_text, (int(0.74 * p[0]), int(0.27 * p[1])))

        while not self.st_done:
            
            screen.blit(boton1, (int(0.09 * p[0]), int(0.24 * p[1])))
            screen.blit(boton2, (int(0.36 * p[0]), int(0.24 * p[1])))
            screen.blit(boton3, (int(0.65 * p[0]), int(0.24 * p[1])))

            pygame.display.update()
            if self.b1.collidepoint(pygame.mouse.get_pos()):
                boton1 = self.images[0]
            else:
                boton1 = self.images[1]

            if self.b2.collidepoint(pygame.mouse.get_pos()):
                boton2 = self.images[0]
            else:
                boton2 = self.images[1]

            if self.b3.collidepoint(pygame.mouse.get_pos()):
                boton3 = self.images[0]
            else:
                boton3 = self.images[1]

            [self.get_event(event, pygame.key.get_pressed())
             for event in pygame.event.get()]
