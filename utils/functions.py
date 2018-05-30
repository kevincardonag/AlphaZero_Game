from utils.constants import CHESSBOARD, tree_development, nodes_visited
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


def search_white_horse(board):

    """
    Autor: Kevin Cardona
    Fecha: marzo 17 2018
    Método que encuentra la posición del mario
    :param board: matriz que representa el tablero
    :return: node, instancia de la clase Nodo
    """
    for position_x in range(len(board)):
        for position_y in range(len(board)):
            if board[position_x][position_y] == 'W':
                node = Node()
                node.position_x = position_x
                node.position_y = position_y
                node.depth = 0
                node.type = 0
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


def tree(node, board):
    father_node = node
    possible_moviments = father_node.possible_movements(board)
    if father_node.depth == 8:
        return True, father_node

    nodes_visited.append(father_node)

    for i in range(len(possible_moviments)):
        pos_x, pos_y = possible_moviments[i][0], possible_moviments[i][1]
        son_node = Node()
        son_node.position_x = pos_x
        son_node.position_y = pos_y

        son_node.node = father_node
        son_node.depth = father_node.depth + 1
        if father_node.type:
            son_node.type = 0
        else:
            son_node.type = 1

        son_node.value = son_node.real_val(board)

        print(str(son_node.position_x) + "," + str(son_node.position_y) + " Padre: " + str(
                son_node.node.position_x) + "," + str(
                son_node.node.position_y) + " tipo: " + str(son_node.type) + " profundidad: " + str(
                son_node.depth) + "Valor: " + str(son_node.value))
        tree_development.append(son_node)

    del tree_development[0]
    next_node = tree_development[0]

    #print("proximo a espandir: "+str(next_node.position_x)+";"+str(next_node.position_y))
    return False, next_node

