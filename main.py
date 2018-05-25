import pygame
import sys
import time
from utils.constants import WIDTH, HIGH, ROWS_NUMBER, COLUMNS_NUMBER, tree_development
from utils.functions import chessboard
from models.Field import Cursor, Image
from models.Node import Node
from random import randint
from pygame.locals import *


class Main(object):
    """
    Autor: Carlos Almario
    Fecha: Mayo 3 2018
    Clase para crear la pantalla del juego
    """

    def __init__(self):
        """
        Autor: Kevin Cardona
        Fecha: Marzo 6 2018
        Se sobrescribe el init para crear las variables de la clase Main.
        """

        pygame.init()
        self.window = pygame.display.set_mode((WIDTH,HIGH))
        self.background_window = pygame.Color(202, 118, 34)
        self.background_two_window = pygame.Color(255, 255, 255)
        pygame.display.set_caption("AlphaZero")
        self.square_white = pygame.image.load("images/white.jpg")
        self.square_black = pygame.image.load("images/black.jpg")
        self.square_red = pygame.image.load("images/red.png")
        self.white_horse = pygame.image.load("images/white_horse.png")
        self.black_horse = pygame.image.load("images/black_horse.png")
        self.cursor = Cursor()
        self.board = chessboard()
        self.node = Node()
        self.run()

    def run(self):
        """
        Autor: Carlos Almario
        Fecha: Mayo 16 2018
        Método para correr la ventana del juego y escuchar los eventos que suceden en ella.
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

                for iterator in range(len(possible_movimenents)):
                    self.window.blit(self.square_red,
                                 (possible_movimenents[iterator][1] * 80, possible_movimenents[iterator][0] * 80))
            else:
                self.window.fill(self.background_two_window)
                button = Image((WIDTH-297)/2, (HIGH-192)/2, "images/button.png")
                button.draw(self.window)

            # cliclo For que está escuchando los eventos
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
                            for iterator in range(len(possible_movimenents)):
                                position_list_x = possible_movimenents[iterator][0]
                                position_list_y = possible_movimenents[iterator][1]

                                if position_x == position_list_x and position_y == position_list_y:
                                    self.board[position_x][position_y] = 'B'
                                    self.board[self.node.position_x][self.node.position_y] = '0'
                                    self.node.position_x = position_x
                                    self.node.position_y = position_y

                    if self.cursor.colliderect(button.rect) and not start:
                        self.create_white_horse()
                        self.create_black_horse()
                        start = True

                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

    def create_white_horse(self):
        """
        Autor: Kevin Cardona
        Fecha: mayo 25 2018
        método encargado de crear el caballo blanco en la matriz
        """
        # ubicacion del caballo blanco

        ramdom_x, ramdom_y = self.position_random(ROWS_NUMBER, COLUMNS_NUMBER)
        if not self.board[ramdom_x][ramdom_y].strip('0'):
            node = Node()
            node.type = 0
            node.node = None
            node.position_x = ramdom_x
            node.position_y = ramdom_y
            self.board[ramdom_x][ramdom_y] = 'W'

    def create_black_horse(self):
        """
        Autor: Kevin Cardona
        Fecha: mayo 25 2018
        método encargado de crear el caballo negro en la matriz
        """
        # ubicacion del caballlo begro
        ramdom_x, ramdom_y = self.position_random(ROWS_NUMBER, COLUMNS_NUMBER)

        if not self.board[ramdom_x][ramdom_y].strip('0'):
            self.node = Node()
            self.node.type = 1
            self.node.position_x = ramdom_x
            self.node.position_y = ramdom_y
            self.board[ramdom_x][ramdom_y] = 'B'

    def position_random(self, max_number_x, max_number_y):
        """
        Autor: Kevin Cardona
        Fecha: mayo 25 2018
        función auxiliar para obtener el ramdon de una posición en la matriz
        :param max_number_x: máximo numero para x
        :param max_number_y: máximo numero para y
        :return: random_x, random_y
        """
        random_x = randint(0, max_number_x-1)
        random_y = randint(0, max_number_y-1)

        return random_x, random_y

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


main_window = Main()

