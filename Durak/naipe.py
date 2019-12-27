from botonCarta import BotonCarta


class Naipe(self):
    def __init__(self, calificacion, valor):
        self.calificacion = calificacion
        self.valor = valor  # Valor numérico, de 6 a 14.

    def isTrump(self, trumpSuit):
        if self.calificacion == trumpSuit:
            return True
        else:
            return False

    def printNaipe(self):
        if self.valor == 11:
            return "J de {}".format(self.calificacion)
        elif self.valor == 12:
            return "Q de {}".format(self.calificacion)
        elif self.valor == 13:
            return "K de {}".format(self.calificacion)
        elif self.valor == 14:
            return "A de {}".format(self.calificacion)
        else:
            return "{} de {}".format(self.valor, self.calificacion)

    def fileNaipe(self):

        if self.calificacion == "Picas":
            return "P_{}.png".format(self.valor)

        elif self.calificacion == "Corazones":
            return "C_{}.png".format(self.valor)

        elif self.calificacion == "Tréboles":
            return "T_{}.png".format(self.valor)
        else:
            return "D_{}.png".format(self.valor)

    def valorNaipe(self):
        return self.valor

    def calificacionNaipe(self):
        return self.calificacion
