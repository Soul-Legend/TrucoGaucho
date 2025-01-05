from carta import Carta


class Jogador:
    def __init__(self):
        self._cartas: list[tuple] = []
        """# @AssociationMultiplicity 0..3
        # @AssociationKind Aggregation"""
        self._venceu_jogo: bool = False
        self._sua_vez: bool = False
        self._vitorias_da_mao: list = []
        self._id_jogador: str = None

    def inicializar(self, id_jog: str = ""):
        self.reset()
        self._id_jogador = id_jog

    def reset(self):
        self._cartas = []
        self._venceu_jogo = False
        self._sua_vez = False
        self._vitorias_da_mao = []

    def troca_turno(self):
        self._sua_vez = not self._sua_vez

    def obtem_id_jogador(self) -> str:
        return self._id_jogador

    def obtemTurno(self) -> bool:
        return self._sua_vez

    def atribuir_empate(self):
        self._vitorias_da_mao.append("E")

    def atribuir_vitoria(self):
        self._vitorias_da_mao.append("V")

    def atribuir_derrota(self):
        self._vitorias_da_mao.append("D")

    def obtem_vitorias_jogador(self) -> list:
        return self._vitorias_da_mao

    def limpar_vitorias_da_mao(self):
        self._vitorias_da_mao = []

    def atribuir_venceu_jogo(self):
        self._venceu_jogo = True

    def obtem_cartas(self) -> list[tuple]:
        return self._cartas

    def receber_cartas(self, cartas: list):
        self._cartas = list(
            map(lambda carta: (Carta.de_dict(carta), self._id_jogador), cartas)
        )

    def retirar_carta(self, carta: tuple):
        self._cartas.remove(carta)

    def atualiza_vitorias_da_mao(self, vitorias_da_mao: list):
        self._vitorias_da_mao = vitorias_da_mao
