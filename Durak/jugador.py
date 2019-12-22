class Jugador(object):
    def __init__(self):
        self.cartas = {"Picas": [], "Corazones": [],
                       "Tréboles": [], "Diamantes": []}
        self.esHumano = ""
        self.cantidad = 0

    def sacarCarta(self, baraja):
        temp = baraja.sacarDeBaraja()
        self.cartas[temp.calificacion].append(temp)
        self.cantidad += 1


class jugadorAI(Jugador):
    def __init__(self):
        Jugador.__init__(self)
        self.esHumano = False


class jugadorHumano(Jugador):
    def __init__(self):
        Jugador.__init__(self)
        self.esHumano = True
