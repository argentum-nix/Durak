import pygame
import sys_tools as st
import text_tools as tt
from botonCarta import BotonCarta


class GameFinished(st.Estados_Juego):
    def __init__(self, durak_state):
        st.Estados_Juego.__init__(self)
        self.durak = durak_state
        print("durak que me pasaron es", durak_state)
      
    def clean(self):
        pass

    def get_event(self, event, keys):
        if event.type == pygame.QUIT:
            self.st_done = True
            self.quit = True
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.st_done = True
            self.next = "MENU"
            self.durak = -1
            pygame.mixer.music.stop()

    def render(self, clock, screen, p):
        screen.fill(self.background_color)
        count = 0
        print("durak en GameFinished es", self.durak)
        if self.durak > 0:
            pygame.mixer.music.load("data/other/win.mp3")
        else:
            pygame.mixer.music.load("data/other/fail.wav")

        pygame.mixer.music.play(-1,0.0)
        while not self.st_done:

            term_text = tt.render_text("S", ">Presione SPACE para volver al menu...",
                                       self.white_to_bg_fade[count % len(self.white_to_bg_fade)])
            screen.blit(term_text, (p[0] / 2 - term_text.get_width() //
                                    2, p[1] - term_text.get_height() - 100 // 2))
            pygame.display.flip()
            count += 1
            clock.tick(5)
            [self.get_event(event, pygame.key.get_pressed())
             for event in pygame.event.get()]
