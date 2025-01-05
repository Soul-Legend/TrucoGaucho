import tkinter as tk
import tkinter.messagebox
import tkinter.simpledialog
from tkinter import ttk

from PIL import Image, ImageTk

from dog.dog_actor import DogActor
from dog.dog_interface import DogPlayerInterface
from dog.start_status import StartStatus
from partida import Partida


class PlayerInterface(DogPlayerInterface):
    def __init__(self):
        self.receive_start = self.receber_inicio
        self.receive_move = self.receber_jogada

        self._janela = tk.Tk()
        self._janela.title("Truco Gaúcho")
        self._janela.geometry("800x600")

        self._janela.rowconfigure(tuple(range(3)), weight=1)
        self._janela.columnconfigure(tuple(range(6)), weight=1)

        self.encher_janela_principal()

        self._dog_server_interface = DogActor()

        nome_jogador = tkinter.simpledialog.askstring(
            title="Identificação do jogador", prompt="Qual é o seu nome?"
        )
        message = self._dog_server_interface.initialize(nome_jogador, self)
        tkinter.messagebox.showinfo(message=message)

        self._partida = Partida()

        self._popup: tk.Toplevel = None

        self._janela.mainloop()

    def encher_janela_principal(self):
        for widget in self._janela.winfo_children():
            widget.destroy()

        self._menu = tk.Menu(self._janela)
        jogo_barra = tk.Menu(self._menu, tearoff=0)
        jogo_barra.add_command(
            label="Iniciar partida",
            command=self.comecar_partida,
        )
        jogo_barra.add_command(
            label="Restaurar estado inicial",
            command=self.restaurar_estado_inicial,
        )
        self._menu.add_cascade(label="Jogo", menu=jogo_barra)

        self._janela.config(menu=self._menu)

        acoes = ttk.Frame(self._janela, borderwidth=10, relief=tk.RIDGE)
        self._flor_bt = ttk.Button(
            acoes,
            text="Flor",
            command=lambda: (
                self.flor() if not self._partida.obtem_pedido_em_andamento() else None
            ),
        )
        self._envido_bt = ttk.Button(
            acoes,
            text="Envido",
            command=lambda: (
                self.envido() if not self._partida.obtem_pedido_em_andamento() else None
            ),
        )
        self._truco_bt = ttk.Button(
            acoes,
            text="Truco",
            command=lambda: (
                self.truco() if not self._partida.obtem_pedido_em_andamento() else None
            ),
        )
        self._correr_bt = ttk.Button(
            acoes,
            text="Correr",
            command=lambda: (
                self.correr() if not self._partida.obtem_pedido_em_andamento() else None
            ),
        )
        self._flor_bt.pack()
        self._envido_bt.pack()
        self._truco_bt.pack()
        self._correr_bt.pack()

        self._ind_turno = tk.StringVar()
        self._vitorias_mao_remoto = tk.StringVar()
        self._vitorias_mao_local = tk.StringVar()
        self._placar_jogador_remoto = tk.StringVar()
        self._placar_jogador_local = tk.StringVar()

        self._placar = ttk.Frame(self._janela, borderwidth=10, relief=tk.RIDGE)
        placar_txt = ttk.Label(self._placar, text="PLACAR", font="Helvetica 20")
        placar_txt.pack()

        remoto_placar = ttk.Label(
            self._placar,
            textvariable=self._placar_jogador_remoto,
            background="red",
            foreground="white",
        )
        remoto_placar.pack()

        local_placar = ttk.Label(
            self._placar,
            textvariable=self._placar_jogador_local,
            background="blue",
            foreground="white",
        )
        local_placar.pack()

        self._vitorias_mao = ttk.Frame(self._janela, borderwidth=10, relief=tk.RIDGE)

        self._cartas_jogador_remoto = ttk.Frame(
            self._janela, borderwidth=10, relief=tk.GROOVE
        )
        self._cartas_jogador_remoto.rowconfigure(0, weight=1)
        self._cartas_jogador_remoto.columnconfigure(tuple(range(6)), weight=1)

        self._cartas_jogador_local = ttk.Frame(
            self._janela, borderwidth=10, relief=tk.GROOVE
        )
        self._cartas_jogador_local.rowconfigure(0, weight=1)
        self._cartas_jogador_local.columnconfigure(tuple(range(6)), weight=1)

        self._cartas_mesa = ttk.Frame(self._janela, borderwidth=10, relief=tk.GROOVE)
        self._cartas_mesa.rowconfigure(0, weight=1)
        self._cartas_mesa.columnconfigure(tuple(range(12)), weight=1)

        self._placar.grid(row=0, column=0, sticky="ne")
        self._vitorias_mao.grid(row=0, column=5, sticky="nwe")
        self._cartas_jogador_remoto.grid(row=0, column=2, columnspan=2, sticky="nwe")
        acoes.grid(row=2, column=5, sticky="s")
        self._cartas_jogador_local.grid(row=2, column=2, columnspan=2, sticky="swe")
        self._cartas_mesa.grid(row=1, column=0, columnspan=6, sticky="we")

        ind_turno = ttk.Label(
            self._placar, textvariable=self._ind_turno, font="Helvetica 15"
        )
        ind_turno.pack()

        vitorias_mao_remoto = ttk.Label(
            self._vitorias_mao,
            textvariable=self._vitorias_mao_remoto,
            background="red",
            foreground="white",
        )
        vitorias_mao_remoto.pack()

        vitorias_mao_local = ttk.Label(
            self._vitorias_mao,
            textvariable=self._vitorias_mao_local,
            background="blue",
            foreground="white",
        )
        vitorias_mao_local.pack()

    def comecar_partida(self):
        status_partida = self._partida.obter_status_partida()

        if status_partida == "sem partida em andamento":
            start_status = self._dog_server_interface.start_match(2)

            codigo = start_status.get_code()
            mensagem = start_status.get_message()

            if codigo == "0" or codigo == "1":
                tkinter.messagebox.showinfo(message=mensagem)
            elif codigo == "2":
                jogadores = start_status.get_players()
                jogada = self._partida.comecar_partida(jogadores)

                self._dog_server_interface.send_move(jogada)
                status_jogo = self._partida.obtem_status()
                self.atualiza_interface(status_jogo)

                tkinter.messagebox.showinfo(message=mensagem)

    def atualiza_interface(self, status_jogo: dict):
        seu_turno = status_jogo["seu_turno"]
        if seu_turno:
            self._ind_turno.set("Seu turno")
        else:
            self._ind_turno.set("Turno oponente")

        vitorias_mao_remoto = " ".join(status_jogo["vitorias_mao_remoto"])
        self._vitorias_mao_remoto.set(f"Remoto: {vitorias_mao_remoto}")

        vitorias_mao_local = " ".join(status_jogo["vitorias_mao_local"])
        self._vitorias_mao_local.set(f"Local: {vitorias_mao_local}")

        (pontos_local, pontos_remoto) = status_jogo["placar"]
        self._placar_jogador_remoto.set(f"Remoto: {pontos_remoto}/30")
        self._placar_jogador_local.set(f"Local: {pontos_local}/30")

        cartas_jogador_local = status_jogo["cartas_jogador_local"]
        self.__carta_tks = []
        for col, (carta, _) in enumerate(cartas_jogador_local):
            carta_str = carta.para_string()

            carta_img = Image.open(f"../images/cartas/{carta_str}.png")
            carta_img.thumbnail(
                (carta_img.width // 8, carta_img.height // 8),
                Image.LANCZOS,
            )
            carta_tk = ImageTk.PhotoImage(carta_img)
            self.__carta_tks.append(carta_tk)

            carta_label = ttk.Label(master=self._cartas_jogador_local, image=carta_tk)
            carta_label.bind(
                "<Button-1>",
                lambda _, c=cartas_jogador_local[col]: self.jogar_carta(c),
            )
            carta_label.grid(row=0, column=2 * col, columnspan=2, padx=5, pady=3)

        carta_virada_img = Image.open("../images/cartas/red_back.png")
        carta_virada_img.thumbnail(
            (
                carta_virada_img.width // 8,
                carta_virada_img.height // 8,
            ),
            Image.LANCZOS,
        )
        self.__carta_virada_tk = ImageTk.PhotoImage(carta_virada_img)

        num_cartas_oponente = len(status_jogo["cartas_jogador_remoto"])
        for col in range(num_cartas_oponente):
            carta_label = ttk.Label(
                master=self._cartas_jogador_remoto, image=self.__carta_virada_tk
            )
            carta_label.grid(row=0, column=2 * col, columnspan=2, padx=5, pady=3)

        cartas_mesa = status_jogo["cartas_mesa"]
        for w in self._cartas_mesa.winfo_children():
            w.destroy()
        self.__carta_rodada_tks = []
        for col_rodada, cartas_rodada in enumerate(cartas_mesa):
            self._frame_cartas_rodada = ttk.Frame(
                self._cartas_mesa, borderwidth=10, relief=tk.GROOVE
            )
            for col, (carta, _) in enumerate(cartas_rodada):
                carta_str = carta.para_string()

                carta_img = Image.open(f"../images/cartas/{carta_str}.png")
                carta_img.thumbnail(
                    (carta_img.width // 8, carta_img.height // 8),
                    Image.LANCZOS,
                )
                carta_tk = ImageTk.PhotoImage(carta_img)
                self.__carta_rodada_tks.append(carta_tk)

                carta_label = ttk.Label(
                    master=self._frame_cartas_rodada, image=carta_tk
                )
                carta_label.grid(row=0, column=2 * col, columnspan=2, padx=5, pady=3)
            self._frame_cartas_rodada.grid(row=0, column=col_rodada)

        if status_jogo["pedido_em_andamento"] and seu_turno:
            self._popup = self.carregar_popup(infos_popup=status_jogo["infos_popup"])
        elif self._popup != None:
            self._popup.destroy()

        if status_jogo["vencedor"] != 0:
            fim_frame = ttk.Frame(self._janela, borderwidth=20, relief=tk.RAISED)
            if status_jogo["vencedor"] == 1:
                msg_fim = "Você venceu!"
            else:
                msg_fim = "O oponente venceu."
            fim_txt = ttk.Label(fim_frame, text=msg_fim)
            fim_txt.pack(side="top", padx=10, pady=5)
            fim_frame.grid(row=1, column=0, columnspan=6, sticky="n")

    def carregar_popup(self, infos_popup: dict):
        popup = tk.Toplevel(self._janela)
        popup.geometry(
            "400x200"
        )  # Define a largura para 300 pixels e a altura para 200 pixels
        popup.resizable(False, False)  # Desabilita o redimensionamento da janela
        popup.protocol(
            "WM_DELETE_WINDOW", lambda: None
        )  # Desabilita o botão de fechamento
        quadro_de_botoes = tk.Frame(popup)  # Cria um frame para os botões
        quadro_de_botoes.place(
            relx=0.5, rely=0.7, anchor="center"
        )  # Posiciona o frame no centro da janela

        texto_popup = tk.Label(
            popup, text=infos_popup["texto_central"], font=("Helvetica", 16)
        )
        texto_popup.place(
            relx=0.5, rely=0.3, anchor="center"
        )  # Posiciona o texto no centro da janela

        acoes = {
            "aceitar_pedido": self.aceitar_pedido,
            "aumentar_valor": self.aumentar_valor,
            "correr": self.correr,
        }

        botoes_popup = []
        botoes = infos_popup["botoes"]
        for botao in botoes:
            botao_temp = tk.Button(
                quadro_de_botoes,
                text=botao,
                command=acoes[botao],
                font=("Helvetica", 12),
            )
            botao_temp.pack(side="left", padx=5)  # Adiciona padding horizontal
            botoes_popup.append(botao_temp)
        return popup

    def receber_jogada(self, jogada: dict):
        self._partida.receber_jogada(jogada)
        status_jogo = self._partida.obtem_status()
        self.atualiza_interface(status_jogo)

    def envido(self):
        jogada = self._partida.envido()
        if jogada:
            status_jogo = self._partida.obtem_status()
            self.atualiza_interface(status_jogo=status_jogo)
            self._dog_server_interface.send_move(move=jogada)
        else:
            print("[JOGO] Não é seu turno, ou já ocorreu flor ou envido na mao atual")

    def flor(self):
        jogada = self._partida.flor()
        if jogada:
            status_jogo = self._partida.obtem_status()
            self.atualiza_interface(status_jogo=status_jogo)
            self._dog_server_interface.send_move(move=jogada)
        else:
            print("[JOGO] Não é seu turno, ou já ocorreu flor ou envido na mao atual")

    def truco(self):
        jogada = self._partida.truco()
        if jogada:
            status_jogo = self._partida.obtem_status()
            self.atualiza_interface(status_jogo=status_jogo)
            self._dog_server_interface.send_move(move=jogada)
        else:
            print("[JOGO] Não é seu turno, ou já ocorreu um truco na mao atual")

    def aumentar_valor(self):
        jogada = self._partida.aumentar_valor()
        status_jogo = self._partida.obtem_status()
        self.atualiza_interface(status_jogo)
        self._dog_server_interface.send_move(jogada)

    def receber_inicio(self, status_inicio: StartStatus):
        self.restaurar_estado_inicial()

        jogadores = status_inicio.get_players()

        self._partida.receber_inicio(jogadores)

        mensagem = status_inicio.get_message()
        tkinter.messagebox.showinfo(message=mensagem)

        status_jogo = self._partida.obtem_status()
        self.atualiza_interface(status_jogo)

    def restaurar_estado_inicial(self):
        status_partida = self._partida.obter_status_partida()

        if status_partida == "encerrada" or status_partida == "abandonada":
            self._partida.restaurar_estado_inicial()
            self.encher_janela_principal()

    def receive_withdrawal_notification(self):
        self._partida.abandonar_partida()
        status_jogo = self._partida.obtem_status()
        self.atualiza_interface(status_jogo)
        print("[JOGO] O oponente abandonou a partida.")

    def jogar_carta(self, carta: tuple):
        jogada = self._partida.jogar_carta(carta)

        if jogada:
            self._dog_server_interface.send_move(move=jogada)

            status_jogo = self._partida.obtem_status()
            self.atualiza_interface(status_jogo=status_jogo)
        else:
            print("[JOGO] Não é seu turno!")

    def aceitar_pedido(self):
        jogada = self._partida.aceitar_pedido()
        self._dog_server_interface.send_move(move=jogada)
        status_jogo = self._partida.obtem_status()
        self.atualiza_interface(status_jogo=status_jogo)

    def correr(self):
        jogada = self._partida.correr()

        if jogada:
            self._dog_server_interface.send_move(move=jogada)
            status_jogo = self._partida.obtem_status()
            self.atualiza_interface(status_jogo)
        else:
            print("[JOGO] Não é seu turno!")
