import random
from naipe import Naipe
from baraja import Baraja



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

    def jugarCarta(self, indice):
        carta = self.mano[indice]
        del self.mano[indice]
        return carta

    def manoAcotada(self, mult = 0):
        return self.mano[0+(3*mult):3+(3*mult)]

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

    def buscarCartas(self, valor, trump = "pass", calificacion = "pass"): # Retorna una lista con las cartas solicitadas
        cartasEncontradas = []
        if calificacion == "pass": # Significa que esta atacando y solo necesita cartas con el mismo numero ingresado en valor o que necesita la lista de cartas trump
            if trump == "pass": # Significa que quiere cartas para atacar solamente.

                for calif in mano.keys(): # Busca las cartas con el mismo valor numerico
                    for carta in mano[calif]:
                        if carta.valorNaipe() == valor:
                            cartasEncontradas.append(carta)

            else: # Significa que quiere las cartas trump
                cartasEncontradas = mano[trump]
        
        else: #Significa que está defendiendo y necesita la calificación para buscar cartas con la misma pinta e igual o mayor valor numerico, además de las cartas trump
            
            for carta in mano[calificacion]:
                if carta.valorNaipe() >= valor:
                    cartasEncontradas.append(carta)
            
            if calificacion != trump:
                cartasEncontradas = cartasEncontradas + mano[trump]
            
        if len(cartasEncontradas) == 0:
            return "pass"
        else:
            return cartasEncontradas
        pass

    def jugarCarta(self, listaCartasEnJuego, trump, boolAtaque):
        chance = random.choice(["jugar"] + ["pass"])

        if chance == "pass": # Decide de manera random si jugar (atacar/defender) o pasar el turno
            return chance
            
        else:
            posiblesCartas = [] # Almacena todas las cartas que se pueden jugar en una lista
            if boolAtaque == True: # Toca atacar

                if len(listaCartasEnJuego) == 0: # Significa que este es el primer ataque            
                    calif = []

                    for calificacion in mano.keys():
                        if len(mano[calificacion]) != 0:
                            calif.append(calificacion) # Agrega todas las calificaciones que poseen cartas para evitar que el random tome una calificacion vacia

                    calif = random.choice(calif) # La cpu jugara una carta de la pinta calif 
                    cartaAJugar = random.choice(mano[calif])

                else: # Significa que hay cartas en juego
                    ranks = [] # Almacena el valor numerico de las cartas en juego
                    cartaAJugar = "pass"

                    for carta in listaCartasEnJuego:
                        if carta.valorNaipe() not in ranks:
                            ranks.append(carta.valorNaipe()) # Agrega el valor del naipe de las cartas en juego a la lista ranks
                    
                    for rank in ranks:
                        posiblesCartas += buscarCartas(rank)                                   

            else: # Toca defender
                lastCard = listaCartasEnJuego[-1] # Ultima carta jugada/Carta del atacante al defensor.
                posiblesCartas = buscarCartas(lastCard.valorNaipe(), trump, lastCard.calificacionNaipe())
            
            if len(posiblesCartas) == 0: # Si no se encontro ninguna carta para jugar, pasara el turno.
                return "pass"
            
            cartaAJugar = random.choice(posiblesCartas) # Elige una carta al azar de entre todas las posibles cartas que se pueden jugar 
            # cartaAJugar almacena la carta que se va a jugar, tanto para ataque como para defensa, ahora sigue eliminarla de la mano y retornarla
            mano[cartaAJugar.calificacionNaipe()].remove(cartaAJugar)

            return cartaAJugar

    def mostrarMano(self):
        for listaDeCartas in self.mano.values():
            for carta in listaDeCartas:
                carta.printNaipe()