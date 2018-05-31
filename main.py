import pygame
import sys
import time
from utils.constants import WIDTH, HIGH, ROWS_NUMBER, COLUMNS_NUMBER, nodes_visited
from utils.functions import chessboard, position_random, search_white_horse, minimax
from models.Field import Cursor, Image
from models.Node import Node
from pygame.locals import *
import threading


class Main(object):
    """
    Autor: Carlos Almario
    Fecha: Mayo 3 2018
    Clase para crear la pantalla del juego
    """

    def __init__(self):
        """
        Autor: Carlos Almario
        Fecha: mayo 10 2018
        Se sobrescribe el init para crear las variables de la clase Main.
        """

        pygame.init()
        self.window = pygame.display.set_mode((WIDTH, HIGH))
        self.background_window = pygame.Color(202, 118, 34)
        self.background_two_window = pygame.Color(255, 255, 255)
        pygame.display.set_caption("AlphaZero")
        self.square_white = pygame.image.load("images/white.jpg")
        self.square_black = pygame.image.load("images/black.jpg")
        self.square_red = pygame.image.load("images/red.png")
        self.white_horse = pygame.image.load("images/white_horse.png")
        self.black_horse = pygame.image.load("images/black_horse.png")
        self.coin = pygame.image.load("images/coin.png")
        self.button = Image((WIDTH - 297) / 2, (HIGH - 192) / 2, "images/button.png")
        self.human_items = 0
        self.cursor = Cursor()
        self.player = 0
        self.board = chessboard()
        self.node = Node()
        self.run()

    def run(self):
        """
        Autor: Carlos Almario
        Fecha: Mayo 16 2018
        Método para correr la ventana del juego y escuchar los eventos que suceden en ella.
        las Siglas W corresponde al color White blanco en español indica que alli esta la ficha blanca,
        la sigla B corresponde al color Black negro en español indica que alli hay una ficha negra en el
        tablero
        """

        c = 0

        start = False
        while True:

            pygame.display.update()
            self.cursor.update()
            # condición para pintar el tablero
            if start:
                self.window.fill(self.background_window)
                self.rewrite()

                possible_movimenents = self.node.possible_movements(self.board)

                for i in range(len(self.board)):
                    for j in range(len(self.board)):

                        if (i+j) % 2 != 0:
                            self.window.blit(self.square_black, (j*80,i*80))
                        else:
                            self.window.blit(self.square_white, (j * 80, i * 80))

                        if self.board[i][j] == 'W':
                            self.window.blit(self.white_horse, (j * 86, i * 80))

                        if self.board[i][j] == 'B':
                            self.window.blit(self.black_horse, (j * 86, i * 80))

                        if self.board[i][j] == 'C':
                            self.window.blit(self.coin, (j * 86, i * 80))

                for i in range(len(possible_movimenents)):
                    pos_x, pos_y = possible_movimenents[i][0], possible_movimenents[i][1]
                    if self.board[pos_x][pos_y] != 'C':
                        self.window.blit(self.square_red, (pos_y * 80, pos_x * 80))

            else:
                self.draw_main()

            # ciclo For que está escuchando los eventos
            for event in pygame.event.get():

                if event.type == pygame.MOUSEBUTTONDOWN:

                    # condicion para el inicio del juego
                    if start:
                        position_x, position_y = int(self.cursor.top/80), int(self.cursor.left/80)

                        # condicion que evalua si donde se da click es una casila del tablero
                        if position_x in range(6) and position_y in range(6):
                            """
                            bucle que busca en la lista de posibles movimientos si la casilla donde se da cick es un
                            movimiento posible
                            """
                            for i in range(len(possible_movimenents)):
                                position_list_x = possible_movimenents[i][0]
                                position_list_y = possible_movimenents[i][1]

                                if position_x == position_list_x and position_y == position_list_y:
                                    if self.player:
                                        self.board[position_x][position_y] = 'B'
                                        self.board[self.node.position_x][self.node.position_y] = '0'
                                        self.node.position_x = position_x
                                        self.node.position_y = position_y
                                        self.player = 0
                                        if not self.player:
                                            white_horse_node = search_white_horse(self.board)
                                            thread = threading.Thread(target=self.execute_minimax,
                                                                      args=(white_horse_node,))
                                            thread.start()

                    if self.cursor.colliderect(self.button.rect) and not start:
                        self.create_coin()
                        white_horse_node = self.create_white_horse()
                        self.create_black_horse()
                        thread = threading.Thread(target=self.execute_minimax, args=(white_horse_node,))
                        thread.start()
                        start = True

                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

    def create_white_horse(self):
        """
        Autor: Carlos almario
        Fecha: mayo 25 2018
        método encargado de crear el caballo blanco en la matriz
        """
        # ubicacion del caballo blanco

        ramdom_x, ramdom_y = position_random(ROWS_NUMBER, COLUMNS_NUMBER)
        if not self.board[ramdom_x][ramdom_y].strip('0'):
            node = Node()
            node.type = 0
            node.node = None
            node.position_x = ramdom_x
            node.position_y = ramdom_y
            self.board[ramdom_x][ramdom_y] = 'W'
            print("nodo padre: "+str(node)+"\n")
            return node

    def create_black_horse(self):
        """
        Autor: Carlos Almario
        Fecha: mayo 25 2018
        método encargado de crear el caballo negro en la matriz
        """
        # ubicacion del caballlo begro
        ramdom_x, ramdom_y = position_random(ROWS_NUMBER, COLUMNS_NUMBER)

        if not self.board[ramdom_x][ramdom_y].strip('0'):
            self.node = Node()
            self.node.type = 1
            self.node.position_x = ramdom_x
            self.node.position_y = ramdom_y
            self.board[ramdom_x][ramdom_y] = 'B'

    def create_coin(self):
        """
        Autor: Carlos almario
        Fecha: mayo 25 2018
        método encargado de crear el caballo blanco en la matriz
        """
        # ubicacion del caballo blanco
        for i in range(6):
            ramdom_x, ramdom_y = position_random(ROWS_NUMBER, COLUMNS_NUMBER)
            if not self.board[ramdom_x][ramdom_y].strip('0'):
                self.board[ramdom_x][ramdom_y] = 'C'

    def rewrite(self):

        """
        Autor: Carlos Almario
        Fecha: mayo 25 2018
        funcion para pintar imagenes en el lienzo derecho de la pantalla
        """
        pos_x = WIDTH-220
        pos_y = 10
        image = Image(pos_x, pos_y, 'images/name.png')
        image.draw(self.window)

    def draw_main(self):
        self.window.fill(self.background_two_window)
        self.button.draw(self.window)

    def execute_minimax(self, node):
        node_max = node
        node_min = self.node
        best_action, turn = minimax(node_max, node_min, self.board, 1)
        self.player = turn
        print(best_action)
        self.board[node.position_x][node.position_y] = '0'
        self.board[best_action.position_x][best_action.position_y] = 'W'


main_window = Main()

