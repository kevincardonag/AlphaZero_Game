from utils.constants import tree_development



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
        self.moves = [[2, 1], [1, 2], [-2, 1], [2, -1], [-1, 2], [1, -2], [-2, -1], [-1, -2]]

    def possible_movements(self, chessboard):
        """
        Funcion que calculo los posibes movimientos que tiene el nodo
        :param chessboard:
        :return: movements_possible, Lista con los movimientos posibles de una ficha
        """

        movements_possible = []
        for n in range(8):
            if (self.position_x + self.moves[n][0]) in range(6) and (self.position_y + self.moves[n][1]) in range(6):
                if chessboard[self.position_x + self.moves[n][0]][self.position_y + self.moves[n][1]] == '0':
                    v = [self.position_x + self.moves[n][0], self.position_y + self.moves[n][1]]
                    movements_possible.append(v)
        return movements_possible

