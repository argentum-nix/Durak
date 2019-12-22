
class Naipe(object):
    def __init__(self, calificacion, valor):
        self.calificacion = calificacion
        self.valor = valor
        self.trump = False

    def isTrump(self, trump):
        if self.calificacion == trump:
            self.trump = True
        return self.trump

    def printNaipe(self):
        print("{} de {}".format(self.valor, self.calificacion))

    def valorNaipe(self):
        try:
            int(self.rank)
            return int(self.rank)
        except ValueError:
            if self.rank == "J":
                return 11
            elif self.rank == "Q":
                return 12
            elif self.rank == "K":
                return 13
            elif self.rank == "A":
                return 14
            else:
                raise Exception("Calificacion de naipe inválida!")