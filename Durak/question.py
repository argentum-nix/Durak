
import sys_tools as st
import text_tools as tt
import pygame
from botonCarta import BotonCarta


class Question(st.Estados_Juego):
    def __init__(self):
        print("Instancee exitosamente clase Question")
        st.Estados_Juego.__init__(self)
        self.skipCheck()
        # si el answer es falso, queremos ver el tutorial
        # si es true, quierp salir inmediatamente
        if self.answer:
            self.st_done = True
            self.next = "JUEGO"

        self.fondo = BotonCarta(200, 100, 407, 251, "qbox.png", False, False)
        self.skip = BotonCarta(260, 240, 90, 90, "skip.png", False, True)
        self.show_tut = BotonCarta(
            450, 240, 90, 90, "continue.png", False, True)


    def skipCheck(self):
        try:
            with open("log.txt", 'r') as f:
                # ve si t: salto la cosa, f - muestro la question_box (dejo al decision al usuario)
                self.answer = (f.readlines()[0].split(":"))[1]
                aux = ["f", "t", True, False]
                # archivo roto, borramos.
                if self.answer not in aux:
                    print("entre al delete con answer " + self.answer)
                    st.delete_txt("log.txt")
                    # escribe un archivo de nuevo
                    self.skipCheck()
                else:
                    self.answer = {"f": False, "t": True}[self.answer]
        except OSError:
            with open("log.txt", 'w') as f:
                f.write("answer:f")
                self.answer = False
        finally:
            f.close()


    def clean(self):
        pass

    def get_event(self, event, keys):
        if event.type == pygame.MOUSEBUTTONDOWN:

            # ya no quiero ver el tutorial, tengo que reescribir el archivo
            if self.skip.getRekt().collidepoint(pygame.mouse.get_pos()):
                self.st_done = True
                st.write_txt("log.txt", "answer:t")
                self.next = "JUEGO"
            # queremos ver el tutorial, no cambio nada en archivo, sigue en answer:f

            elif self.show_tut.getRekt().collidepoint(pygame.mouse.get_pos()):
                self.st_done = True
                self.next = "TUTORIAL"
               

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

        temp = pygame.image.load(st.current_dir() + "/data/other/game_start3.png").convert_alpha()
        temp = pygame.transform.scale(temp, (800, 500))
        screen.blit(temp, (0,0))            
        pygame.time.delay(600)
        pygame.display.update()

