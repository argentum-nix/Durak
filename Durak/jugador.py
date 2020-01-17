import random
from naipe import Naipe
from baraja import Baraja
import sys_tools as st
import operator

'''
class Jugador:
 |  Clase, que modela a un jugador cualquiera.
 |  Dado que los jugadores Humano y AI se difieren en implementación
 |  de los métodos, pero los comparten entre si, la clase
 |  Jugador juega el rol de clase 'abstracta'.
'''


class Jugador(object):
    def __init__(self):
        self.esHumano = ""
    '''
    isHuman(self)
    |   Función de tipo get() que retorna si el jugador es humano o no.
    '''

    def sacarCarta(self, nuevaCarta):
        pass
    '''
    mostrarCantidad(self)
    |   Definición abstracta' de función mostrarCantidad.
    '''

    def mostrarCantidad(self):
        pass
    '''
    jugarCarta(self, indice)
    |   Definición 'abstracta' de función jugarCarta.
    '''

    def jugarCarta(self, indice):
        pass
    '''
    getLowerTrump(self)
    |   Definición 'abstracta' de función getLowerTrump.
    '''

    def getLowerTrump(self):
        pass


'''
class JugadorHumano(Jugador)
 |  Clase, que deriva directamente de Jugador y 
 |  es responsable de modelar el comportamiento del usuario.
'''


class JugadorHumano(Jugador):
    def __init__(self):
        Jugador.__init__(self)
        self.esHumano = True
        self.mano = []
    '''
    sacarCarta(self, nuevaCarta)
    |   Agrega una carta a la mano del usuario.
    '''

    def sacarCarta(self, nuevaCarta):
        self.mano.append(nuevaCarta)
    '''
    mostrarCantidad(self)
    |   Retorna la cantidad de cartas del usuario.
    '''

    def mostrarCantidad(self):
        return len(self.mano)

    '''
    posiblesCartas(self, listaCartasEnJuego, trump, boolAtaque)
    |   Retorna todas las cartas, con las cuales puede defenderse o atacar el usuario.
    |   La elección de cartas sigue las reglas de juego:
    |
    |   Si el jugador es atacante, tiene libre elección de cartas y puede atacar con 
    |   cualquiera al inicio, y después de primer ataque, solo con los de valor de 
    |   cartas, que ya estan en la mesa.
    |
    |   En caso de la defensa, se puede defenderse solo con las cartas de misma pinta
    |   y mayor valor (por ejemplo, si se defiende en contra de K de Corazones, sirve
    |   cualquier triunfo o solo A de Corazones) o el trump de cualquier valor contra 
    |   toda pinta que no sea de truinfo. Para defenderse contra carta de triunfo, se
    |   puede ocupar solo cartas de triunfo de mayor valor, que la de que se defiende.
    '''

    def posiblesCartas(self, listaCartasEnJuego, trump, boolAtaque):
        posiblesCartas = []  # Almacena todas las cartas que se pueden jugar en una lista
        if boolAtaque == True:

            # Significa que este es el primer ataque, todo vale
            if (len(listaCartasEnJuego["defensa"]) == 0) and (len(listaCartasEnJuego["ataque"]) == 0):
                return self.mano

            else:
                # Significa que hay cartas en juego, solo se pueden jugar cartas de igual rank.
                ranks = []
                # Almacena el valor numerico de las cartas en juego.

                for carta in listaCartasEnJuego["defensa"] + listaCartasEnJuego["ataque"]:
                    if int(carta.valorNaipe()) not in ranks:
                        # Agrega el valor del naipe de las cartas en juego a la lista ranks.
                        ranks.append(int(carta.valorNaipe()))

                for carta in self.mano:
                    if carta.valorNaipe() != '' and int(carta.valorNaipe()) in ranks:
                        posiblesCartas.append(carta)

        else:
            # Toca defender, solo se puede jugar cartas de igual o mayor rank e igual caliificación.
            # Ultima carta jugada/Carta del atacante al defensor.
            lastCard = listaCartasEnJuego["ataque"][-1]

            for carta in self.mano:
                if carta.valorNaipe() != '':
                    if (int(carta.valorNaipe()) >= int(lastCard.valorNaipe())) and (carta.calificacionNaipe() == lastCard.calificacionNaipe()):
                        posiblesCartas.append(carta)
                    # Si la ultima carta jugada no es de triunfo:
                    elif not lastCard.isTrump(trump.calificacionNaipe()):
                        if carta.isTrump(trump.calificacionNaipe()):
                            posiblesCartas.append(carta)

        return posiblesCartas
    '''
    jugarCarta(self, indice)
    |   Juega la carta, borrandola de la mano del usuario.
    '''

    def jugarCarta(self, carta):
        if carta != "pass":
            del self.mano[self.mano.index(carta)]
    '''
    getLowerTrump(self)
    |   Retorna el menor naipe de triunfo.
    '''

    def getLowerTrump(self, trump):
        lower = 15
        for naipe in self.mano:
            if naipe.isTrump(trump) and int(naipe.valorNaipe()) < lower:
                lower = naipe.valorNaipe()
        return lower

    '''
    rellnarMano(self)
    |   Dado que se ocupa una lista, que va de a tres cartas,
    |   y siempre queremos ver 3 cartas en la pantalla, en caso de 
    |   no tener cantidad, divisible por 3, la mano del jugador se 
    |   rellena con cartas NULL hasta que sea divisible por tres.
    |   Por ejemplo, si el jugador tiene 4 cartas, se agregarán 2 NULL's.
    '''

    def rellenar(self):
        relleno = []
        if self.mostrarCantidad() == 0:
            return [Naipe("Null", 0), Naipe("Null", 0), Naipe("Null", 0)]
        while((len(relleno) + len(self.mano)) % 3 != 0):
            relleno.append(Naipe("Null", 0))
        return relleno
    '''
    manoAcotada(self, mult)
    |   Retorna el slice de 3 naipes, las cuales se mostraran en zona 
    |   interactiva del humano.
    '''

    def manoAcotada(self, mult):
        return (self.mano + self.rellenar())[0 + (3 * mult): 3 + (3 * mult)]


