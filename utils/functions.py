from utils.constants import CHESSBOARD, tree_development
from models.Node import Node
from random import randint
from sys import maxsize


def chessboard():
    """
    Autor: Carlos Almario
    Fecha: mayo 24 2018

    :return: CHESSBOARD, Tablero en limpio para comenzar las partidas
    """
    return CHESSBOARD


def search_black_horse(board):

    """
    Autor: Kevin Cardona
    Fecha: marzo 17 2018
    Método que encuentra la posición del mario
    :param board: matriz que representa el tablero
    :return: node, instancia de la clase Nodo
    """
    for position_x in range(len(board)):
        for position_y in range(len(board)):
            if board[position_x][position_y] == 'B':
                node = Node()
                node.position_x = position_x
                node.position_y = position_y
                node.type = 1
                return node


def position_random(max_number_x, max_number_y):
        """
        Autor: Carlos Almario
        Fecha: mayo 25 2018
        función auxiliar para obtener el ramdon de una posición en la matriz
        :param max_number_x: máximo numero para x
        :param max_number_y: máximo numero para y
        :return: random_x, random_y
        """
        random_x = randint(0, max_number_x-1)
        random_y = randint(0, max_number_y-1)

        return random_x, random_y