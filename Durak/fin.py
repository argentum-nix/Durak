import pygame
import sys_tools as st
import text_tools as tt
from botonCarta import BotonCarta

'''
class GameFinished(st.Estados_Juego)
|   Clase, que corresponde a la última fase del juego.
|   Para instanciarla, debe recibir el valor de durak_state -
|   perdedor del juego, para su correcto funcionamiento.
|   Por pantalla se avisara quién perdió y se dara la opción
|   de volver al menu, del cual el usuario es libre de cerrar
|   la aplicación o proceder a jugar otra vez.
'''


class GameFinished(st.Estados_Juego):
    def __init__(self, durak_state):
        st.Estados_Juego.__init__(self)
        self.durak = durak_state
    '''
    get_event(self, event, keys)
    |   Función, que analiza los eventos de juego. Al cerrar la ventana (ESC),
    |   el evento corresponde a pygame.QUIT y se termina la ejecución del código.
    |   En caso de presionar SPACE, el usuario volverá al menu.
    '''

    def get_event(self, event, keys):
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            self.st_done = True
            self.quit = True
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.st_done = True
            self.next = "MENU"
            self.durak = -1
            pygame.mixer.music.stop()
    '''
    selectDurakMusic(self)
    |   En base de quien perdio (0 - usuario, otro - computadora),
    |   se elige la música del fondo de la fase.
    '''

    def selectDurakMusic(self):
        if self.durak > 0:
            pygame.mixer.music.load("data/other/win.mp3")
        else:
            pygame.mixer.music.load("data/other/fail.wav")
        pygame.mixer.music.play(-1, 0.0)
    '''
    render(self)
    |   Funcion render, utilizada para mostrar la media y texto en la pantalla.
    |   Se muestra el texto por pantalla, cuyo contenido depende del perdedor del juego actual.
    |   Ademas, en la parte inferior de la pantalla, se muestra el texto, que indica como 
    |   volver al menu. Para generar el texto, se usa funcion modulo, para obtener el efecto
    |   de "flashing text".
    |   USO DE CONCEPTOS: Comprensión de listas.
    '''

    def render(self, clock, screen, p):
        screen.fill(self.background_color)
        count = 0
        self.selectDurakMusic()
        if self.durak > 0:
            durak_text = tt.render_text(
                "S", "El Jugador " + str(self.durak) + " es el Rey de los Idiotas!", self.white)
        else:
            durak_text = tt.render_text(
                "M", "No levanto mi sombrero ante un idiota!", self.white)
        while not self.st_done:
            fools_hat =  pygame.image.load(st.current_dir() + "/data/other/fool.png").convert_alpha()
            term_text = tt.render_text("S", ">Presione SPACE para volver al menu...",
                                       self.white_to_bg_fade[count % len(self.white_to_bg_fade)])

            screen.blit(term_text, (p[0] / 2 - term_text.get_width() //
                                    2, p[1] - term_text.get_height() - 100 // 2))

            screen.blit(durak_text, (p[0]/2 - durak_text.get_width()//2, p[1]//2 - durak_text.get_height()//2))

            screen.blit(fools_hat, (p[0] / 2 - fools_hat.get_width() //
                                      2, p[1] - 380 - fools_hat.get_height() // 2))
            pygame.display.flip()
            count += 1
            clock.tick(5)
            [self.get_event(event, pygame.key.get_pressed())
             for event in pygame.event.get()]
