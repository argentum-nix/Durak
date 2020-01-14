import sys_tools as st
import text_tools as tt
import pygame

'''
class Intro(st.Estados_Juego)
 |  Clase, responsable de instanciar la pantalla introductoria.
 |  Recibe st.Estados_Juego, que contiene algunos de los parametros, 
 |  comunes para cada clase-fase de juego.
 |
 |  Muestra el nombre de juego y el texto, que indica como pasar a menu.
 |  Esta opción se activa, al usar cualquier tecla (Línea 30, pygame,KEYDOWN)
 |  
 |  Ademas, se activa la musica de fondo, que se desactiva, una vez que
 |  empiece el juego. Esto se logra, usando pygame.mixer (Línea 34-34)
 |
 |  En el loop (Linea 40), para lograr el efecto de texto con gradiente, se usa 
 |  función generadora de textos, que, con cado paso de loop, genera texto de 
 |  nuevo color, según la lista self.white_to_bg_fade
'''

class Intro(st.Estados_Juego):
    def __init__(self):
        st.Estados_Juego.__init__(self)

    def get_event(self, event, keys):
        if event.type == pygame.QUIT:
            self.quit = True
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            self.st_done = True
            self.next = "MENU"

    def render(self, clock, screen, p):
        pygame.mixer.music.load("data/other/menu_intro.mp3") 
        pygame.mixer.music.play(1,0.0)
        screen.fill(self.background_color)    
        text_logo = tt.render_text("L", "Durak", self.white)
        screen.blit(text_logo, (p[0] / 2 - text_logo.get_width() //
                                2, p[1] / 2  -text_logo.get_height() // 2))      
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
