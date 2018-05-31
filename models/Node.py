from sys import maxsize
from utils.constants import nodes_visited

class Node(object):
    """
    Autor: carlos Almario
    Fecha: abril 25 2018
    Clase Node

    clase que se usará para la creación del arbol minimax
    """
    def __init__(self):
        """
        Autor: Carlos Almario
        Fecha: abril 25 2018
        Se sobrescribe el init para crear las variables de la clase Max.
        """
        self.node = self.__class__
        self.position_x = 0
        self.position_y = 0
        self.caught_items = 0
        self.depth = 0
        self.type = 0
        self.value = 0
        self.moves = [[2, 1], [1, 2], [-2, 1], [2, -1], [-1, 2], [1, -2], [-2, -1], [-1, -2]]
        self.tree = []
        self.items_in_board = 0
        self.board = []
        self.create_tree()

    def __str__(self):
        """
        Autor: Kevin Cardona
        Fecha: 10 de marzo 2018
        Método para la representación de la clase nodo
        :return:
        """
        return "[{0}-{1}]".format(self.position_x, self.position_y)

    def create_tree(self):
        if self.depth > 0 and self.items_in_board > 0:
            possible_movements = self.possible_movements(self.board)
            for i in range(len(possible_movements)):
                pos_x, pos_y = possible_movements[i][0], possible_movements[i][1]
                self


    def possible_movements(self, chessboard):
        """
        Funcion que calculo los posibes movimientos que tiene el nodo
        :param chessboard:
        :return: movements_possible, Lista con los movimientos posibles de una ficha
        """

        movements_possible = []
        for n in range(8):
            if (self.position_x + self.moves[n][0]) in range(6) and (self.position_y + self.moves[n][1]) in range(6):
                position_x = self.position_x + self.moves[n][0]
                position_y = self.position_y + self.moves[n][1]

                if chessboard[position_x][position_y] == '0' or chessboard[position_x][position_y] == 'C':
                    v = [position_x, position_y]
                    movements_possible.append(v)

        return movements_possible

    def in_list(self, list):
        """
            Autor: Carlos Almario
            Fecha: Mayo 26 2018
            metodo para mirar si el nodo esta en una lista determinada
            :param list: lista de nodos en la cual se va a buscar
            :return: in_list, variable booleana que indica si está o no o el nodo en la lista
        """
        in_list = False

        for n in list:
            if self.is_equal(n):
                in_list = True

        return in_list

    def is_equal(self, other):
        """
            Autor: Carlos Almario
            Fecha: Mayo 26 2018
            metodo para comparar el estado de Mario
            :param other: Nodo con el cual se va a comparar
            :return: bool,
        """
        if other is None:
            return False

        if self.position_x == other.position_x and self.position_y == other.position_y and self.type == other.type:
            return True
        else:
            return False

    def real_val(self, items, items_max, items_min):
        """value = 0
        if node_min.caught_items > self.caught_items:
            value = self.caught_items - node_min.caught_items * -1
        elif node_min.caught_items < self.caught_items :
            value = self.caught_items - node_min.caught_items
        return value"""
        value = 0
        if self.depth == 8 and items > 0:
            value = items_max - items_min
        elif items == 0:
            if self.type:
                value = 40
            else:
                value = -40
        return value

    def is_goal(self, board):
        field = board[self.position_x][self.position_y]
        if field == 'C':
            return True
        return False

    def minimax(self, node_max, node_min, board, items):
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
        best_utility = -1
        node_max = node_max
        node_min = node_min
        possible_moviments = node_min.possible_movements(board)
        for i in range(len(possible_moviments)):
            pos_x, pos_y = possible_moviments[i][0], possible_moviments[i][1]
            son_node_min = Node()
            son_node_min.position_x = pos_x
            son_node_min.position_y = pos_y
            son_node_min.type = 1
            son_node_min.node = node_min
            son_node_min.depth = node_max.depth + 1

            if son_node_min.caught_items < items:
                if son_node_min.is_goal(board):
                    son_node_min.caught_items = son_node_min.node.caught_items + 1
                    items = items - 1
                else:
                    son_node_min.caught_items = son_node_min.node.caught_items

            utility = son_node_min.valor_min(node_max, son_node_min, board, items)
            if utility > best_utility:
                best_action = son_node_min
                best_utility = utility
                print(best_utility)
                print(items)

        return best_action, 1

    def valor_min(self, node_max, node_min, board, items):
        node_max = node_max
        min_value = maxsize

        if node_min.depth == 8:
            return node_max.real_val(node_min, items)

        possible_moviments = node_max.possible_movements(board)
        for i in range(len(possible_moviments)):
            pos_x, pos_y = possible_moviments[i][0], possible_moviments[i][1]
            son_node_max = Node()
            son_node_max.position_x = pos_x
            son_node_max.position_y = pos_y
            son_node_max.node = node_max
            son_node_max.type = 0
            son_node_max.depth = node_min.depth + 1
            if son_node_max.caught_items < items:
                if son_node_max.is_goal(board):
                    son_node_max.caught_items = son_node_max.node.caught_items + 1
                    items = items - 1
                else:
                    son_node_max.caught_items = son_node_max.node.caught_items

            utility = son_node_max.valor_max(node_min, son_node_max, board, items)
            if utility < min_value:
                min_value = utility
        return min_value

    def valor_max(self, node_min, node_max, board, items):
        node_min = node_min
        max_value = maxsize * -1
        if node_max.depth == 8 or not items:
            return node_max.real_val(node_min, items)

        possible_moviments = node_min.possible_movements(board)
        for i in range(len(possible_moviments)):
            pos_x, pos_y = possible_moviments[i][0], possible_moviments[i][1]
            son_node_min = Node()
            son_node_min.node = node_min
            son_node_min.position_x = pos_x
            son_node_min.position_y = pos_y
            son_node_min.type = 1
            son_node_min.depth = node_max.depth + 1
            if son_node_min.caught_items < items:
                if son_node_min.is_goal(board):
                    son_node_min.caught_items = son_node_min.node.caught_items + 1
                    items = items - 1
                else:
                    son_node_min.caught_items = son_node_min.node.caught_items

            utility = son_node_min.valor_min(node_max, son_node_min, board, items)
            if utility > max_value:
                max_value = utility

        return max_value

    def number_items(self, board):
        items = 0
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j].strip('C'):
                    items += 1
        return items