class Envido:
    def __init__(self):
        self._pontos: int = 2

    def envido(self) -> dict:
        self.atualizar_pontos_envido(pontos=2)
        jogada = {
            "qual_jogada": "envido",
            "match_status": "next",
        }
        return jogada

    def obtem_pontos_confronto(self) -> int:
        return self._pontos

    def atualizar_pontos_envido(self, pontos: int):
        self._pontos = pontos

    def obtem_popup(self, grau_de_aumento: str) -> dict:
        if grau_de_aumento == "envido":
            infos_popup = {
                "texto_central": "O oponente pediu envido!",
                "botoes": ["aceitar_pedido", "aumentar_valor", "correr"]
            }
        elif grau_de_aumento == "real-envido":
            infos_popup = {
                "texto_central": "O oponente pediu real-envido!",
                "botoes": ["aceitar_pedido", "aumentar_valor", "correr"]
            }
        elif grau_de_aumento == "falta-envido":
            infos_popup = {
                "texto_central": "O oponente pediu falta-envido!",
                "botoes": ["aceitar_pedido", "correr"]
            }
        return infos_popup
