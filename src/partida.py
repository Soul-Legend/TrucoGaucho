import statistics
import time
from asyncio import sleep

from carta import Carta
from dog.dog_actor import DogActor
from envido import Envido
from flor import Flor
from jogador import Jogador
from mesa import Mesa
from truco import Truco


class Partida:
    def __init__(self):
        self._jogador_local = Jogador()
        self._jogador_remoto = Jogador()

        self._mesa = Mesa()

        self._pontos_jogador_local: int = 0
        self._pontos_jogador_remoto: int = 0

        self._pedido_em_andamento: bool = False
        self._qual_pedido: str = ""
        self._infos_popup: dict = dict()
        self._status_partida: str = "sem partida em andamento"

        self._truco: Truco = Truco()
        self._envido: Envido = Envido()
        self._flor: Flor = Flor()
        self._flor_ou_envido_ja_ocorreu: bool = False
        self._truco_ja_ocorreu: bool = False

    def obtem_truco_ja_ocorreu(self):
        return self._truco_ja_ocorreu

    def atribui_truco_ja_ocorreu(self, ja_ocorreu: bool):
        self._truco_ja_ocorreu = ja_ocorreu
        return

    def obtem_flor_ou_envido_ja_ocorreu(self):
        return self._flor_ou_envido_ja_ocorreu

    def atribui_flor_ou_envido_ja_ocorreu(self, ja_ocorreu: bool):
        self._flor_ou_envido_ja_ocorreu = ja_ocorreu

    def obtem_pedido_em_andamento(self):
        return self._pedido_em_andamento

    def obtem_infos_popup(self):
        return self._infos_popup

    def obter_status_partida(self) -> str:
        return self._status_partida

    def receber_inicio(self, jogadores: list[str]):
        self._status_partida = "em progresso"

        self._jogador_local.reset()
        self._jogador_local.inicializar(jogadores[0][1])

        self._jogador_remoto.reset()
        self._jogador_remoto.inicializar(jogadores[1][1])

        if int(jogadores[0][2]) == 1:
            self._jogador_local.troca_turno()
        else:
            self._jogador_remoto.troca_turno()

    def comecar_partida(self, jogadores: list[str]):
        self._status_partida = "em progresso"

        self._jogador_local.reset()
        self._jogador_local.inicializar(jogadores[0][1])

        self._jogador_remoto.reset()
        self._jogador_remoto.inicializar(jogadores[1][1])

        jogada = self.iniciar_nova_mao()

        if int(jogadores[0][2]) == 1:
            self._jogador_local.troca_turno()
        else:
            self._jogador_remoto.troca_turno()

        return jogada

    def obtem_status(self) -> dict:
        status_jogo = dict()

        fim_de_partida = self.verificar_fim_de_partida()
        status_jogo["vencedor"] = fim_de_partida

        placar = (self._pontos_jogador_local, self._pontos_jogador_remoto)
        status_jogo["placar"] = placar

        cartas_jogador_local = self._jogador_local.obtem_cartas()
        status_jogo["cartas_jogador_local"] = cartas_jogador_local

        cartas_jogador_remoto = self._jogador_remoto.obtem_cartas()
        status_jogo["cartas_jogador_remoto"] = cartas_jogador_remoto

        cartas_mesa = self._mesa.obtem_cartas_da_mesa()
        status_jogo["cartas_mesa"] = cartas_mesa

        seu_turno = self._jogador_local.obtemTurno()
        status_jogo["seu_turno"] = seu_turno

        vitorias_mao_local = self._jogador_local.obtem_vitorias_jogador()
        status_jogo["vitorias_mao_local"] = vitorias_mao_local

        vitorias_mao_remoto = self._jogador_remoto.obtem_vitorias_jogador()
        status_jogo["vitorias_mao_remoto"] = vitorias_mao_remoto

        pedido_em_andamento = self.obtem_pedido_em_andamento()
        status_jogo["pedido_em_andamento"] = pedido_em_andamento

        infos_popup = self.obtem_infos_popup()
        status_jogo["infos_popup"] = infos_popup

        return status_jogo

    def receber_jogada(self, jogada: dict):
        qual_jogada = jogada["qual_jogada"]
        if qual_jogada == "jogar_carta":
            self.receber_jogar_carta(jogada)
        elif qual_jogada == "envido" or qual_jogada == "truco" or qual_jogada == "flor":
            self.registra_pedido(qual_jogada)
            self.obtem_popup()
        elif qual_jogada == "aumentar_valor":
            self.receber_aumentar_valor()
            self.obtem_popup()
        elif qual_jogada == "aceitar_pedido":
            self.receber_aceitar_pedido(jogada)
        elif qual_jogada == "correr":
            self.receber_correr(jogada)
        elif qual_jogada == "nova_mao":
            self.receber_nova_mao(jogada)
        if jogada["match_status"] == "next":
            self._jogador_local.troca_turno()
            self._jogador_remoto.troca_turno()

    def receber_aumentar_valor(self):
        pedido = self.obtem_qual_pedido()
        self.registra_pedido_aumentado(pedido=pedido)
        return

    def receber_nova_mao(self, jogada: dict):
        self._mesa.limpar_mesa()

        self._jogador_local.limpar_vitorias_da_mao()
        self._jogador_remoto.limpar_vitorias_da_mao()

        self._jogador_local.receber_cartas(jogada["cartas_jogador_local"])
        self._jogador_remoto.receber_cartas(jogada["cartas_jogador_remoto"])

        self.atribui_flor_ou_envido_ja_ocorreu(False)
        self.atribui_truco_ja_ocorreu(False)

    def envido(self) -> dict:
        flor_ou_envido_ja_ocorreu = self.obtem_flor_ou_envido_ja_ocorreu()
        turno_jogador_local = self._jogador_local.obtemTurno()
        if not turno_jogador_local or flor_ou_envido_ja_ocorreu:
            return {}

        jogada = self._envido.envido()
        self.registra_pedido("envido")
        self._jogador_local.troca_turno()
        self._jogador_remoto.troca_turno()
        return jogada

    def flor(self) -> dict:
        flor_ou_envido_ja_ocorreu = self.obtem_flor_ou_envido_ja_ocorreu()
        turno_jogador_local = self._jogador_local.obtemTurno()
        if not turno_jogador_local or flor_ou_envido_ja_ocorreu:
            return {}

        jogada = self._flor.flor()
        self.registra_pedido("flor")
        self._jogador_local.troca_turno()
        self._jogador_remoto.troca_turno()
        return jogada

    def truco(self) -> dict:
        turno = self._jogador_local.obtemTurno()
        if not turno or self.obtem_truco_ja_ocorreu():
            return {}

        jogada = self._truco.truco()
        self.registra_pedido("truco")
        self._jogador_local.troca_turno()
        self._jogador_remoto.troca_turno()
        return jogada

    def obtem_popup(self):
        pedido = self.obtem_qual_pedido()
        if pedido == "truco" or pedido == "retruco" or pedido == "vale-quatro":
            self._infos_popup = self._truco.obtem_popup(pedido)
        elif pedido == "envido" or pedido == "real-envido" or pedido == "falta-envido":
            self._infos_popup = self._envido.obtem_popup(pedido)
        elif (
            pedido == "flor"
            or pedido == "contra-flor"
            or pedido == "contra-flor-e-o-resto"
        ):
            self._infos_popup = self._flor.obtem_popup(pedido)
        self.registra_pedido(pedido)
        return

    def registra_pedido(self, pedido: str):
        self._pedido_em_andamento = True
        self._qual_pedido = pedido
        if pedido == "truco":
            self.atribui_truco_ja_ocorreu(True)
        elif pedido == "envido" or pedido == "flor":
            self.atribui_flor_ou_envido_ja_ocorreu(True)
        return

    def avaliar_vencedor(self, tipo_avaliacao: str):
        # Relembrando:
        # Rodada = disputada entre 2 cartas jogadas, uma de cada jogador
        # Mão = conjunto de 3 rodadas, resulta no ganho de pontos
        # Partida = conjunto de mãos, acaba quando um dos jogadores tem 30 ou mais pontos

        fim_de_mao = 0

        if tipo_avaliacao == "fim_de_rodada":
            cartas_e_donos = self._mesa.obtem_cartas_da_mesa()[-1]
            resultado = self.comparar_cartas(cartas_e_donos)
            if resultado == 0:
                # Empatou a rodada
                self._jogador_local.atribuir_empate()
                self._jogador_remoto.atribuir_empate()
            elif resultado == 1:
                # Jogador local ganhou a rodada
                self._jogador_local.atribuir_vitoria()
                self._jogador_remoto.atribuir_derrota()
            elif resultado == 2:
                # Jogador remoto ganhou a rodada
                self._jogador_local.atribuir_derrota()
                self._jogador_remoto.atribuir_vitoria()
            vitoria_jogador_local = self._jogador_local.obtem_vitorias_jogador()
            vitoria_jogador_remoto = self._jogador_remoto.obtem_vitorias_jogador()
            fim_de_mao = self.checar_condicao_de_fim_de_mao(
                vitorias_da_mao_jogador_local=vitoria_jogador_local,
                vitorias_da_mao_jogador_remoto=vitoria_jogador_remoto,
            )
            quantidade_pontos = self._mesa.obtem_pontos_mao()
            if fim_de_mao != 0:  # Caso tenha terminado a mão
                if (
                    fim_de_mao != 3
                ):  # Caso não tenha terminado em empate, atribui pontos
                    if fim_de_mao == 1:
                        # Acabou a mão, jogador local ganhou
                        self.atualiza_pontuacao_jogador_local(
                            pontuacao=self._pontos_jogador_local + quantidade_pontos
                        )
                    elif fim_de_mao == 2:
                        # Acabou a mão, jogador remoto ganhou
                        self.atualiza_pontuacao_jogador_remoto(
                            pontuacao=self._pontos_jogador_remoto + quantidade_pontos
                        )
                self._jogador_local.limpar_vitorias_da_mao()
                self._jogador_remoto.limpar_vitorias_da_mao()
            # fim_de_mao == 0: Ainda não acabou a mão
        else:
            # envido, real-envido, falta-envido, flor, contra-flor, contra-flor-e-o-resto
            cartas_da_mesa = self._mesa.obtem_cartas_da_mesa()[-1]
            cartas_jogador_local = self._jogador_local.obtem_cartas().copy()
            cartas_jogador_remoto = self._jogador_remoto.obtem_cartas().copy()
            if cartas_da_mesa != []:
                cartas_jogador_local, cartas_jogador_remoto = self.juntar_cartas(
                    cartas_jogador_local=cartas_jogador_local,
                    cartas_jogador_remoto=cartas_jogador_remoto,
                    cartas_mesa=cartas_da_mesa,
                )
            quem_ganhou_envido_e_flor = self.calcular_vencedor_envido_e_flor(
                cartas_jogador_local=cartas_jogador_local,
                cartas_jogador_remoto=cartas_jogador_remoto,
            )
            if quem_ganhou_envido_e_flor != 0:
                # Caso alguém tenha ganhou o envido ou a flor, atualiza a pontuação,
                # caso contrário, não atribui
                if (
                    tipo_avaliacao == "envido"
                    or tipo_avaliacao == "real-envido"
                    or tipo_avaliacao == "falta-envido"
                ):
                    # Estamos tratando um envido
                    pontos_confronto = self._envido.obtem_pontos_confronto()
                else:
                    # Estamos a tratar uma flor
                    pontos_confronto = self._flor.obtem_pontos_confronto()
                if quem_ganhou_envido_e_flor == 1:
                    # Jogador local ganhou
                    self.atualiza_pontuacao_jogador_local(
                        self._pontos_jogador_local + pontos_confronto
                    )
                else:
                    # Jogador remoto ganhou
                    self.atualiza_pontuacao_jogador_remoto(
                        self._pontos_jogador_remoto + pontos_confronto
                    )

        fim_de_partida = self.verificar_fim_de_partida()
        jogada_iniciar_nova_mao = {}

        if fim_de_partida != 0:
            # Acabou a partida
            if fim_de_partida == 1:
                # Acabou a partida e o jogador local ganhou
                self._jogador_local.atribuir_venceu_jogo()
                self._status_partida = "encerrada"
            elif fim_de_partida == 2:
                # Acabou a partida e o jogador remoto ganhou
                self._jogador_remoto.atribuir_venceu_jogo()
                self._status_partida = "encerrada"
        else:
            # Não acabou a partida
            if tipo_avaliacao == "fim_de_rodada":
                # Não acabou a partida e estamos tratando fim de rodada
                if fim_de_mao != 0:
                    jogada_iniciar_nova_mao = self.iniciar_nova_mao()

        jogada = {
            "qual_jogada": "avaliar_vencedor",
            "vitorias_da_mao_jogador_local": self._jogador_remoto.obtem_vitorias_jogador(),
            "vitorias_da_mao_jogador_remoto": self._jogador_local.obtem_vitorias_jogador(),
            "fim_de_mao": fim_de_mao,
            "fim_de_partida": fim_de_partida,
            "pontuacao_jogador_local": self._pontos_jogador_remoto,
            "pontuacao_jogador_remoto": self._pontos_jogador_local,
            "jogada_iniciar_nova_mao": jogada_iniciar_nova_mao,
        }
        return jogada

    def comparar_cartas(self, cartas_e_donos: list[tuple]) -> int:
        forca_cartas = {
            "Ae": 14,
            "Ap": 13,
            "7e": 12,
            "7o": 11,
            "3p": 10,
            "3o": 10,
            "3c": 10,
            "3e": 10,
            "2p": 9,
            "2o": 9,
            "2c": 9,
            "2e": 9,
            "Ao": 8,
            "Ac": 8,
            "Kp": 7,
            "Ko": 7,
            "Kc": 7,
            "Ke": 7,
            "Qp": 6,
            "Qo": 6,
            "Qc": 6,
            "Qe": 6,
            "jp": 5,
            "jo": 5,
            "jc": 5,
            "je": 5,
            "7p": 4,
            "7c": 4,
            "6p": 3,
            "6o": 3,
            "6c": 3,
            "6e": 3,
            "5p": 2,
            "5o": 2,
            "5c": 2,
            "5e": 2,
            "4p": 1,
            "4o": 1,
            "4c": 1,
            "4e": 1,
        }
        index_carta_jogadores = ["", ""]
        # resultado == 0 -> Empate
        resultado = 0
        for i, carta in enumerate(cartas_e_donos):
            index_carta_jogadores[i] = forca_cartas[carta[0].para_string()]
        if index_carta_jogadores[1] > index_carta_jogadores[0]:
            # resultado == 2 -> Vitoria do remoto
            if cartas_e_donos[1][1] == self._jogador_remoto.obtem_id_jogador():
                resultado = 2
            else:
                resultado = 1
        elif index_carta_jogadores[1] < index_carta_jogadores[0]:
            # resultado == 1 -> Vitoria do local
            if cartas_e_donos[0][1] == self._jogador_remoto.obtem_id_jogador():
                resultado = 2
            else:
                resultado = 1
        else:
            pass
        return resultado

    def checar_condicao_de_fim_de_mao(
        self,
        vitorias_da_mao_jogador_local: list[str],
        vitorias_da_mao_jogador_remoto: list[str],
    ) -> int:
        for i, lista in enumerate(
            [vitorias_da_mao_jogador_local, vitorias_da_mao_jogador_remoto]
        ):
            if (
                lista == ["V", "D", "E"]
                or lista == ["V", "E"]
                or lista == ["E", "V"]
                or lista == ["E", "E", "V"]
                or lista == ["V", "V"]
                or lista == ["D", "V", "V"]
                or lista == ["V", "D", "V"]
            ):
                resultado = i + 1
                return resultado
            elif lista == ["E", "E", "E"]:
                resultado = 3
                return resultado
            else:
                pass
        resultado = 0
        return resultado

    def verificar_fim_de_partida(self) -> int:
        if self._pontos_jogador_local >= 30:
            # Jogador local ganhou a partida.
            return 1
        elif self._pontos_jogador_remoto >= 30:
            # Jogador remoto ganhou a partida.
            return 2
        else:
            # A partida ainda não terminou.
            return 0

    def juntar_cartas(
        self,
        cartas_jogador_local: list[tuple],
        cartas_jogador_remoto: list[tuple],
        cartas_mesa: list[tuple],
    ) -> list[list[tuple]]:
        # Caso o ‘id’ da carta 0 na mesa é igual ao ‘id’ do jogador local
        # coloca a carta 0 no jogador local e a carta 1 no jogador remoto

        if cartas_mesa[0][1] == cartas_jogador_local[0][1]:
            cartas_jogador_local.append(cartas_mesa[0])
            if len(cartas_mesa) > 1:
                cartas_jogador_remoto.append(cartas_mesa[1])
        else:
            cartas_jogador_remoto.append(cartas_mesa[0])
            if len(cartas_mesa) > 1:
                cartas_jogador_local.append(cartas_mesa[1])
        return [cartas_jogador_local, cartas_jogador_remoto]

    def calcular_vencedor_envido_e_flor(
        self, cartas_jogador_local: list[tuple], cartas_jogador_remoto: list[tuple]
    ) -> int:
        pontos_jogador_local = 0
        pontos_jogador_remoto = 0
        pontos_jogador_local = self.calcular_pontos_lista(cartas_jogador_local)
        pontos_jogador_remoto = self.calcular_pontos_lista(cartas_jogador_remoto)

        if pontos_jogador_local == pontos_jogador_remoto:
            return 0
        elif pontos_jogador_local > pontos_jogador_remoto:
            return 1
        else:
            return 2

    def calcular_pontos_lista(self, cartas: list[tuple]) -> int:
        pontos = 0
        qual_pedido: str
        naipes: list
        num_mesmo_naipe: int

        qual_pedido = self.obtem_qual_pedido()
        naipes = list(map(lambda c: c[0].obtem_naipe(), cartas))
        num_mesmo_naipe = naipes.count(statistics.mode(naipes))
        if num_mesmo_naipe == 3 or (
            num_mesmo_naipe == 2
            and qual_pedido in ["envido", "real-envido", "falta-envido"]
        ):
            pontos += 20
        for carta in cartas:
            if carta[0].obtem_numero_carta() < 10:
                pontos += carta[0].obtem_numero_carta()
        return pontos

    def aumentar_valor(self) -> dict:
        pedido = self.obtem_qual_pedido()
        self.registra_pedido_aumentado(pedido=pedido)
        self._jogador_local.troca_turno()
        self._jogador_remoto.troca_turno()
        jogada = {
            "qual_jogada": "aumentar_valor",
            "match_status": "next",
        }
        return jogada

    def obtem_qual_pedido(self) -> str:
        return self._qual_pedido

    def registra_pedido_aumentado(self, pedido: str):
        dif = self.diferenca_para_ganhar()
        if pedido == "truco":
            self._truco.atualizar_pontos_truco(pontos=3)
            self._qual_pedido = "retruco"
        elif pedido == "retruco":
            self._truco.atualizar_pontos_truco(pontos=4)
            self._qual_pedido = "vale-quatro"
        elif pedido == "envido":
            self._envido.atualizar_pontos_envido(pontos=3)
            self._qual_pedido = "real-envido"
        elif pedido == "real-envido":
            self._envido.atualizar_pontos_envido(pontos=dif)
            self._qual_pedido = "falta-envido"
        elif pedido == "flor":
            self._flor.atualizar_pontos_flor(pontos=5)
            self._qual_pedido = "contra-flor"
        elif pedido == "contra-flor":
            self._flor.atualizar_pontos_flor(pontos=dif)
            self._qual_pedido = "contra-flor-e-o-resto"

    def diferenca_para_ganhar(self):
        maior_pontuacao = max(self._pontos_jogador_local, self._pontos_jogador_remoto)
        return 30 - maior_pontuacao

    def abandonar_partida(self):
        self._status_partida = "abandonada"

    def iniciar_nova_mao(self):
        cartas = self._mesa.iniciar_nova_mao()

        self._jogador_local.limpar_vitorias_da_mao()
        self._jogador_remoto.limpar_vitorias_da_mao()

        cartas_jogador_local = cartas[0]
        cartas_jogador_remoto = cartas[1]

        self._jogador_local.receber_cartas(cartas_jogador_local)
        self._jogador_remoto.receber_cartas(cartas_jogador_remoto)

        self.atribui_flor_ou_envido_ja_ocorreu(False)
        self.atribui_truco_ja_ocorreu(False)

        jogada = {
            "qual_jogada": "nova_mao",
            "cartas_jogador_local": cartas_jogador_remoto,
            "cartas_jogador_remoto": cartas_jogador_local,
            "match_status": "progress",
        }

        return jogada

    def jogar_carta(self, carta: tuple):
        _, jogador_id = carta
        turno = self._jogador_local.obtemTurno()

        if not turno:
            return {}

        self._jogador_local.retirar_carta(carta)
        self._mesa.jogar_carta(carta)
        fim_de_rodada = self.verificar_fim_de_rodada()
        jogada_avaliar_vencedor = {}
        if fim_de_rodada:
            jogada_avaliar_vencedor = self.avaliar_vencedor(
                tipo_avaliacao="fim_de_rodada"
            )
        self._jogador_local.troca_turno()
        self._jogador_remoto.troca_turno()

        jogada = {
            "qual_jogada": "jogar_carta",
            "carta_jogada": carta,
            "jogada_avaliar_vencedor": jogada_avaliar_vencedor,
            "match_status": "finished" if jogada_avaliar_vencedor != {} and jogada_avaliar_vencedor["fim_de_partida"] != 0 else "next",
        }
        return jogada

    def receber_jogar_carta(self, jogada: dict):
        carta_jogada, id_jogador = jogada["carta_jogada"]
        carta = (Carta.de_dict(carta_jogada), id_jogador)
        cartas_jogador_remoto = self._jogador_remoto.obtem_cartas()
        if carta in cartas_jogador_remoto:
            self._jogador_remoto.retirar_carta(carta)
            self._mesa.jogar_carta(carta)
        if jogada["jogada_avaliar_vencedor"] != {}:
            self.receber_avaliacao(jogada["jogada_avaliar_vencedor"])

    def verificar_fim_de_rodada(self) -> bool:
        num = self._mesa.obter_numero_cartas()
        return num % 2 == 0

    def receber_avaliacao(self, jogada: dict):
        self._jogador_local.atualiza_vitorias_da_mao(
            jogada["vitorias_da_mao_jogador_local"]
        )
        self._jogador_remoto.atualiza_vitorias_da_mao(
            jogada["vitorias_da_mao_jogador_remoto"]
        )
        self.atualiza_pontuacao_jogador_local(jogada["pontuacao_jogador_local"])
        self.atualiza_pontuacao_jogador_remoto(jogada["pontuacao_jogador_remoto"])
        if jogada["fim_de_partida"] != 0:
            if jogada["fim_de_partida"] == 1:
                self._jogador_local.atribuir_venceu_jogo()
            elif jogada["fim_de_partida"] == 2:
                self._jogador_remoto.atribuir_venceu_jogo()
            self._status_partida = "encerrada"
        if jogada["fim_de_mao"] != 0:
            self._jogador_local.limpar_vitorias_da_mao()
            self._jogador_remoto.limpar_vitorias_da_mao()
        if jogada["jogada_iniciar_nova_mao"] != {}:
            self.receber_nova_mao(jogada["jogada_iniciar_nova_mao"])

    def atualiza_pontuacao_jogador_local(self, pontuacao: int):
        self._pontos_jogador_local = pontuacao

    def atualiza_pontuacao_jogador_remoto(self, pontuacao: int):
        self._pontos_jogador_remoto = pontuacao

    def receber_correr(self, jogada: dict):
        self.atualiza_pontuacao_jogador_local(
            self._pontos_jogador_local + jogada["pontos_corrida"]
        )
        if jogada["correndo_de"] != "":
            self.finalizar_pedido()
        if jogada["fim_de_partida"] != 0:
            if jogada["fim_de_partida"] == 1:
                self._jogador_local.atribuir_venceu_jogo()
            elif jogada["fim_de_partida"] == 2:
                self._jogador_remoto.atribuir_venceu_jogo()
            self._status_partida = "encerrada"
        if jogada["jogada_iniciar_nova_mao"] != {}:
            self.receber_nova_mao(jogada["jogada_iniciar_nova_mao"])

    def receber_aceitar_pedido(self, jogada: dict):
        pedido = self.obtem_qual_pedido()

        if pedido in ["truco", "retruco", "vale-quatro"]:
            self._mesa.atualizar_pontos_mao(jogada["pontuacao_mesa"])

        self.finalizar_pedido()

        if jogada["jogada_avaliar_vencedor"] != {}:
            self.receber_avaliacao(jogada=jogada["jogada_avaliar_vencedor"])

    def aceitar_pedido(self) -> dict:
        valor_mao = 0
        pedido = self.obtem_qual_pedido()

        jogada_avaliar_vencedor = {}
        if pedido in ["truco", "retruco", "vale-quatro"]:
            valor_mao = self._truco.obter_pontos_truco()
            self._mesa.atualizar_pontos_mao(pontos=valor_mao)
        else:
            jogada_avaliar_vencedor = self.avaliar_vencedor(tipo_avaliacao=pedido)
        self.finalizar_pedido()
        cartas_jogador_local = self._jogador_local.obtem_cartas()
        cartas_jogador_remoto = self._jogador_remoto.obtem_cartas()
        match_status = "progress"
        if len(cartas_jogador_local) <= len(cartas_jogador_remoto):
            self._jogador_local.troca_turno()
            self._jogador_remoto.troca_turno()
            match_status = "next"
        jogada = {
            "qual_jogada": "aceitar_pedido",
            "pontuacao_mesa": valor_mao,
            "jogada_avaliar_vencedor": jogada_avaliar_vencedor,
            "match_status": "finished" if jogada_avaliar_vencedor != {} and jogada_avaliar_vencedor["fim_de_partida"] != 0 else match_status,
        }
        return jogada

    def finalizar_pedido(self):
        self._pedido_em_andamento = False
        self._qual_pedido = ""
        self._infos_popup = dict()

    def correr(self) -> dict:
        turno_jogador_local = self._jogador_local.obtemTurno()
        if not turno_jogador_local:
            return {}

        pedido = self.obtem_qual_pedido()

        pontuacao = self.obter_pontos_corrida(pedido)
        self.atualiza_pontuacao_jogador_remoto(self._pontos_jogador_remoto + pontuacao)

        jogada_iniciar_nova_mao = {}

        if pedido in [
            "truco",
            "retruco",
            "vale-quatro",
            "envido",
            "real-envido",
            "falta-envido",
            "flor",
            "contra-flor",
            "contra-flor-e-o-resto",
        ]:
            self.finalizar_pedido()
        
        fim_de_partida = self.verificar_fim_de_partida()

        if fim_de_partida != 0:
            # Acabou a partida
            if fim_de_partida == 1:
                # Acabou a partida e o jogador local ganhou
                self._jogador_local.atribuir_venceu_jogo()
                self._status_partida = "encerrada"
            elif fim_de_partida == 2:
                # Acabou a partida e o jogador remoto ganhou
                self._jogador_remoto.atribuir_venceu_jogo()
                self._status_partida = "encerrada"
        elif pedido == "" or pedido == "truco":
            jogada_iniciar_nova_mao = self.iniciar_nova_mao()

        self._jogador_local.troca_turno()
        self._jogador_remoto.troca_turno()

        jogada = {
            "qual_jogada": "correr",
            "correndo_de": pedido,
            "pontos_corrida": pontuacao,
            "fim_de_partida": fim_de_partida,
            "jogada_iniciar_nova_mao": jogada_iniciar_nova_mao,
            "match_status": "next" if fim_de_partida == 0 else "finished",
        }
        return jogada

    def obter_pontos_corrida(self, pedido: str) -> int:
        tabela_pontos_correr = {
            "": self._mesa.obtem_pontos_mao(),
            "truco": 1,
            "retruco": 2,
            "vale-quatro": 3,
            "envido": 1,
            "real-envido": 2,
            "falta-envido": 5,
            "flor": 3,
            "contra-flor": 4,
            "contra-flor-e-o-resto": 6,
        }
        return tabela_pontos_correr[pedido]

    def restaurar_estado_inicial(self):
        self._mesa.limpar_mesa()
        self.reiniciar_pontuacao()
        self.finalizar_pedido()
        self.atribui_flor_ou_envido_ja_ocorreu(False)
        self.atribui_truco_ja_ocorreu(False)

        self._jogador_local = Jogador()
        self._jogador_remoto = Jogador()

        self._status_partida = "sem partida em andamento"

    def reiniciar_pontuacao(self):
        self._pontos_jogador_local = 0
        self._pontos_jogador_remoto = 0
