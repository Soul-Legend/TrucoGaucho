import random

from carta import Carta, Naipe


class Baralho:
    def __init__(self):
        self._cartas: list[Carta] = None
        """# @AssociationMultiplicity 34..40
        # @AssociationKind Aggregation"""

        self.reiniciar_baralho()

    def embaralhar(self):
        random.shuffle(self._cartas)

    def reiniciar_baralho(self):
        self._cartas = [
            Carta(numero, naipe)
            for numero in range(1, 13)
            if numero not in [8, 9]
            for naipe in [Naipe.ESPADAS, Naipe.COPAS, Naipe.OUROS, Naipe.PAUS]
        ]

    def distribuir_cartas(self) -> list:
        cartas_jogadores = []

        for i in range(2):
            cartas_temp = []
            for j in range(3):
                carta = self._cartas.pop()
                cartas_temp.append(carta)
            cartas_jogadores.append(cartas_temp)

        return cartas_jogadores
