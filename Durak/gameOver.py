import pygame
import sys_tools as st 
import text_tools as tt
from botonCarta import BotonCarta

class GameOver(st.Estados_Juego):
    def __init__(self):
        st.Estados_Juego.__init__(self)

    def clean(self):
        pass

    def render(self, clock, screen, p):
        screen.fill(self.background_color):
        screen.blit(pause_text, (p[0]/2 - pause_text.get_width()//2, 20))
        term_text = tt.render_text("S", ">Presione SPACE para volver a jugar...", self.white_to_bg_fade[count % len(self.white_to_bg_fade)])
        screen.blit(term_text, (p[0]/2 - term_text.get_width() //
                                    2, p[1] - term_text.get_height() - 100// 2))
        pygame.display.flip()
        count += 1
        clock.tick(5)
        [self.get_event(event, pygame.key.get_pressed(), screen) for event in pygame.event.get()]    