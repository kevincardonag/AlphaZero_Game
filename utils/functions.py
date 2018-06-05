from utils.constants import tree_development, nodes_visited
from models.Node import Node
from random import randint
from sys import maxsize


def chessboard(items):
    """
    Autor: Carlos Almario
    Fecha: mayo 24 2018

    :return: CHESSBOARD, Tablero en limpio para comenzar las partidas
    """

    CHESSBOARD = [

        ['0', '0', '0', '0', '0', '0'],
        ['0', '0', '0', '0', '0', '0'],
        ['0', '0', '0', '0', '0', '0'],
        ['0', '0', '0', '0', '0', '0'],
        ['0', '0', '0', '0', '0', '0'],
        ['0', '0', '0', '0', '0', '0'],

    ]
    count = 0

    while True:
        ramdom_x = randint(0, 5)
        ramdom_y = randint(0, 5)

        if CHESSBOARD[ramdom_x][ramdom_y] == 'C':
            continue
        else:
            CHESSBOARD[ramdom_x][ramdom_y] = 'C'
            count += 1

        if count == items:
            break

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


def minimax(node_max, board, items, items_machine, items_human):
        """
        Autor: Carlos Almario
        Fecha: Mayo 26 2018
        metodo
        :param node_max:
        :param node_min:
        :param board:
        :param items:
        :return:
        """
        items = items
        best_action = None
        best_utility = -maxsize
        node_max = node_max
        items_max = items_machine
        items_min = items_human
        possible_movements = node_max.possible_movements(board)
        for i in range(len(possible_movements)):
            pos_x, pos_y = possible_movements[i][0], possible_movements[i][1]
            son_node_min = Node()
            son_node_min.position_x = pos_x
            son_node_min.position_y = pos_y
            son_node_min.type = 1
            son_node_min.node = node_max
            son_node_min.depth = node_max.depth + 1
            if son_node_min.is_goal(board):
                son_node_min.caught_items = son_node_min.node.caught_items + 1
                items = items - 1
                items_min += 1
            else:
                son_node_min.caught_items = son_node_min.node.caught_items

            #son_node_min.value = son_node_min.real_val(items, items_max, items_min)

            #print(str(son_node_min)+" Valor: "+str(son_node_min.value)+" tipo: "+str(son_node_min.type)+"items: "+str(items)+"padre: "+str(son_node_min.node))
            utility = valor_min(son_node_min, board, items, items_max, items_min)

            if utility > best_utility:
                best_action = son_node_min
                best_utility = utility
                print("mejor utilidad: "+str(best_utility))
                print("items: "+str(items))
                print("items min: " + str(items_min))
                print("items max: " + str(items_max))
                print("items: " + str(items))

            return best_action, 1


def valor_min(node_min, board, items, items_max, items_min):
        node_min = node_min
        min_value = maxsize
        if node_min.depth == 4:
            return node_min.real_val(items, items_max, items_min)

        possible_movements = node_min.possible_movements(board)
        for i in range(len(possible_movements)):
            pos_x, pos_y = possible_movements[i][0], possible_movements[i][1]
            son_node_max = Node()
            son_node_max.position_x = pos_x
            son_node_max.position_y = pos_y
            son_node_max.node = node_min
            son_node_max.type = 0
            son_node_max.depth = node_min.depth + 1
            if son_node_max.is_goal(board):
                son_node_max.caught_items = son_node_max.node.caught_items + 1
                items = items - 1
                items_max += 1
            else:
                son_node_max.caught_items = son_node_max.node.caught_items

            #son_node_max.value = son_node_max.real_val(items, items_max, items_min)

            #print(str(son_node_max)+" Valor: "+str(son_node_max.value) + " tipo: " + str(son_node_max.type)+"items: "+str(items)+"padre: "+str(son_node_max.node))

            utility = valor_max(son_node_max, board, items, items_max, items_min)

            if utility < min_value:
                min_value = utility

        return min_value


def valor_max(node_max, board, items, items_max, items_min):
    node_max = node_max
    max_value = -maxsize
    if node_max.depth == 4:

        return node_max.real_val(items, items_max, items_min)

    possible_movements = node_max.possible_movements(board)
    for i in range(len(possible_movements)):
        pos_x, pos_y = possible_movements[i][0], possible_movements[i][1]
        son_node_min = Node()
        son_node_min.node = node_max
        son_node_min.position_x = pos_x
        son_node_min.position_y = pos_y
        son_node_min.type = 1
        son_node_min.depth = node_max.depth + 1
        if son_node_min.is_goal(board):
            son_node_min.caught_items = son_node_min.node.caught_items + 1
            items = items - 1
            items_min += 1
        else:
            son_node_min.caught_items = son_node_min.node.caught_items
        son_node_min.value = son_node_min.real_val(items, items_max, items_min)
        if son_node_min.depth == 4:
            utility = valor_min(son_node_min, board, items, items_max, items_min)

        #print(str(son_node_min)+" Valor: "+str(son_node_min.value) + " tipo: " + str(son_node_min.type)+" items: "+str(items)+" padre: "+str(son_node_min.node))

        if utility > max_value:
            max_value = utility

    return max_value

