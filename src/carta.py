from enum import Enum


class Naipe(int, Enum):
    ESPADAS = 1
    COPAS = 2
    OUROS = 3
    PAUS = 4


# Tivemos que fazer uma herança com dict do Python para fazer a classe Carta
# serializável por JSON e com isso ser possível mandá-la pelo send_move().
class Carta(dict):
    def __init__(self, numero, naipe):
        self._numero = numero
        self._naipe = naipe

        dict.__init__(self, _numero=numero, _naipe=naipe)

    def obtem_numero_carta(self):
        return self._numero

    def obtem_naipe(self):
        return self._naipe

    @staticmethod
    def de_dict(carta_dict):
        if type(carta_dict) == Carta:
            carta_dict = dict(carta_dict)

        numero = carta_dict["_numero"]
        naipe = carta_dict["_naipe"]

        if type(naipe) != Naipe:
            naipe = Naipe(naipe)

        return Carta(numero, naipe)

    def para_string(self):
        naipes_str = {
            Naipe.ESPADAS: "e",
            Naipe.COPAS: "c",
            Naipe.OUROS: "o",
            Naipe.PAUS: "p",
        }
        numeros_str = ["", "A", "2", "3", "4", "5", "6", "7", "", "", "j", "Q", "K"]

        return numeros_str[self.obtem_numero_carta()] + naipes_str[self.obtem_naipe()]
