import pygame
import sys_tools as st
import text_tools as tt


class Menu(st.Estados_Juego):
    def __init__(self):
        st.Estados_Juego.__init__(self)
        jacket_button1 = pygame.image.load(
            st.current_dir() + "/data/cards/jacket_1.png").convert_alpha()

        jacket_button2 = pygame.image.load(
            st.current_dir() + "/data/cards/jacket_2.png").convert_alpha()

        self.b1 = pygame.Rect(102, 154, 135, 181)
        self.b2 = pygame.Rect(322, 154, 135, 181)
        self.b3 = pygame.Rect(552, 154, 135, 181)

        jacket_button1 = pygame.transform.scale(jacket_button1, (160, 226))
        jacket_button2 = pygame.transform.scale(jacket_button2, (160, 226))

        self.images = [jacket_button1, jacket_button2]
        print("Estoy en clase Menu de modeulo menu.py")
        # screen.fill(self.background_color)
        # screen.blit(jacket_button1, (0, 0))

    def clean(self): 
        pass

    def get_event(self, event, keys):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.b1.collidepoint(pygame.mouse.get_pos()):
                self.st_done = True
                self.next = "JUEGO"

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

        screen.blit(boton1_text, (112, 135))
        screen.blit(boton2_text, (330, 135))
        screen.blit(boton3_text, (562, 135))

        while not self.st_done:
            
            screen.blit(boton1, (70, 120))
            screen.blit(boton2, (290, 120))
            screen.blit(boton3, (520, 120))

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