'''
class Jugador:
 |  Clase, que modela a un jugador cualquiera.
 |  Dado que los jugadores Humano y AI se difieren en implementación
 |  de los métodos, pero los comparten entre si, la clase
 |  Jugador juega el rol de clase 'abstracta'.
'''


class JugadorCPU(Jugador):
    def __init__(self):
        Jugador.__init__(self)
        self.esHumano = False
        self.mano = {"Picas": [], "Corazones": [],
                     "Tréboles": [], "Diamantes": []}
    '''
    mostrarCantidad(self)
    |   Retorna la cantidad de cartas del usuario.
    '''

    def mostrarCantidad(self):
        return len(self.mano["Picas"]) + len(self.mano["Corazones"]) + len(self.mano["Tréboles"]) + len(self.mano["Diamantes"])
    '''
    sacarCarta(self, nuevaCarta)
    |   Agrega una nueva carta a la mano de AI. Además, las cartas se ordenan
    |   según su valor y calificación.
    |   CONCEPTOS DE CURSO: Formas funcionales: lambda.
    '''

    def sacarCarta(self, nuevaCarta):
        self.mano[nuevaCarta.calificacionNaipe()].append(nuevaCarta)
        self.mano[nuevaCarta.calificacionNaipe()] = sorted(
            self.mano[nuevaCarta.calificacionNaipe()], key=lambda x: x.valorNaipe())
    '''
    getLowerTrump(self)
    |   Retorna el menor naipe de triunfo.
    '''

    def getLowerTrump(self, trump):
        if len(self.mano[trump.calificacionNaipe()]) > 0:
            return self.mano[trump.calificacionNaipe()][0].valorNaipe()
        else:
            return 15
    '''
    buscarCartas(self, valor, trump="pass", calificacion="pass")
    |   Retorna cartas, con que puede jugar el AI.
    |   Para elegir estas cartas, se aplican las reglas de ataque y defensa.
    |   Al atacar, necesitamos cartas de mismo valor, que en la mesa. Al defenderse,
    |   AI tiene que elegir cartas de mayor valor y misma pinta, o una carta de triunfo.
    '''

    def buscarCartas(self, valor, trump="pass", calificacion="pass"):
        cartasEncontradas = []
        if calificacion == "pass":
            # Está atacando y solo necesita cartas con el mismo valor o que necesita la lista de cartas de triunfo.
            if trump == "pass":
                # Significa que quiere cartas para atacar solamente.

                for calif in self.mano.keys():
                    # Busca las cartas con el mismo valor numerico.
                    for carta in self.mano[calif]:
                        if carta.valorNaipe() == valor:
                            cartasEncontradas.append(carta)

            else:
                # Significa que quiere las cartas trump.
                cartasEncontradas = self.mano[trump.calificacionNaipe()]

        else:
            # Está defendiendo y necesita la calificación para buscar cartas
            # con la misma pinta e igual o mayor valor, además de las cartas trump.

            for carta in self.mano[calificacion]:
                if carta.valorNaipe() >= valor:
                    cartasEncontradas.append(carta)

            if calificacion != trump.calificacionNaipe():
                cartasEncontradas = cartasEncontradas + \
                    self.mano[trump.calificacionNaipe()]

        return cartasEncontradas
    '''
    jugarCarta(self, listaCartasEnJuego, trump, boolAtaque)
    |   Función, responsable de jugar las cartas de AI. El AI, al 
    |   no poseer consciencia propia, se basa en funciones random y simples
    |   condiciones.
    '''

    def jugarCarta(self, listaCartasEnJuego, trump, boolAtaque):
        chance = random.choice(["jugar"] + ["pass"])
        chance = "jugar"
        # Decide de manera random si jugar (atacar/defender) o pasar el turno
        if chance == "pass":
            return chance

        else:
            posiblesCartas = []  # Almacena todas las cartas que se pueden jugar en una lista
            if boolAtaque == True:

                chance = random.choice(["jugar"] + ["pass"] + ["jugar"])
                if chance == "pass":
                    return "pass"
                # Significa que este es el primer ataque
                if len(listaCartasEnJuego["defensa"]) + len(listaCartasEnJuego["ataque"]) == 0:
                    calif = []
                    for calificacion in self.mano.keys():
                        if len(self.mano[calificacion]) != 0:
                            # Agrega todas las calificaciones que poseen cartas para evitar que el random tome una pinta vacia
                            calif.append(calificacion)

                    # La cpu jugara una carta de la pinta calif
                    calif = random.choice(calif)
                    # Elige la carta de menor valor de su mano
                    cartaAJugar = self.mano[calif][0]
                    self.mano[cartaAJugar.calificacionNaipe()].remove(
                        cartaAJugar)
                    return cartaAJugar

                else:  # Significa que hay cartas en juego
                    ranks = []  # Almacena el valor numerico de las cartas en juego
                    cartaAJugar = "pass"

                    for carta in listaCartasEnJuego["defensa"] + listaCartasEnJuego["ataque"]:
                        if carta.valorNaipe() not in ranks:
                            # Agrega el valor del naipe de las cartas en juego a la lista ranks
                            ranks.append(carta.valorNaipe())

                    for rank in ranks:
                        posiblesCartas += self.buscarCartas(rank)

            else:  # Toca defender
                # Ultima carta jugada/Carta del atacante al defensor.
                lastCard = listaCartasEnJuego["ataque"][-1]
                posiblesCartas = self.buscarCartas(
                    lastCard.valorNaipe(), trump, lastCard.calificacionNaipe())

            # Si no se encontro ninguna carta para jugar, pasará el turno.
            if len(posiblesCartas) == 0:
                return "pass"

            # Elige una carta al azar de entre todas las posibles cartas que se pueden jugar.
            cartaAJugar = random.choice(posiblesCartas)
            # cartaAJugar almacena la carta que se va a jugar, tanto para ataque como para defensa.
            self.mano[cartaAJugar.calificacionNaipe()].remove(cartaAJugar)

            return cartaAJugar
