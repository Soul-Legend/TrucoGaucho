from baralho import Baralho
from mao import Mao


class Mesa:
    def __init__(self):
        self._mao = Mao()
        self._baralho = Baralho()
        """# @AssociationMultiplicity 1
        # @AssociationKind Composition"""
        self._cartas_jogadas: list[list[tuple]] = [[]]
        """# @AssociationMultiplicity 0..6
        # @AssociationKind Aggregation"""

    def obtem_cartas_da_mesa(self) -> list[list[tuple]]:
        return self._cartas_jogadas

    def obtem_pontos_mao(self) -> int:
        return self._mao.obtem_pontos_mao()

    def atualizar_pontos_mao(self, pontos: int):
        self._mao.atualizar_pontos_mao(pontos)

    def iniciar_nova_mao(self) -> list:
        self.limpar_mesa()

        self._baralho.embaralhar()

        cartas_jogadores = self._baralho.distribuir_cartas()
        return cartas_jogadores

    def limpar_mesa(self):
        self._cartas_jogadas = [[]]
        self._baralho.reiniciar_baralho()
        self._mao.reiniciar_mao()

    def jogar_carta(self, carta: tuple):
        if len(self._cartas_jogadas[-1]) == 2:
            self._cartas_jogadas.append([])

        self._cartas_jogadas[-1].append(carta)

    def obter_numero_cartas(self) -> int:
        return sum(len(sublista) for sublista in self._cartas_jogadas)
