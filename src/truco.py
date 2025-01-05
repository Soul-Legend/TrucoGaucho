class Truco:
    def __init__(self):
        self._pontos: int = 2

    def truco(self) -> dict:
        self.atualizar_pontos_truco(pontos=2)
        jogada = {
            "qual_jogada": "truco",
            "match_status": "next",
        }
        return jogada

    def obter_pontos_truco(self):
        return self._pontos

    def atualizar_pontos_truco(self, pontos: int):
        self._pontos = pontos

    def obtem_popup(self, grau_de_aumento: str) -> dict:
        if grau_de_aumento == "truco":
            infos_popup = {
                "texto_central": "O oponente pediu truco!",
                "botoes": ["aceitar_pedido", "aumentar_valor", "correr"]
            }
        elif grau_de_aumento == "retruco":
            infos_popup = {
                "texto_central": "O oponente pediu retruco!",
                "botoes": ["aceitar_pedido", "aumentar_valor", "correr"]
            }
        elif grau_de_aumento == "vale-quatro":
            infos_popup = {
                "texto_central": "O oponente pediu vale-quatro!",
                "botoes": ["aceitar_pedido", "correr"]
            }
        return infos_popup
