import pygame
import sys_tools as st
import text_tools as tt

from baraja import Baraja
from naipe import Naipe
from jugador import Jugador, JugadorCPU, JugadorHumano
from botonCarta import BotonCarta


'''
class Juego(st.Estados_Juego)
|   
'''

class Juego(st.Estados_Juego): 
    def __init__(self, nJugadores):
        st.Estados_Juego.__init__(self)
        self.nJugadores = nJugadores
        # Crea a los n jugadores (incluyendo al usuario como jugador 0) y los guarda en una lista
        self.jugadores = []
        self.next = "FIN"
        self.st_done = False
        # Muestra la primera carta de la baraja para conseguir el trump
        self.trump = Naipe("Null", 0)
        self.w = 70
        self.h = 103
        self.atacante_count = 0 
        self.defensor_count = 0

        # Se tienen dos identificadores de jugador para no perder el orden de turno al realizar ataques/defensas.
        self.turno = -1 # Indice del jugador al que le corresponde el turno original.
        self.defensor = -1 # Indice del jugador al que le corresponde defender.
        self.atacante = -1  # Indice del jugador al que le corresponde el turno para atacar.
        self.boolAtq = True # boolean que indica el jugador activo. True para atacante, False para defensor.
        self.boolDfs = True # boolean que indica si el defensor tiene cartas para defender.
        self.atacantes = [] # Almacena a los atacantes en orden
        self.endTurn = False # Boolean que indica si termino el turno.
        self.passers = [] # Almacena los atacantes que pasaron su turno 

        self.cartasJugadas = {"ataque": [], "defensa": []}
        self.cartaHumano = Naipe("Null", 0) # Carta que puede jugar el humano, captada por el click en pantalla.

        self.gameFinished = False # Bool que determina si la partida sigue o termina
        self.listpos = 0
        self.manoVisible = []

        # Lista con el nombre de los archivos de las imagenes correspondientes para cada carta en manoVisible
        self.imagesName = []
        self.createOptionButtons()
        self.createJacketsAI()
        self.touchCardflag = False
    '''
    createOptionButtons(self)
    |   Función, que crea los botones para agregar la interactividad al juego.
    '''

    def createOptionButtons(self):
        self.tomar = BotonCarta(600,400,85,40,"tomar_gris.png","tomar_red.png",True)
        self.pasar = BotonCarta(600,430,85,40,"pass_gris.png", "pass_red.png", True)
        self.pause = BotonCarta(720,360,30,30,"stop_gray.png","stop_blue.png",True)
        self.sound = BotonCarta(720,400,30,30,"sound_blue.png","sound_gray.png",True)
        self.music = BotonCarta(720,440,30,30,"music_blue.png","music_gray.png",True)
        self.arrow_up = BotonCarta(600, 370, 30, 30, "up.png", False, False)
        self.arrow_down = BotonCarta(655, 370, 30, 30, "down.png", False, False)
    '''
    createJacketsAI(self)
    |   Función, que crea los jackets de naipes, que representan a los oponentes del usuario.
    |   CONCEPTOS DE CURSO: Funciones de orden superior y lambda. Formas funcionales.
    '''
    def createJacketsAI(self):
        self.pos = [(20, 200), (20, 20), (369, 20), (700, 20), (700, 200)]
        self.bot_ai = list(map(lambda i: BotonCarta(self.pos[i][0], self.pos[i][1],
                      self.w, self.h, "Grey_1.png", "Blue_1.png", False), [i for i in range(5)]))

    '''
    crearJugadores(self, nJugadores)
    |   Función, que crea a los jugadores (representados por
    |   la clase JugadorCPU() y los agrega a la lista de jugadores.
    '''

    def crearJugadores(self, nJugadores):
        jugadores = [JugadorCPU() for id in range(1, nJugadores)]
        jugadores.append(JugadorHumano())
        #Jugador humano siempre en indice 0
        jugadores.reverse()  
        return jugadores

    '''
    crearJugadores(self, nJugadores)
    |   Función, que permite repartir las cartas al inicio de la partida.
    '''
    def repartirCartas(self, atacantes=[], screen=None):  # Repartir cartas al inicio de la partida o al finalizar un ataque
        if len(atacantes) == 0: 
            jugadores = self.jugadores
        else:
            jugadores = atacantes

        repartir = False
        for i in range(len(jugadores)):
            if self.baraja.mostrarCantidad() > 0:
                if jugadores[i].mostrarCantidad() < 6:
                    repartir = True
                    self.jugadores[self.jugadores.index(jugadores[i])].sacarCarta(self.baraja.sacarDeBaraja())

            else:
                repartir = False

        if repartir:
            self.repartirCartas(atacantes, screen)
    '''
    makeTrump(self)
    |   Función, que elige la carta de triunfo.
    '''
    def makeTrump(self):
        if self.nJugadores >= 6:
            return self.baraja.sacarTrumpCon6Jugadores()
        else:
            return self.baraja.sacarTrump()
    '''
    cardOnScreen(self, screen, carta, pos, w=None, h=None)
    |   Función, permite mostrar una carta en la pantalla,
    |   en posición especifica.
    '''

    def cardOnScreen(self, screen, carta, pos, w=None, h=None):
        if (w == None) | (h == None):
            w = self.w
            h = self.h
        img = carta.getImgNaipe(w, h)
        screen.blit(img, pos)


    def getDefensor(self, defensa=-1):
        if defensa == -1:

            if self.turno == (len(self.jugadores) - 1):
                self.defensor = 0
            else:
                self.defensor = self.turno + 1

        else:

            if self.defensor == (len(self.jugadores) - 1):
                self.defensor = 0
            else:
                self.defensor += 1

        if (self.jugadores[self.defensor].mostrarCantidad() == 0) or (self.defensor == self.atacante):
            self.getDefensor(self.defensor)
        self.boolDfs = True

    '''
    actualizarTurno(self, lastTurn = -1)
    |   Función que actualiza el turno, reiniciando
    |   las variables-contadoras y avanzando en lista de jugadores.
    '''
    def actualizarTurno(self, lastTurn=-1):
        self.atacante_count = 0

        self.defensor_count = 0

        if lastTurn == -1:
            self.turno = int(self.defensor)
            if len(self.cartasJugadas["ataque"]) != len(self.cartasJugadas["defensa"]):
                self.actualizarTurno(self.turno)

        else:
            if lastTurn == (len(self.jugadores) - 1):
                self.turno = 0
            else:
                self.turno = lastTurn + 1

        if self.jugadores[self.turno].mostrarCantidad() == 0: # Los jugadores sin cartas en la mano no juegan
            self.actualizarTurno(self.turno)

        if self.atacante == 0:
            cartasPosibles = self.cartasPosibles()

    '''
    actualizarTurno(self, lastTurn = -1)
    |   Función que actualiza el turno, reiniciando
    |   las variables-contadoras y avanzando en lista de jugadores.
    '''

    def nextAtaquer(self):
        if self.atacante == (len(self.jugadores) - 1):
            self.atacante = 0
        else:
            self.atacante += 1

        if self.jugadores[self.atacante].mostrarCantidad() == 0:
            self.nextAtaquer()
            
        if self.atacante == self.defensor:
            self.nextAtaquer()
    '''
    getActivePlayer(self)
    |   Función que retorna al jugador activo.
    '''

    def getActivePlayer(self):
        if self.boolAtq == True:
            return self.atacante
        else:
            return self.defensor
    '''
    makeFirstPlayer(self)
    |   Función que prepara al primer atacante del juego.
    '''
    def makeFirstPlayer(self):
        trumps = [jugador.getLowerTrump(self.trump) for jugador in self.jugadores] # Lista con los menores trump de los jugadores

        self.turno = trumps.index(min(trumps))
        self.atacante = int(self.turno)
        self.boolAtq = True
        self.getDefensor()
        if self.atacante == 0:
            cartasPosibles = self.cartasPosibles()
    '''
    changeActive(self)
    |   Función que cambia al jugador activo.
    '''
    def changeActive(self):
        if self.boolAtq and self.boolDfs:
        # Si boolDfs es falso, el defensor no tiene para defender por lo tanto no tendra mas turnos

            self.boolAtq = False
        else:
            self.boolAtq = True

    '''
    checkGame(self)
    |   Función que revisa el estado de juego. Si el juego termino,
    |   se asigna el valor al durak, el cual corresponde al indice del jugador.
    '''
    def checkGame(self):
        cantNaipes = [jugador.mostrarCantidad() for jugador in self.jugadores]
        if cantNaipes.count(0) == (len(self.jugadores) - 1):
            # 1 jugador quedo con cartas en su mano
            self.gameFinished = True
            for i in range(len(cantNaipes)):
                if cantNaipes[i] != 0:
                    self.durak = i
        elif cantNaipes.count(0) == len(self.jugadores):
            # todos los jugadores quedaron con 0 cartas (draw)
            self.gameFinished = True
            self.durak = -1

        return self.gameFinished

    '''
    play(self, posicion, screen, carta="pass")
    |   La función base de la clase. Se usa los booleanos self.boolDfs y self.boolAtq
    |   para analizar cada caso de evento en juego, según las reglas del Durak.
    '''
    def play(self, posicion, screen, carta="pass"):
        self.playCard = pygame.mixer.Sound('data/other/card-deal.wav')
        pos_zona = [(180,180), (250,180), (320, 180),(390, 180), (460, 180), (530,180)]
        pos_zona_desfase = [(190,220),(260,220),(330, 220),(400, 220),(470, 220),(550,220)]
        # Maneja la continuidad de los turnos
        if posicion == self.atacante and len(self.passers) > 0:
            if posicion == self.passers[0]:

                self.endTurn = True
                self.atacante_count = 0
                self.defensor_count = 0
                self.passers = []
                self.refreshUI(screen)
                return
        if posicion != 0: 
            # Si es la cpu consigue la carta a jugar de manera interna, a diferencia del humano.

            carta = self.jugadores[posicion].jugarCarta(self.cartasJugadas, self.trump, self.boolAtq)
            self.refreshUI(screen)
        
        else:

            self.jugadores[posicion].jugarCarta(carta) 
            # Elimina la carta de la mano del humano.
        if carta == "pass":

            if posicion == self.defensor:
                self.boolDfs = False 
                # Ya no puede seguir defendiendo.
                self.changeActive()

            else:
                self.nextAtaquer() 
                # Ya no tiene cartas para atacar -> pasa al siguiente atacante.

                if self.jugadores[posicion].mostrarCantidad() > 0:
                    self.passers.append(posicion)
        else:
            if posicion == self.defensor:
                self.cartasJugadas["defensa"].append(carta)
                if self.defensor_count < 6:
                    self.cardOnScreen(screen, carta, pos_zona_desfase[self.defensor_count], 55, 83)
                    self.defensor_count += 1
                if self.defensor_count ==  6:
                    self.defensor_count = 0

                self.playCard.play()
                self.changeActive()

                if posicion == 0:
                    self.refreshUI(screen)
                else:
                    self.actualizarMano(self.defensor)

            else:
                self.cartasJugadas["ataque"].append(carta)
                self.atacantes.append(self.jugadores[posicion])

                if self.atacante_count < 6:
                    self.cardOnScreen(screen, carta, pos_zona[self.atacante_count], 55, 83)
                    self.atacante_count += 1
                if self.atacante_count == 6:
                    self.atacante_count = 0

                self.passers = []
                self.changeActive()
                self.playCard.play()
                if posicion == 0:
                    self.refreshUI(screen)
                else:
                    self.actualizarMano(self.atacante)

        if self.getActivePlayer() == 0 and len(self.cartasJugadas["ataque"]) != 6:
            if self.boolAtq == True:
                cartasPosibles = self.cartasPosibles()
                
            else:
                cartasPosibles = self.cartasPosibles()
        self.refreshUI(screen)

    '''
    game(self, screen)
        La función central de la clase juego, la cuál maneja el flow de juego.
        CONCEPTOS DE CURSO: Funciones de orden superior y lambda.
    '''
    def game(self, screen):
        self.receiveCards = pygame.mixer.Sound('data/other/card-bridge.wav')
        if self.boolDfs == False:
            x = lambda carta: self.jugadores[self.defensor].sacarCarta(carta)
            if(len(self.cartasJugadas["ataque"] + self.cartasJugadas["defensa"]) > 0 ): 
                self.receiveCards.play()
            for carta in self.cartasJugadas["ataque"] + self.cartasJugadas["defensa"]:
                x(carta)
            if self.defensor == 0:
                self.refreshUI(screen)
            else:
                self.actualizarMano(self.defensor)

        self.endTurn = False
        # Revisa si la partida termino.
        self.checkGame()
        if not self.gameFinished:
            # Avanzar los turnos.
            self.actualizarTurno()
            self.atacante = int(self.turno)
            self.getDefensor()
            self.boolAtq = True
            self.boolDfs = True
            self.cartasJugadas = {"ataque": [], "defensa": []}
            # Future proof
            self.repartirCartas(self.atacantes, screen)
            self.repartirCartas([self.jugadores[self.defensor]], screen)
            self.atacantes = []

    '''
    cartasPosibles(self)
    |   Función que retorna lista con las cartas de la mano del humano que se pueden jugar en este turno
    '''
    def cartasPosibles(self):
        return self.jugadores[0].posiblesCartas(self.cartasJugadas, self.trump, self.atacante == 0)   

    '''
    cartasPosibles(self)
    |   Función que retorna lista con nombres de .png de cartas en la mano visible.
    |   CONCEPTOS DE CURSO: Comprensión de Listas.
    '''
    def getImagesName(self):
        return [carta.fileNaipe() for carta in self.manoVisible]

    '''
    avanzarListPos(self, action)
    |   Función que permite avanzar por la lista de las cartas del jugador,
    |   visible en la parte inferior de la pantalla. Se usa paso de a 3.
    '''
    def avanzarListPos(self, action):
        # usaremos cantidad para acotar cuantas veces se puede bajar/subir
        canti = self.jugadores[0].mostrarCantidad()
        if action: 
            # True == down

            if (canti % 3) == 0:
                if self.listpos >= int(canti / 3) - 1:
                    self.listpos = 0
                else:
                    self.listpos += 1
            else:
                if (self.listpos >= int(canti/3)):

                    self.listpos = 0
                else:
                    self.listpos += 1

        else:
            # False == up
            if self.listpos > 0:
                self.listpos -= 1
            elif self.listpos == 0:

                if (canti % 3) == 0:
                    self.listpos = int(canti / 3) - 1
                else:
                    self.listpos = int(canti/3)

    '''
    revisarJugada(self, naipe)
    |   Revisa la jugada, mientras no se ha atacado con 6 cartas. Para el humano se revisan las cartas 
    |   posibles para el ataque o la defensa.
    '''
    def revisarJugada(self, naipe):

        if (len(self.cartasJugadas["ataque"]) < 6 or not self.boolAtq) and not self.gameFinished and not self.endTurn:
            # Humano
            if (self.atacante == 0 and self.boolAtq) or ((self.defensor == 0 and self.boolAtq) and self.boolDfs):
                cartasPosibles = self.cartasPosibles()
                if len(cartasPosibles) > 0:
                    if naipe.printNaipe() in [carta.printNaipe() for carta in cartasPosibles]:
                        for carta in cartasPosibles:
                            if naipe.printNaipe() == carta.printNaipe():
                                self.cartaHumano = carta
                                return True
                    return False
    '''
    actualizarMano(self, indice)
    |   Funcion para actualizar el numero de cartas que muestra cada jugador.
    '''
    def actualizarMano(self, indice):
        nuevo_texto = tt.render_text("T", str(self.jugadores[indice].mostrarCantidad()), self.white)
        self.cant_Textos.remove(self.cant_Textos[indice])
        self.cant_Textos.insert(indice, nuevo_texto)

    '''
    get_event(self, event, keys)
    |   Función, que analiza los eventos de juego. Al cerrar la ventana (ESC),
    |   el evento corresponde a pygame.QUIT y se termina la ejecución del código.
    |   En caso de pasar el mouse por cualquiera de las cartas de la lista, y en caso de que
    |   una de los naipes sea válido para ataque o defensa, se aplicara self.botón.mouseOverButton,
    |   elevando la carta de la lista.
    |
    |   En caso de usar el botón de pause o presionar SPACE, el juego se pausea.
    |
    |   En caso de usar flechas, estas se activan con teclas arriba o abajo, o con mouse, y permiten
    |   desplazarse por la lista de cartas del usuario.
    |
    |   En caso de usar botón tomar o pasar, al ser estos activos, se ponen grises (inactivos).
    |
    |   Al usar botón de sonidos, se apaga todo, excepto los sonidos de las cartas.
    |
    |   Al usar botón de música, se baja el sonido.
    '''
    def get_event(self, event, keys, screen):
        # Carta 1
        if self.u1.getRekt().collidepoint(pygame.mouse.get_pos()) and self.revisarJugada(self.u1.makeNaipe()) and self.checkGame() != True and self.mode_pause:   

            
            self.u1.mouseOverButton(True, 340)
            self.touchCardflag = True
           

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.play(0, screen, self.cartaHumano)
        else:
            self.u1.mouseOverButton(False, 370)
            

        # Carta 2

        if self.u2.getRekt().collidepoint(pygame.mouse.get_pos()) and self.revisarJugada(self.u2.makeNaipe()) and self.checkGame() != True and self.mode_pause:   

            self.touchCardflag =  True
            self.u2.mouseOverButton(True, 340) 

            if event.type == pygame.MOUSEBUTTONDOWN:

                self.play(0, screen, self.cartaHumano)
        else:
            self.u2.mouseOverButton(False, 370)

        # Carta 3
        if self.u3.getRekt().collidepoint(pygame.mouse.get_pos()) and self.revisarJugada(self.u3.makeNaipe()) and self.checkGame() != True and self.mode_pause:   

            self.touchCardflag =  True
            self.u3.mouseOverButton(True, 340) 

            if event.type == pygame.MOUSEBUTTONDOWN:

                self.play(0, screen, self.cartaHumano)
        else:
            self.u3.mouseOverButton(False, 370)


        # Volúmen:
        if self.sound.getRekt().collidepoint(pygame.mouse.get_pos()):
            self.sound.isActivePlayer(True)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.volume == 1:
                    self.volume = 2
                    pygame.mixer.music.set_volume(0.7)
                elif self.volume == 2:
                    self.volume = 3
                    pygame.mixer.music.set_volume(0.3)
                elif self.volume == 3:

                    self.volume = 0
                    pygame.mixer.music.set_volume(0.0)
                else:
                    self.volume = 1
                    pygame.mixer.music.set_volume(1.0)
        else:
            self.sound.isActivePlayer(False)

        # Pausar musica:
        if self.music.getRekt().collidepoint(pygame.mouse.get_pos()):
            self.music.isActivePlayer(True)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.pauseMusic == False: 
                    # Esta sonando el bgm.
                    self.pauseMusic = True
                    pygame.mixer.music.pause()
                else:
                    self.pauseMusic = False
                    pygame.mixer.music.unpause()
        else:
            self.music.isActivePlayer(False)


        # Si el humano no tiene cartas validas para jugar:
        if (not self.atacante or not self.defensor) and not self.checkGame() and self.mode_pause:
            #Humano es el defensor, puede tomar cartas en cualquier momento (no solo si no pueda defenderse). Tecla: t.

            if not self.defensor and self.boolDfs:
                self.tomar.isActivePlayer(True)
                if (self.tomar.getRekt().collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN) or (event.type == pygame.KEYDOWN and event.key == pygame.K_t):
                    self.play(0, screen, "pass")
                    self.tomar.isActivePlayer(False)
            #Humano es un atacante, decide por su cuenta si atacar o pasar el turno. Tecla : p.
            elif not self.atacante and self.boolAtq:
                self.pasar.isActivePlayer(True)
                if (self.pasar.getRekt().collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN) or (event.type == pygame.KEYDOWN and event.key == pygame.K_p):
                    self.play(0, screen, "pass")
                    self.pasar.isActivePlayer(False)


        # Para las flechas:

        if (event.type == pygame.KEYDOWN and event.key == pygame.K_UP) or (event.type == pygame.MOUSEBUTTONDOWN and self.arrow_up.getRekt().collidepoint(pygame.mouse.get_pos())) and self.mode_pause:
            self.avanzarListPos(False)
            self.manoVisible = self.jugadores[0].manoAcotada(self.listpos)
            self.refreshUI(screen)

        if (event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN) or (event.type == pygame.MOUSEBUTTONDOWN and self.arrow_down.getRekt().collidepoint(pygame.mouse.get_pos())) and self.mode_pause:
            self.avanzarListPos(True)
            self.manoVisible = self.jugadores[0].manoAcotada(self.listpos)
            self.refreshUI(screen)


        #En juego se para al presionar SPACE o al usar el botón de pause.
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or (event.type == pygame.MOUSEBUTTONDOWN and self.pause.getRekt().collidepoint(pygame.mouse.get_pos())):
            if self.mode_pause:
                self.mode_pause = False 
            else:
                self.mode_pause = True

        #Término de juego.        

        if self.gameFinished == True:
            self.st_done = True
            self.next = "FIN"
            pygame.mixer.music.stop()

        if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            self.quit = True
            pygame.quit()
            quit()


        self.actualizarMano(0)
    '''
    mostrarTrump(self, screen)
    |   Función que muestra la carta de triunfo en la
    |   esquina inferior izquiera de la pantalla.
    '''

    def mostrarTrump(self, screen):
        trumpImg = self.t1.getImg()
        trump_text = tt.render_text(
            "T", "Triunfo: " + self.trump.printNaipe(), self.white)
        screen.blit(trump_text, (self.t1.getX() - 65, self.t1.getY() - 18))
        screen.blit(trumpImg, (self.t1.getX(), self.t1.getY()))

    '''
    refreshUI(self, screen=None)
    |   Función, responsable de refresh de la la lista de naipes del usuario.
    '''
    def refreshUI(self, screen=None):

        canti = self.jugadores[0].mostrarCantidad()
        if canti == 0:
            self.listpos = 0
        else:
            if self.listpos == int(canti / 3):
                if canti % 3 == 0:
                    self.listpos = 0

            if self.listpos > int(canti / 3):
                self.listpos = 0

        self.manoVisible = self.jugadores[0].manoAcotada(self.listpos)
        self.u1 = BotonCarta(267, 370, self.w, self.h,
                            self.manoVisible[0].fileNaipe(), False, True)
        self.u2 = BotonCarta(369, 370, self.w, self.h,
                                self.manoVisible[1].fileNaipe(), False, True)
        self.u3 = BotonCarta(471, 370, self.w, self.h,
                            self.manoVisible[2].fileNaipe(), False, True)

        self.actualizarMano(0)

    '''
    mostrarCantidadNaipes(self, screen, listaTextos)
    |   Función que muestra la cantidad de naipes de cada jugador AI.
    |   CONCEPTOS DE CURSO: Funciones de orden superior. Formas funcionales.
    '''

    def mostrarCantidadNaipes(self, screen, listaTextos):
        screen.blit(listaTextos[0],(self.u2.getX() + 33, self.u2.getY() + 107))
        list(map(lambda i: screen.blit(listaTextos[i + 1], (self.bot_ai[i].getX(
        ) + 33, self.bot_ai[i].getY() + 107)), [i for i in range(5)]))

    '''
    mostrarOponentes(self, screen)
    |   Función que muestra los jackets de oponentes del usuario.
    |   CONCEPTOS DE CURSO: Funciones de orden superior. Formas funcionales.
    '''
    def mostrarOponentes(self, screen):
        list(map(lambda i: screen.blit(self.bot_ai[i].getImg(),
            (self.bot_ai[i].getX(), self.bot_ai[i].getY())), [i for i in range(5)]))

    '''
    gameStart(self, screen)
    |   Función responsable de inciar el juego. Se crea la baraja, se reparte
    |   las cartas, se genera la mano visible del usuario y la lista interactiva.
    '''
    def gameStart(self, screen):
        self.jugadores = self.crearJugadores(self.nJugadores)
        self.baraja = Baraja() 
        # Crea la baraja para la partida
        self.repartirCartas(self.jugadores, screen)
        self.trump = self.makeTrump()
        self.makeFirstPlayer()
        self.manoVisible = self.jugadores[0].manoAcotada(self.listpos)
        # Lista con el nombre de los archivos de las imagenes.
        self.imagesName = self.getImagesName()
        self.manoVisible = self.jugadores[0].manoAcotada(self.listpos)
        #Los tres botones de la lista interactiva  de naipes del usuario.

        self.u1 = BotonCarta(267, 370, self.w, self.h,
                             self.manoVisible[0].fileNaipe(), False, True)
        self.u2 = BotonCarta(369, 370, self.w, self.h,
                             self.manoVisible[1].fileNaipe(), False, True)
        self.u3 = BotonCarta(471, 370, self.w, self.h,

        # t1 es la carta de triunfo.
        self.t1 = BotonCarta(
            100, 400, 50, 67, self.trump.fileNaipe(), False, False)
    '''
    mostrarFlechas(self, screen)
    |   Función que muestra los dos botónes-flechas, usadas para desplazar en la lista.
    '''
    def mostrarFlechas(self, screen):
        screen.blit(self.arrow_down.getImg(), (self.arrow_down.getX(), self.arrow_down.getY()))
        screen.blit(self.arrow_up.getImg(), (self.arrow_up.getX(), self.arrow_up.getY()))
    '''
    mostrarTomar(self, screen)
    |   Función que muestra el botón de tomar.
    '''
    def mostrarTomar(self, screen):
        screen.blit(self.tomar.getImg(),(self.tomar.getX(),self.tomar.getY()))
    '''
    mostrarPasar(self, screen)
    |   Función que muestra el botón de pasar.
    '''
    def mostrarPasar(self, screen):
        screen.blit(self.pasar.getImg(),(self.pasar.getX(),self.pasar.getY()))
    '''
    mostrarOptions(self, screen)
    |   Función, en la cual se llama a blit para mostrar los 3 botones, de la
    |   parte derecha de la zona de usuario. Los botones corresponden a:
    |   pausar, bajar el volúmen, apagar el BGM.
    '''

    def mostrarOptions(self, screen):
        screen.blit(self.pause.getImg(),(self.pause.getX(),self.pause.getY()))
        screen.blit(self.music.getImg(),(self.music.getX(),self.music.getY()))
        screen.blit(self.sound.getImg(),(self.sound.getX(),self.sound.getY()))

    '''
    generarCantidades(self)
    |   Genera la lista de textos, que corresponden a cantidades de naipes en la mano de cada jugador.
    |   CONCEPTOS DE CURSO: Formas funcionales. Funciones de orden superior.
    '''

    def generarCantidades(self):
        cant_Textos = list(map(lambda i: tt.render_text("T", str(self.jugadores[i].mostrarCantidad()), self.white), [i for i in range(1, 6)]))
        cant_Textos.insert(0, tt.render_text("S", str(self.jugadores[0].mostrarCantidad()), self.white))
        return cant_Textos


    '''
    updateParcial(self, screen, p)
    |   Función, en la cual se muestra rectángulos en la pantalla,
    |   de color de fondo, para cubrir el rastreo de los números de
    |   las cartas en la mano de cada AI.
    '''

    def updateParcial(self, screen, p):
        screen.fill(self.background_color,(0,0,p[0],p[1]//2 - 100))
        screen.fill(self.background_color,(0,p[1]//2 + 100,p[0],p[1]//2 + 100))
        screen.fill(self.background_color,(0,0,p[0]//2 - 300,p[1]))
        screen.fill(self.background_color,(p[0]//2 + 300,0,p[0]//2,p[1]))


    '''
    updateZonaHumano(self, screen, p)
    |   Función, en la cual se muestra un rectángulo en la pantalla,
    |   de color de fondo, para cubrir el rastreo de las cartas 
    |   interactivas en la zona del humano.
    '''
    def updateZonaHumano(self, screen, p):
        screen.fill(self.background_color,(0,p[1]//2 + 70,p[0],p[1]//2)) 

    '''
    turnoCPU(self, screen)
    |   Función, en la cual se basa el comportamiento de los AI's.
    |   Además, se ocupa pygame.wait(450) para que los AI's no
    |   jueguen demasiado rápido.
    '''
    def turnoCPU(self, screen): 
        if not self.checkGame():
            pygame.time.wait(450)
            if self.boolAtq:
            #Turno de atacante
                self.play(self.atacante, screen)
            else:
                if self.boolDfs:
                    #Turno de defensor

                    self.play(self.defensor, screen)
    '''
    checkTurn(self, jugadorActual, screen)d
    |   Función que revisa el turno. Este termina si todos pasan la ronda,
    |   es decir, no tienen cartas para atacar o si las cartas en la mesa
    |   llegan a ser 6 o el defensor se queda sin poder defenderse.
    '''
    def checkTurn(self, jugadorActual, screen):
        if jugadorActual == self.atacante and len(self.passers) > 0: 
            if jugadorActual == self.passers[0]: 
            # Si todos pasan la ronda
                self.endTurn = True
                self.atacante_count = 0
                self.defensor_count = 0
                self.passers = []

        if (self.jugadores[self.defensor].mostrarCantidad() == 0) or (len(self.cartasJugadas["ataque"]) == 6 and self.boolAtq):

            self.endTurn = True 
            # Si el defensor se queda sin cartas o las cartas jugadas en ataque llegan a 6
            self.atacante_count = 0
            self.defensor_count = 0
            self.passers = []

    '''
    gameMusic(self)
    |   Función responsable de la música de fondo del juego.
    '''
    def gameMusic(self):
        pygame.mixer.music.load("data/other/bgm.mp3") 
        self.touchCard = pygame.mixer.Sound('data/other/card-flip.wav')
        self.touchPlayed = False

        self.volume = 1
        self.pauseMusic = False 

        pygame.mixer.music.play(-1,0.0)


    '''
    render(self)
    |   Función render, utilizada para mostrar la media y texto en la pantalla.
    |   Se utiliza funcion blit() para mostrar el texto de creditos
    |   en posición indicada.
    |   Admeas, para lograr el efecto de "flashing text" en pause, se usa una 
    |   lista de colores, propia a la clase st.Estados_Juego.
    |   La funcion conteien dos loops, el while not self.st_done es el loop, 
    |   que corre mientras el juego no termina. El segundo loop anidado es el 
    |   loop, que corresponde al caso cuando el jugador presiona el boton space
    |   y pausa el juego. Mientras no se presiona space de nuevo, no se volvera a
    |   jugar.
    |   CONCEPTOS DE CURSO: Comprensión de listas.
    '''

    def render(self, clock, screen, p):
        #se inicia sin pausar el juego
        self.gameMusic()
        self.mode_pause = True
        screen.fill(self.background_color)
        # Inicializa valores para el juego
        self.gameStart(screen) 
        # Mano del humano muestra 3 cartas
        self.cant_Textos = self.generarCantidades()
        self.refreshUI(screen)   
        #Mientras el juego sigue:
        while not self.st_done:

            if self.mode_pause:
                #Dibuja mano de jugador, que siempre permanece en la pantalla.

                self.cardOnScreen(
                    screen, self.manoVisible[0], (self.u1.getX(), self.u1.getY()))
                self.cardOnScreen(
                    screen, self.manoVisible[1], (self.u2.getX(), self.u2.getY()))
                self.cardOnScreen(
                    screen, self.manoVisible[2], (self.u3.getX(), self.u3.getY()))

                self.mostrarOponentes(screen)
                # Debajo de cada carta, se imprime la cantidad de naipes de cada jugador.
                self.mostrarCantidadNaipes(screen, self.cant_Textos)
                # Muestra la trump
                self.mostrarTrump(screen)

                # Muestra las felchas
                self.mostrarFlechas(screen)
                # Muestra el boton tomar
                self.mostrarTomar(screen)
                # Muestra el boton pasar
                self.mostrarPasar(screen)
                # Muestra el boton de pausar,musica y sonidos
                self.mostrarOptions(screen)
                pygame.display.update()
                if self.boolAtq: self.checkTurn(self.atacante, screen)               
                if not ((self.atacante == 0 and self.boolAtq) or ((self.defensor == 0 and not self.boolAtq) and self.boolDfs) and not self.checkGame()):
                    if not self.endTurn: self.turnoCPU(screen)         
                if self.boolAtq: self.checkTurn(self.atacante, screen)

                #Una vez que termine la ronda, borramos las cartas de la zona de ataque, y reiniciamos el turno.
                if (len(self.cartasJugadas["ataque"]) == 6 and self.boolAtq) or self.endTurn:
                    self.game(screen)
                    screen.fill(self.background_color)

            else:
                #El jugador presionó SPACE o usó el botón en la pantalla, para pausar el juego.
                pause_text = tt.render_text("M", "PAUSE", self.white)
                count = 0
                while not self.mode_pause:
                    #Se rellena la pantalla, formando un arco, que no cubre zona de ataque central, conservando las cartas.

                    self.updateParcial(screen, p)
                    screen.blit(pause_text, (p[0]/2 - pause_text.get_width()//2, 20))
                    term_text = tt.render_text("S", ">Presione SPACE para volver a jugar...", self.white_to_bg_fade[count % len(self.white_to_bg_fade)])
                    screen.blit(term_text, (p[0]/2 - term_text.get_width() //
                                    2, p[1] - term_text.get_height() - 100// 2))
                    pygame.display.flip()
                    count += 1
                    clock.tick(5)
                    [self.get_event(event, pygame.key.get_pressed(), screen) for event in pygame.event.get()]    
            [self.get_event(event, pygame.key.get_pressed(), screen) for event in pygame.event.get()]

            self.updateParcial(screen, p)
            self.updateZonaHumano(screen, p)
            