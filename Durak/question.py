
import sys_tools as st
import text_tools as tt
import pygame
from botonCarta import BotonCarta

'''
class Question(st.Estados_Juego)
|   Clase, que se instancia para revisar
|   si el jugador queire ver el tutorial.
'''


class Question(st.Estados_Juego):
    def __init__(self):
        st.Estados_Juego.__init__(self)
        self.skipCheck()
        # Si self.answer = False, veremos el tutorial.
        # En caso contrario, la clase Question cambia a clase Juego.
        if self.answer:
            self.st_done = True
            self.next = "JUEGO"

        self.fondo = BotonCarta(200, 100, 407, 251, "qbox.png", False, False)
        self.skip = BotonCarta(260, 240, 90, 90, "skip.png", False, True)
        self.show_tut = BotonCarta(
            450, 240, 90, 90, "continue.png", False, True)
    '''
    skipCheck(self)
    |   Función, que obtiene la respuesta de usuario, guardad en log.txt
    |   Se usa try-except-finally para revisar que el archivo existe, y,
    |   usando split, obtener la respuesta, pasandola a booleanos con el
    |   operador ternario.
    |
    |   En caso de que el archivo tenga forma, distinta a answer: f o t,
    |   se considera que el archivo esta rota, y este se borra,
    |   escribiendo la respuesta answer:f por default.
    |
    |   Por default, answer:f significa que se preguntará al usuario si
    |   este quiere ver el tutorial o si quiere saltarlo.
    |   CONCEPTOS DE CURSO: Manejo de Errores.
    '''

    def skipCheck(self):
        try:
            with open("log.txt", 'r') as f:
                # True: se salta el tutorial y nunca mas se muestra.
                # False: se pregunta al usuario si este quiere ver el tutorial.
                self.answer = (f.readlines()[0].split(":"))[1]
                aux = ["f", "t", True, False]
                # Arhcivo roto (usuario modifico el archivo/otra causa)
                if self.answer not in aux:
                    st.delete_txt("log.txt")
                    self.skipCheck()
                else:
                    self.answer = {"f": False, "t": True}[self.answer]
        except OSError:
            with open("log.txt", 'w') as f:
                f.write("answer:f")
                self.answer = False
        finally:
            f.close()
    '''
    get_event(self, event, keys)
    |   Función, que analiza los eventos de juego. Al cerrar la ventana (ESC),
    |   el evento corresponde a pygame.QUIT y se termina la ejecución del código.
    |   En caso de presionar botón NO, el jugador pasa a la fase de Tutorial.
    |   Al usar botón SI, el jugador accede directamente al juego.
    '''

    def get_event(self, event, keys):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.skip.getRekt().collidepoint(pygame.mouse.get_pos()):
                self.st_done = True
                st.write_txt("log.txt", "answer:t")
                self.next = "JUEGO"

            elif self.show_tut.getRekt().collidepoint(pygame.mouse.get_pos()):
                self.st_done = True
                self.next = "TUTORIAL"

        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            self.quit = True
            pygame.quit()
            exit()

    '''
    render(self)
    |   Funcion render, utilizada para mostrar la media y texto en la pantalla.
    |   Se usa para demostrar una ventana con dos botones: SI y NO.
    |   Al elegir SI,el usuario salta el tutorial y pasa al juego.
    |   Al elegir NO, procederá a ver el tutorial.
    |   USO DE CONCEPTOS: Comprensión de listas.
    '''

    def render(self, clock, screen, p):

        if not self.st_done:
            screen.fill(self.background_color)
            string = "Saltar el tutorial?"
            screen.blit(self.fondo.getImg(),
                        (self.fondo.getX(), self.fondo.getY()))
            question_text = tt.render_text("S", string, self.white)
            screen.blit(question_text, (290, 200))

        while not self.st_done:
            pygame.display.update()
            screen.blit(self.skip.getImg(),
                        (self.skip.getX(), self.skip.getY()))
            screen.blit(self.show_tut.getImg(),
                        (self.show_tut.getX(), self.show_tut.getY()))
            [self.get_event(event, pygame.key.get_pressed())

             for event in pygame.event.get()]

        temp = pygame.image.load(
            st.current_dir() + "/data/other/game_start3.png").convert_alpha()
        temp = pygame.transform.scale(temp, (800, 500))
        screen.blit(temp, (0, 0))
        pygame.time.delay(600)
        pygame.display.update()
