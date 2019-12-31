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

    def posiblesCartas(self):
        pass


class JugadorHumano(Jugador):
    def __init__(self):
        Jugador.__init__(self)
        self.esHumano = True
        self.mano = []

    def sacarCarta(self, nuevaCarta):
        self.mano.append(nuevaCarta)

    def mostrarMano(self):
        [carta.printNaipe() for carta in self.mano]

    def mostrarCantidad(self):
        return len(self.mano)

    def posiblesCartas(self, listaCartasEnJuego, trump, boolAtaque):
        posiblesCartas = []  # Almacena todas las cartas que se pueden jugar en una lista
        if boolAtaque == True:  # Toca atacar

            if len(listaCartasEnJuego) == 0:  # Significa que este es el primer ataque, todo vale
                return self.mano 

            else:  # Significa que hay cartas en juego, solo se pueden jugar cartas de igual rank
                ranks = []  # Almacena el valor numerico de las cartas en juego

                for carta in listaCartasEnJuego:
                    if carta.valorNaipe() not in ranks:
                        # Agrega el valor del naipe de las cartas en juego a la lista ranks
                        ranks.append(carta.valorNaipe())

                for carta in self.mano:
                    if carta.valorNaipe() in ranks:
                        posiblesCartas.append(carta)

        else:  # Toca defender, solo se puede jugar cartas de igual o mayor rank e igual calificacion o cualquier trump
            # Ultima carta jugada/Carta del atacante al defensor.
            lastCard = listaCartasEnJuego[-1]
            for carta in self.mano:
                if (carta.valorNaipe() >= lastCard.valorNaipe() and carta.calificacionNaipe == lastCard.calificacionNaipe) or carta.isTrump(trump):
                    posiblesCartas.append(carta)

        return posiblesCartas

    def jugarCarta(self, indice):
        carta = self.mano[indice]
        del self.mano[indice]

        return carta

    def getLowerTrump(self, trump):
        lower = 15
        for naipe in mano:
            if naipe.valorNaipe() < lower and naipe.isTrump(trump):
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

        print("El mas ceracno divisible a largo es",
              closestDivisible(len(self.mano), 3))

        if(len(self.mano) % 3 != 0):
            length_mano = len(self.mano)
            print("Largo inicial de la lista es ", length_mano)
            closest = closestDivisible(len(self.mano), 3)
            print("De hecho debo estar agregando cosas porque la dif es:",
                  abs(length_mano - closest))
            for i in range(abs(length_mano - closest)):
                self.mano.append(Naipe("", ""))
            print("Largo final de la mano es ", len(self.mano))

    def manoAcotada(self, mult):
        self.rellenarMano()
        return self.mano[0 + (3 * mult): 3 + (3 * mult)]


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
        self.mano[nuevaCarta.calificacionNaipe()] = sorted(self.mano[nuevaCarta.calificacionNaipe()], lambda x: x.valorNaipe())

    def getLowerTrump(self, trump):
        return self.mano[trump][0].valorNaipe()
    
    # Retorna una lista con las cartas solicitadas
    def buscarCartas(self, valor, trump="pass", calificacion="pass"):
        cartasEncontradas = []
        if calificacion == "pass":  # Significa que esta atacando y solo necesita cartas con el mismo numero ingresado en valor o que necesita la lista de cartas trump
            if trump == "pass":  # Significa que quiere cartas para atacar solamente.

                for calif in mano.keys():  # Busca las cartas con el mismo valor numerico
                    for carta in mano[calif]:
                        if carta.valorNaipe() == valor:
                            cartasEncontradas.append(carta)

            else:  # Significa que quiere las cartas trump
                cartasEncontradas = mano[trump]

        else:  # Significa que está defendiendo y necesita la calificación para buscar cartas con la misma pinta e igual o mayor valor numerico, además de las cartas trump

            for carta in mano[calificacion]:
                if carta.valorNaipe() >= valor:
                    cartasEncontradas.append(carta)

            if calificacion != trump:
                cartasEncontradas = cartasEncontradas + mano[trump]

        return cartasEncontradas

    def jugarCarta(self, listaCartasEnJuego, trump, boolAtaque):
        #Si se quiere agregar la opcion de pasar un turno: 
        #chance = random.choice(["jugar"] + ["pass"])
        chance = "jugar"
        # Decide de manera random si jugar (atacar/defender) o pasar el turno
        if chance == "pass":
            return chance

        else:
            posiblesCartas = []  # Almacena todas las cartas que se pueden jugar en una lista
            if boolAtaque == True:  # Toca atacar

                if len(listaCartasEnJuego) == 0:  # Significa que este es el primer ataque
                    calif = []

                    for calificacion in mano.keys():
                        if len(mano[calificacion]) != 0:
                            # Agrega todas las calificaciones que poseen cartas para evitar que el random tome una pinta vacia
                            calif.append(calificacion)

                    # La cpu jugara una carta de la pinta calif
                    calif = random.choice(calif)
                    cartaAJugar = random.choice(mano[calif])

                else:  # Significa que hay cartas en juego
                    ranks = []  # Almacena el valor numerico de las cartas en juego
                    cartaAJugar = "pass"

                    for carta in listaCartasEnJuego:
                        if carta.valorNaipe() not in ranks:
                            # Agrega el valor del naipe de las cartas en juego a la lista ranks
                            ranks.append(carta.valorNaipe())

                    for rank in ranks:
                        posiblesCartas += buscarCartas(rank)

            else:  # Toca defender
                # Ultima carta jugada/Carta del atacante al defensor.
                lastCard = listaCartasEnJuego[-1]
                posiblesCartas = buscarCartas(lastCard.valorNaipe(), trump, lastCard.calificacionNaipe())

            # Si no se encontro ninguna carta para jugar, pasara el turno.
            if len(posiblesCartas) == 0:
                return "pass"

            # Elige una carta al azar de entre todas las posibles cartas que se pueden jugar
            cartaAJugar = random.choice(posiblesCartas)
            # cartaAJugar almacena la carta que se va a jugar, tanto para ataque como para defensa, ahora sigue eliminarla de la mano y retornarla
            mano[cartaAJugar.calificacionNaipe()].remove(cartaAJugar)

            return cartaAJugar

    def mostrarMano(self):
        for listaDeCartas in self.mano.values():
            for carta in listaDeCartas:
                carta.printNaipe()
