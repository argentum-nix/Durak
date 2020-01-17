import pygame
import sys_tools as st
import text_tools as tt
from botonCarta import BotonCarta


class Tutorial(st.Estados_Juego):
    def __init__(self):
        st.Estados_Juego.__init__(self)
        self.fondo = BotonCarta(200, 100, 407, 251, "window.png", False, False)
        self.arrow_right = BotonCarta(self.fondo.getX(
        ) + 330, self.fondo.getY() + 190, 30, 30, "right.png", False, False)
        # seria muy bueno guardar esto en el archivo, y crear una funcion que me haga este array o algo, o que lea linea por linea mejor aun
        # y ahi mismo meter try catch y todo el rollo
        # also ojala revisar que es lo que escribi porque son las 4am no tengo neuronas
        self.strings = ["Hola!", "Bienvenido al juego Durak.", "Las reglas son:", "1.No quedar con cartas", "Número debajo de los naipes", "Representa la cantidad de cartas", "que tiene el jugador.",
                        "El que queda el último, pierde.", "2.Se juega de a 6 personas.", "3.Mejor pinta: Trinufo", "Última carta de la baraja", "Gana a toda otra pinta", "4.El primer atacante es el que",
                        "posee el menor trinufo.", "5.Se ataca con cualquier carta", "Pero la defensa es más compleja:", "Se defiende con:", "Triunfo de mayor valor,", "O carta mayor de la misma pinta",
                        "Las cartas, válidas para usar", "Serán interactivas", "6.Para ver sus cartas", "Use UP y DOWN", "o haga click sobre los botones.", "Se puede pasar el ataque", "guardando las cartas", "para pasar, presione P",
                        "o haga click en el botón", "En caso de no poder defenderse", "Hay que tomar las cartas", "Para hacerlo, presione T", " O haga el click en el botón", "Use el menu para apagar", "la música o los sonidos",
                        "Presione SPACE para", "pausar el juego en el caso", "de que sea necesario", "Suerte!"]

    def clean(self):
        pass

    def mostrarFlechas(self, screen, x=None, y=None):
        if x == None and y == None:
            x = self.arrow_right.getX()
            y = self.arrow_right.getY()
        right = self.arrow_right.getImg()
        screen.blit(right, (x, y))

    def createBG(self):
        self.bg_array = []
        for i in range(1, 6):
            temp = pygame.image.load(
                st.current_dir() + "/data/other/{}.png".format(str(i))).convert_alpha()
            temp = pygame.transform.scale(temp, (800, 500))
            self.bg_array.append(temp)

    def get_event(self, event, keys):
        if event.type == pygame.QUIT:
            self.st_done = True
            self.quit = True
            pygame.quit()
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
            self.st_done = True
            self.next = "JUEGO"
        if (event.type == pygame.MOUSEBUTTONDOWN and self.arrow_right.getRekt().collidepoint(pygame.mouse.get_pos())) or (event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT):
            if self.i != len(self.strings) - 1:
                self.i += 1
            else:
                self.st_done = True
                self.next = "JUEGO"

    def render(self, clock, screen, p):
        self.i = 0
        self.createBG()
        curr = self.bg_array[0]
        while not self.st_done:
            screen.blit(curr, (0, 0))
            question_text = tt.render_text(
                "S", self.strings[self.i], self.background_color)
            screen.blit(self.fondo.getImg(),
                        (self.fondo.getX(), self.fondo.getY()))
            screen.blit(question_text, (self.fondo.getRekt().center[0] - question_text.get_width(
            ) // 2, self.fondo.getRekt().center[1] - question_text.get_height() // 2))
            self.mostrarFlechas(screen)

            # explicacion de cantidades
            if self.i == 4:
                curr = self.bg_array[1]
            # explicacion sobre cartas de jugador
            if self.i == 8:
                curr = self.bg_array[2]
            # explicacion sobre los oponentes
            if self.i == 12:
                curr = self.bg_array[0]
            # explicacion sobre el ataque/defensa
            if self.i == 19:
                curr = self.bg_array[3]
            # explicacion sobre UP/DOWN y uso de botones
            if self.i == 21:
                curr = self.bg_array[4]
            # las demas explicaciones
            if self.i == 32:
                curr = self.bg_array[0]
            pygame.display.update()
            [self.get_event(event, pygame.key.get_pressed())
             for event in pygame.event.get()]

        temp = pygame.image.load(
        st.current_dir() + "/data/other/game_start3.png").convert_alpha()
        temp = pygame.transform.scale(temp, (800, 500))
        screen.blit(temp, (0, 0))
        pygame.display.update()
