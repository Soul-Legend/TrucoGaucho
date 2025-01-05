class Mao:
    def __init__(self):
        self._pontos_mao: int = 1

    def obtem_pontos_mao(self) -> int:
        return self._pontos_mao

    def atualizar_pontos_mao(self, pontos: int):
        self._pontos_mao = pontos

    def reiniciar_mao(self):
        self._pontos_mao = 1
