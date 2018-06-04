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
        self.type = -1
        self.value = 0
        self.items_min = 0
        self.items_max = 0
        self.moves = [[2, 1], [1, 2], [-2, 1], [2, -1], [-1, 2], [1, -2], [-2, -1], [-1, -2]]
        self.tree = []
        self.items_in_board = 0
        self.board = []

    def __str__(self):
        """
        Autor: Kevin Cardona
        Fecha: 10 de marzo 2018
        Método para la representación de la clase nodo
        :return:
        """
        return "[{0}-{1}]".format(self.position_x, self.position_y)

    def possible_movements(self, chessboard):
        """
        Autor: Carlos Almario
        Fecha: 2 junio 2018
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

    def real_val(self, items, items_max, items_min):
        """
        Autor: Carlos Almario
        Fecha: 2 junio 2018
        Metodo que calcula la utilidad de los nodos para efectuar la mejor opcion del algoritmo minimax

        :param items:
        :param items_max:
        :param items_min:
        :return: value:  valor de la utilidad que llevara el nodo
        """
        if items == 0 or self.depth == 8:
            if items == 0 and items_max < items_min:
                return 1000000000
            return items_max - items_min
        return maxsize

    def is_goal(self, board):
        """
        Autor: Carlos Almario
        Fecha: 2 junio 2018

        Metodo que se encarga de responder si en una posicion determinada hay una moneda ('C', coin)
        :param board: tablero de juego
        :return: boolean: variable booleana si existe o no una moneda
        """
        field = board[self.position_x][self.position_y]
        if field == 'C':
            return True
        return False

    def minimax(self, node_max, board, items, items_max, items_min):
        """
        Autor: Carlos Almario
        Fecha: 2 junio 2018

        Metodo minimax que efectua la mejor opción de juego para la maquina con profundidad 8, este metodo construye
        el arbol por profundidad y o explora de esa  manera, solo retorna la mejor accion cuando ha explorado
        todo el arbol
        :param node_max: estado inicial del juego
        :param board: tablero de juego donde se encuentran las monedas  y las fichas ('W', ficha blanca), ('B', ficha negra)
        :param items: número de items que hay en el tablero
        :param items_max: numero de items que tiene la maquina hasta el momento
        :param items_min: número de items que tiene el usuario hasta el momento
        :return: best_action: nodo que es la mejor accion del juego, 1 numero que idica el turno de juego
        """
        self.items_in_board = items
        self.items_max = items_max
        self.items_min = items_min
        best_action = None
        best_utility = -maxsize
        node_max = node_max
        possible_moviments = node_max.possible_movements(board)
        # ciclo que recorreo las posibles acciones de ese estado
        for i in range(len(possible_moviments)):
            pos_x, pos_y = possible_moviments[i][0], possible_moviments[i][1]
            son_node_min = Node()
            son_node_min.position_x = pos_x
            son_node_min.position_y = pos_y
            son_node_min.type = 1
            son_node_min.node = node_max
            son_node_min.depth = node_max.depth + 1

            if son_node_min.is_goal(board):
                self.items_min += 1
                if self.items_in_board > 0:
                    self.items_in_board -= 1
            son_node_min.value = self.real_val(self.items_in_board, self.items_max, self.items_min)
            # asignación del valor al nodo

            utility = son_node_min.valor_min(son_node_min, board, self.items_in_board, self.items_max, self.items_min)
            if utility >= best_utility:
                print(utility)
                best_action = son_node_min
                best_utility = utility

        return best_action, 1

    def valor_min(self, node_min, board, items, items_max, items_min):
        """
        Autor: Carlos Almario
        Fecha: 2 junio 2018

        Metodo que busca el valor minimo en el arbol

        :param node_min: estado min del arbol
        :param board: tablero de juego
        :param items: numero de items en juego
        :param items_max: numero de items que tiene la maquina
        :param items_min: numero de items que tiene min
        :return: min_value: valor minimo
        """
        node_min = node_min
        min_value = maxsize
        self.items_min = items_min
        self.items_max = items_max
        self.items_in_board = items
        if node_min.depth == 8 or (abs(node_min.value) != maxsize):
            return node_min.value * node_min.type

        possible_moviments = node_min.possible_movements(board)
        # ciclo que recorreo las posibles acciones de ese estado
        for i in range(len(possible_moviments)):
            pos_x, pos_y = possible_moviments[i][0], possible_moviments[i][1]
            son_node_max = Node()
            son_node_max.position_x = pos_x
            son_node_max.position_y = pos_y
            son_node_max.node = node_min
            son_node_max.type = -1
            son_node_max.depth = node_min.depth + 1

            if son_node_max.is_goal(board):
                self.items_max += 1
                if self.items_in_board > 0:
                    self.items_in_board -= 1

            son_node_max.value = self.real_val(self.items_in_board, self.items_max, self.items_min)
            # asignación del valor al nodo
            utility = son_node_max.valor_max(son_node_max, board, self.items_in_board, self.items_max, self.items_min)
            if utility < min_value:
                min_value = utility

        return min_value

    def valor_max(self, node_max, board, items, items_max, items_min):
        """
        Autor: Carlos Almario
        Fecha: 2 junio 2018

        Metodo que explora el mejor valor es decir MAX
        :param node_max: estado max del arbol, para miras los posibles movimientos
        :param board: tablero de juego
        :param items: items en juego
        :param items_max: items que posee MAX en el momento
        :param items_min: items que tiene MIN en el momento
        :return: max_value:  mejor valor
        """
        node_max = node_max
        max_value = -maxsize
        self.items_min = items_min
        self.items_max = items_max
        self.items_in_board = items
        if node_max.depth == 8 or (abs(node_max.value) != maxsize):
            return node_max.value * node_max.type
        possible_moviments = node_max.possible_movements(board)
        # ciclo que recorreo las posibles acciones de ese estado
        for i in range(len(possible_moviments)):
            pos_x, pos_y = possible_moviments[i][0], possible_moviments[i][1]
            son_node_min = Node()
            son_node_min.node = node_max
            son_node_min.position_x = pos_x
            son_node_min.position_y = pos_y
            son_node_min.type = 1
            son_node_min.depth = node_max.depth + 1
            if son_node_min.is_goal(board):
                self.items_min += 1
                if self.items_in_board > 0:
                    self.items_in_board -= 1
            son_node_min.value = self.real_val(self.items_in_board, self.items_max, self.items_min)

            utility = son_node_min.valor_min(son_node_min, board, self.items_in_board, self.items_max, self.items_min)
            if utility > max_value:
                max_value = utility

        return max_value

