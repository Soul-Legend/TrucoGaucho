#!/usr/bin/python

import os

from player_interface import PlayerInterface


def main():
    # Garante que o usuário pode executar o programa a partir de qualquer diretório.
    try:
        caminho_exec = os.path.dirname(__file__)
        os.chdir(caminho_exec)
    except Exception:
        pass

    PlayerInterface()


if __name__ == "__main__":
    main()
