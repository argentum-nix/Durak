# para solamente printear los nombres paralelo etc
import sys_tools as st
import text_tools as tt
import pygame


class Creditos(st.Estados_Juego):
    def __init__(self):
        st.Estados_Juego.__init__(self)
        self.integrante1 = "Anastasiia Fedorova"
        self.rol_int1 = "201873505-1"
        self.integrante2 = "Ignacio Jorquera"
        self.rol_int2 = "201873561-2"
        self.paralelo = "200"
        self.sem = "2019-2"
        self.ramo = "Lenguajes de Programacion"
        self.next = "MENU"
        self.software = "[Software: Pixelator ©]"
        self.naipes = "[Naipes de 'Card Pack by Andrew Tidey']"

        self.logo_utfsm = pygame.image.load(
            st.current_dir() + "/data/other/utfsm_pixel.png").convert_alpha()

    def clean(self):
        pass

    def get_event(self, event, keys):
        if event.type == pygame.QUIT:
            self.quit = True
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.st_done = True

    def render(self, clock, screen, p):
        self.logo_utfsm = pygame.transform.scale(self.logo_utfsm, (int(0.31 * p[0]), int(0.32 * p[1])))

        screen.fill(self.background_color)
        screen.blit(self.logo_utfsm, (p[0] / 2 - self.logo_utfsm.get_width() // 2, p[1] - int(0.76 * p[1]) - self.logo_utfsm.get_height() // 2))
        main_text = tt.render_text("M", "Integrantes:", self.white)
        screen.blit(main_text, (p[0] / 2 - main_text.get_width() // 2, p[1] / 2 + int(0.06 * p[1]) - main_text.get_height() // 2))

        i1_text = tt.render_text(
            "S", ">" + self.integrante1 + " " + self.rol_int1, self.white)
        screen.blit(i1_text, (int(0.25 * p[0]), int(0.62 * p[1])))
        i2_text = tt.render_text(
            "S", ">" + self.integrante2 + "   " + self.rol_int2, self.white)
        screen.blit(i2_text, (int(0.25 * p[0]), int(0.66 * p[1])))

        paralelo_text = tt.render_text(
            "S", "Paralelo: " + self.paralelo, self.white)
        screen.blit(paralelo_text, (int(0.25 * p[0]), int(0.44 * p[1])))

        soft = tt.render_text("T", ">" + self.software, self.white)
        screen.blit(soft,(int(0.25 * p[0]), int(0.74 * p[1])))

        cards = tt.render_text("T", ">" + self.naipes, self.white)
        screen.blit(cards, (int(0.25 * p[0]), int(0.78 * p[1])))

        count = 0
        while not self.st_done:
            term_text = tt.render_text(
                "S", ">Presione ENTER para volver al menu...", self.white_to_bg_fade[count % len(self.white_to_bg_fade)])
            screen.blit(term_text, (p[0] / 2 - term_text.get_width() //
                                    2, p[1] - 100 / 2 - term_text.get_height() // 2))
            pygame.display.flip()
            count += 1
            clock.tick(5)
            [self.get_event(event, pygame.key.get_pressed())
             for event in pygame.event.get()]
