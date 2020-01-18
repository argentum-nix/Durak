import random
from naipe import Naipe
from baraja import Baraja
import sys_tools as st
import operator


class Jugador(object):
    def __init__(self):
        self.esHumano = ""

    def isHuman(self):
        return self.esHumano

    def sacarCarta(self, nuevaCarta):
        pass

    def mostrarCantidad(self):
        pass

    def jugarCarta(self, indice):
        pass

    def mostrarMano(self):
        pass

    def getLowerTrump(self):
        pass


class JugadorHumano(Jugador):
    def __init__(self):
        Jugador.__init__(self)
        self.esHumano = True
        self.mano = []

    def sacarCarta(self, nuevaCarta):
        self.mano.append(nuevaCarta)

    def mostrarMano(self):
        return [carta.printNaipe() for carta in self.mano]

    def mostrarCantidad(self):
        return len(self.mano)

    def posiblesCartas(self, listaCartasEnJuego, trump, boolAtaque):
        posiblesCartas = []  # Almacena todas las cartas que se pueden jugar en una lista
        if boolAtaque == True:  # Toca atacar

            # Significa que este es el primer ataque, todo vale
            if (len(listaCartasEnJuego["defensa"]) == 0) and (len(listaCartasEnJuego["ataque"]) == 0):
                return self.mano

            else:  # Significa que hay cartas en juego, solo se pueden jugar cartas de igual rank
                ranks = []  # Almacena el valor numerico de las cartas en juego

                for carta in listaCartasEnJuego["defensa"] + listaCartasEnJuego["ataque"]:
                    if int(carta.valorNaipe()) not in ranks:
                        # Agrega el valor del naipe de las cartas en juego a la lista ranks
                        ranks.append(int(carta.valorNaipe()))

                for carta in self.mano:
                    if carta.valorNaipe() != '' and int(carta.valorNaipe()) in ranks:
                        posiblesCartas.append(carta)

        else:  # Toca defender, solo se puede jugara cartas de igual o mayor rank e igual calificacion o cualquier trump
            # Ultima carta jugada/Carta del atacante al defensor.
            lastCard = listaCartasEnJuego["ataque"][-1]

            for carta in self.mano:
                if carta.valorNaipe() != '':                    
                    if (int(carta.valorNaipe()) >= int(lastCard.valorNaipe())) and (carta.calificacionNaipe() == lastCard.calificacionNaipe()):
                        posiblesCartas.append(carta) 
                    # Si la ultima carta jugada no es trump:
                    elif not lastCard.isTrump(trump.calificacionNaipe()): 
                        if carta.isTrump(trump.calificacionNaipe()): 
                            posiblesCartas.append(carta)     

        return posiblesCartas

    def jugarCarta(self, carta):
        if carta != "pass":
            del self.mano[self.mano.index(carta)]

    def getLowerTrump(self, trump):
        lower = 15
        for naipe in self.mano:
            if naipe.isTrump(trump) and int(naipe.valorNaipe()) < lower:
                lower = naipe.valorNaipe()
        return lower

    # rellena mano con NULLs si falta para ser divisible por 3
    def rellenarMano(self):
        # funcion propia de la rellanrMano, rellana con cartas vacias
        # en funcion de multiplo de 3 mas cercano (y chico)
        def closestDivisible(n, m):
            quotient = int(n / m)
            n1 = m * quotient
            if (n * m) > 0:
                n2 = m * (quotient + 1)
            else:
                n2 = m * (quotient - 1)
            smallest = {True: n1, False: n2}[n1 <= n2]

            if (n1 > n) & (n1 == smallest):
                return n1
            else:
                return n2

        if(len(self.mano) % 3 != 0):
            length_mano = len(self.mano)
            closest = closestDivisible(len(self.mano), 3)
            for i in range(abs(length_mano - closest)):
                self.mano.append(Naipe("", ""))

    def rellenar(self):
        relleno = []
        if self.mostrarCantidad() == 0:
            return [Naipe("Null", 0), Naipe("Null", 0), Naipe("Null", 0)]
        while((len(relleno) + len(self.mano)) % 3 != 0):
            relleno.append(Naipe("Null", 0))
        return relleno

    def manoAcotada(self, mult):
        return (self.mano + self.rellenar())[0 + (3 * mult): 3 + (3 * mult)]


