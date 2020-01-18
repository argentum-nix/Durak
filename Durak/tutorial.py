import pygame
import sys_tools as st
import text_tools as tt
from botonCarta import BotonCarta

'''
class Tutorial(st.Estados_Juego)
|   Clase, correspondiente a la fase de tutorial.
|   Usando un array, se muestra una ventana con la instruccion.
|   Una vez terminadas las instrucciones, el usuario procederá
|   a jugar.
'''


class Tutorial(st.Estados_Juego):
    def __init__(self):
        st.Estados_Juego.__init__(self)
        self.fondo = BotonCarta(200, 100, 407, 251, "window.png", False, False)
        self.arrow_right = BotonCarta(self.fondo.getX(
        ) + 330, self.fondo.getY() + 190, 30, 30, "right.png", False, False)
        self.strings = ["Hola!", "Bienvenido al juego Durak.", "Las reglas son:", "1.No quedar con cartas", "Número debajo de los naipes", "Representa la cantidad de cartas", "que tiene el jugador.",
                        "El que queda el último, pierde.", "2.Se juega de a 6 personas.", "3.Mejor pinta: Trinufo", "Última carta de la baraja", "Gana a toda otra pinta", "4.El primer atacante es el que",
                        "posee el menor trinufo.", "5.Se ataca con cualquier carta", "Pero la defensa es más compleja:", "Se defiende con:", "Triunfo de mayor valor,", "O carta mayor de la misma pinta",
                        "Las cartas, válidas para usar", "Serán interactivas", "6.Para ver sus cartas", "Use UP y DOWN", "o haga click sobre los botones.", "Se puede pasar el ataque", "guardando las cartas", "para pasar, presione P",
                        "o haga click en el botón", "En caso de no poder defenderse", "Hay que tomar las cartas", "Para hacerlo, presione T", " O haga el click en el botón", "Use el menu para apagar", "la música o los sonidos",
                        "Presione SPACE para", "pausar el juego en el caso", "de que sea necesario", "Suerte!"]

    '''
    mostrarFlechas(self, screen, x=None, y=None)
    |   Función, que muestra el botón- flecha en la pantalla en un lugar específico.
    '''

    def mostrarFlechas(self, screen, x=None, y=None):
        if x == None and y == None:
            x = self.arrow_right.getX()
            y = self.arrow_right.getY()
        right = self.arrow_right.getImg()
        screen.blit(right, (x, y))

    '''
    createBG(self)
    |   Función que renderiza el fondo según la parte de tutorial, en que esta en usuario.
    '''

    def createBG(self):
        self.bg_array = []
        for i in range(1, 6):
            temp = pygame.image.load(
                st.current_dir() + "/data/other/{}.png".format(str(i))).convert_alpha()
            temp = pygame.transform.scale(temp, (800, 500))
            self.bg_array.append(temp)
    '''
    get_event(self, event, keys)
    |   Función, que analiza los eventos de juego. Al cerrar la ventana (ESC),
    |   el evento corresponde a pygame.QUIT y se termina la ejecución del código.
    |   En caso de presionar tecla right arrow o botón de la pantalla, se avanza en
    |   la lista de instrucciones. En caso de querer saltar el tutorial, se puede 
    |   hacerlo, presionando SPACE.
    '''

    def get_event(self, event, keys):
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            self.st_done = True
            self.quit = True
            pygame.quit()
            exit()
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
            self.st_done = True
            self.next = "JUEGO"
        if (event.type == pygame.MOUSEBUTTONDOWN and self.arrow_right.getRekt().collidepoint(pygame.mouse.get_pos())) or (event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT):
            if self.i != len(self.strings) - 1:
                self.i += 1
            else:
                self.st_done = True
                self.next = "JUEGO"
    '''
    render(self)
    |   Función render, utilizada para mostrar la media y texto en la pantalla.
    |   Muestra la ventana y la instruccion, correspondiente a la posicion en la
    |   lista de instruccuiones self.strings. Además, el fondo de pantalla 
    |   tambien cambia, en funcion de la instruccion/posicion en self.strings.
    |   CONCEPTOS DE CURSO: Comprensión de listas.
    '''

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
            screen.blit(question_text, (self.fondo.getRekt().center[0] - question_text.get_width() // 2,
                                        self.fondo.getRekt().center[1] - question_text.get_height() // 2))
            self.mostrarFlechas(screen)

            # Explicación de cantidades
            if self.i == 4:
                curr = self.bg_array[1]
            # Explicación sobre cartas de jugador
            if self.i == 8:
                curr = self.bg_array[2]
            # Explicación sobre los oponentes
            if self.i == 12:
                curr = self.bg_array[0]
            # Explicación sobre el ataque/defensa
            if self.i == 19:
                curr = self.bg_array[3]
            # Explicación sobre UP/DOWN y uso de botones
            if self.i == 21:
                curr = self.bg_array[4]
            # Expliaciones que quedan.

            if self.i == 32:
                curr = self.bg_array[0]
            pygame.display.update()
            [self.get_event(event, pygame.key.get_pressed())
             for event in pygame.event.get()]
        # Pantalla de "loading..."
        temp = pygame.image.load(
            st.current_dir() + "/data/other/game_start3.png").convert_alpha()
        temp = pygame.transform.scale(temp, (800, 500))
        screen.blit(temp, (0, 0))
        pygame.display.update()
