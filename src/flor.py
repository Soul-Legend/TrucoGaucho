class Flor:
    def __init__(self):
        self._pontos: int = 4

    def flor(self) -> dict:
        self.atualizar_pontos_flor(pontos=4)
        jogada = {
            "qual_jogada": "flor",
            "match_status": "next",
        }
        return jogada

    def obtem_pontos_confronto(self) -> int:
        return self._pontos

    def atualizar_pontos_flor(self, pontos: int):
        self._pontos = pontos

    def obtem_popup(self, grau_de_aumento: str) -> dict:
        if grau_de_aumento == "flor":
            infos_popup = {
                "texto_central": "O oponente pediu flor!",
                "botoes": ["aceitar_pedido", "aumentar_valor", "correr"]
            }
        elif grau_de_aumento == "contra-flor":
            infos_popup = {
                "texto_central": "O oponente pediu contra-flor!",
                "botoes": ["aceitar_pedido", "aumentar_valor", "correr"]
            }
        elif grau_de_aumento == "contra-flor-e-o-resto":
            infos_popup = {
                "texto_central": "O oponente pediu contra-flor-e-o-resto!",
                "botoes": ["aceitar_pedido", "correr"]
            }
        return infos_popup