class JugadorCPU(Jugador):
    def __init__(self):
        Jugador.__init__(self)
        self.esHumano = False
        self.mano = {"Picas": [], "Corazones": [],
                     "Tréboles": [], "Diamantes": []}

    def mostrarCantidad(self):
        return len(self.mano["Picas"]) + len(self.mano["Corazones"]) + len(self.mano["Tréboles"]) + len(self.mano["Diamantes"])

    def sacarCarta(self, nuevaCarta):
        self.mano[nuevaCarta.calificacionNaipe()].append(nuevaCarta)
        self.mano[nuevaCarta.calificacionNaipe()] = sorted(
            self.mano[nuevaCarta.calificacionNaipe()], key = lambda x: x.valorNaipe())

    def getLowerTrump(self, trump):
        if len(self.mano[trump.calificacionNaipe()]) > 0:
            return self.mano[trump.calificacionNaipe()][0].valorNaipe()
        else:
            return 15


    # Retorna una lista con las cartas solicitadas
    def buscarCartas(self, valor, trump = "pass", calificacion="pass"):
        cartasEncontradas = []
        if calificacion == "pass":  # Significa que esta atacando y solo necesita cartas con el mismo numero ingresado en valor o que necesita la lista de cartas trump
            if trump == "pass":  # Significa que quiere cartas para atacar solamente.

                for calif in self.mano.keys():  # Busca las cartas con el mismo valor numerico
                    for carta in self.mano[calif]:
                        if carta.valorNaipe() == valor:
                            cartasEncontradas.append(carta)

            else:  # Significa que quiere las cartas trump
                cartasEncontradas = self.mano[trump.calificacionNaipe()]

        else:  # Significa que está defendiendo y necesita la calificación para buscar cartas con la misma pinta e igual o mayor valor numerico, además de las cartas trump

            for carta in self.mano[calificacion]:
                if carta.valorNaipe() >= valor:
                    cartasEncontradas.append(carta)

            if calificacion != trump.calificacionNaipe():
                cartasEncontradas = cartasEncontradas + \
                    self.mano[trump.calificacionNaipe()]
 

        return cartasEncontradas

    def jugarCarta(self, listaCartasEnJuego, trump, boolAtaque):
        # Si se quiere agregar la opcion de pasar un turno:
        #chance = random.choice(["jugar"] + ["pass"])
        chance = "jugar"
        # Decide de manera random si jugar (atacar/defender) o pasar el turno
        if chance == "pass":
            return chance

        else:
            posiblesCartas = []  # Almacena todas las cartas que se pueden jugar en una lista
            if boolAtaque == True:  # Toca atacar
                
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
                    self.mano[cartaAJugar.calificacionNaipe()].remove(cartaAJugar)
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
                posiblesCartas = self.buscarCartas(lastCard.valorNaipe(), trump, lastCard.calificacionNaipe())

            # Si no se encontro ninguna carta para jugar, pasara el turno.
            if len(posiblesCartas) == 0:
                return "pass"

            # Elige una carta al azar de entre todas las posibles cartas que se pueden jugar
            cartaAJugar = random.choice(posiblesCartas)
            # cartaAJugar almacena la carta que se va a jugar, tanto para ataque como para defensa, ahora sigue eliminarla de la mano y retornarla
            self.mano[cartaAJugar.calificacionNaipe()].remove(cartaAJugar)

            return cartaAJugar

    def mostrarMano(self):
        for listaDeCartas in self.mano.values():
            for carta in listaDeCartas:
                carta.printNaipe()
