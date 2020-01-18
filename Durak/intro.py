import sys_tools as st
import text_tools as tt
import pygame


class Intro(st.Estados_Juego):
    def __init__(self):
        print("Instanceando clase Intro")
        st.Estados_Juego.__init__(self)
        self.next = "MENU"
        print("Estoy en clase de intro (modulo intro.py)")

    def clean(self):
        pass

    def get_event(self, event, keys):
        if event.type == pygame.QUIT:
            self.quit = True
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            self.st_done = True

    def render(self, clock, screen, p):
        screen.fill(self.background_color)
        text_logo = tt.render_text("L", "Durak", self.white)
        screen.blit(text_logo, (p[0] / 2 - text_logo.get_width() //
                                2, p[1] / 2 - text_logo.get_height() // 2))
        count = 0
        while not self.st_done:
            term_text = tt.render_text(
                "S", ">Presione cualquier tecla para continuar...", self.white_to_bg_fade[count % len(self.white_to_bg_fade)])
            screen.blit(term_text, (p[0] / 2 - term_text.get_width() //
                                    2, p[1] - 100 / 2 - term_text.get_height() // 2))
            pygame.display.flip()
            count += 1
            clock.tick(5)
            [self.get_event(event, pygame.key.get_pressed())
             for event in pygame.event.get()]
