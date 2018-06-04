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
        self.font = pygame.font.SysFont("images/SuperMario256.ttf", 20)
        self.coin = pygame.image.load("images/coin.png")
        self.button = Image((WIDTH - 297) / 2, (HIGH - 192) / 2, "images/button.png")
        self.text_thinking = ""
        self.human_items = 0
        self.machine_items = 0
        self.items = 3
        self.game_over_ = False
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

        start = False
        while True:

            pygame.display.update()
            self.cursor.update()

            # condición para pintar el tablero
            if start and not self.game_over_:
                self.window.fill(self.background_window)
                self.draw_text_right()
                self.rewrite()
                possible_movimenents = self.node.possible_movements(self.board)

                # ciclo que pinta la matriz del juego
                for i in range(len(self.board)):
                    for j in range(len(self.board)):
                        # condicion para pintar los recuadros blanco y negro
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
                # pinta de color verde los posibes movimientos del usuario
                for i in range(len(possible_movimenents)):
                    pos_x, pos_y = possible_movimenents[i][0], possible_movimenents[i][1]
                    if self.board[pos_x][pos_y] != 'C':
                        self.window.blit(self.square_red, (pos_y * 80, pos_x * 80))

            elif not self.game_over_:
                self.draw_main()
            else:
                self.game_over()

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
                                # condicion  que examina las posiciones de los clicks
                                if position_x == position_list_x and position_y == position_list_y:
                                    # condicion que examina si el turno es para el usuario
                                    if self.player:
                                        if self.board[position_x][position_y] == 'C':
                                            self.human_items += 1
                                            self.items -= 1
                                            if self.items == 0:
                                                self.game_over_ = True

                                        self.board[position_x][position_y] = 'B'
                                        self.board[self.node.position_x][self.node.position_y] = '0'
                                        self.node.position_x = position_x
                                        self.node.position_y = position_y
                                        self.player = 0
                                        # condicion que examina si es el turno de la  maquina
                                        if not self.player:
                                            white_horse_node = search_white_horse(self.board)
                                            thread = threading.Thread(
                                                                    target=self.execute_minimax,
                                                                    args=(
                                                                            white_horse_node, self.items,
                                                                            self.machine_items,
                                                                            self.human_items,
                                                                        )
                                                                    )
                                            thread.start()
                    # condiicón de inicio del juego
                    if self.cursor.colliderect(self.button.rect) and not start and not self.game_over_:
                        #self.create_coin()
                        white_horse_node = self.create_white_horse()
                        self.create_black_horse()
                        thread = threading.Thread(
                            target=self.execute_minimax,
                            args=(
                                white_horse_node, self.items,
                                self.machine_items,
                                self.human_items,
                            )
                        )
                        thread.start()
                        start = True
                    elif self.game_over_:
                        self.game_over()

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
            node.board = self.board
            self.board[ramdom_x][ramdom_y] = 'W'
            return node
        else:
            self.create_white_horse()

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
        else:
            self.create_black_horse()

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
        """
        Autor: Carlos Almario
        Fecha: junio 02 2018

        Metodo encargado de pintar la pantalla de inicio del juego
        :return:
        """
        self.window.fill(self.background_two_window)
        self.button.draw(self.window)

    def draw_text_right(self):
        """
        Autor: Carlos Almario
        Fecha: Junio 02 2018

        Metodo que pinta el texto de la derecha de l pantalla de juego dode se encuentran los puntajes
        :return:
        """
        score_human = self.create_text("PUNTAJE USUARIO:  " + str(self.human_items), 0, 0, 0)
        score_machine = self.create_text("PUNTAJE MAQUINA:  " + str(self.machine_items), 0, 0, 0)
        text_items_in_board = self.create_text("TOTAL MONEDAS EN JUEGO: "+str(self.items), 0, 0, 0)
        text = self.font.render(self.text_thinking, 0, (0, 0, 0))

        self.window.blit(text, ((len(self.board) * 78) + 14, HIGH - 40))
        self.window.blit(text_items_in_board, ((len(self.board) * 80) + 14, 50))
        self.window.blit(score_human, ((len(self.board) * 78) + 14, 90))
        self.window.blit(score_machine, ((len(self.board) * 78) + 14, 130))

    def game_over(self):
        """
        Autor: Carlos Almario
        Fecha: Junio 02 2018
        Metodo que pinta la panatalla de juego de terminado
        :return:
        """
        self.window.fill(self.background_two_window)
        winner = ""
        if self.items == 0 and self.human_items > self.machine_items:
            winner = "GANASTE"
        elif self.items == 0 and self.human_items < self.machine_items:
            winner = "PERDISTE BUENA SUERTE EN LA PROXIMA"
        game_over = self.create_text("EL JUEGO TERMINÓ "+ winner, 0, 0, 0)

        self.window.blit(game_over, (140, (HIGH/2)-100))

    def create_text(self, text, r, g, b):
        """
            Autor: Carlos Almario
            Fecha: junio 02 2018
            Método para crear el texto que va se va a mostrar en la pantalla del proyecto
            :return:
        """

        return self.font.render(text, 0, (r, g, b))

    def execute_minimax(self, node, items, items_machine, items_human):
        """
        Autor:
        Fecha:

        Metodo que ejecuta el algoritmo minimax mediante un hilo de ejecución
        :param node: estado inicial del juego
        :param items: numro de items en juego
        :param items_machine: items que posee la maquina en el momento
        :param items_human: items que posee el usuario en el momento
        :return:
        """
        if self.items == 0:
            self.game_over_ = True
        node_max = node
        self.text_thinking = "REALIZANDO CALCULOS..."
        best_action, turn = node_max.minimax(node_max, self.board, items, items_machine, items_human)
        self.player = turn
        # condicion que evalua si la acción retornada no es None o vacia
        if best_action is not None:
            # condición si en esa posicion de la mejor acción hay una moneda y capturarla y se descuentan los items en juego
            if self.board[best_action.position_x][best_action.position_y] == 'C':
                self.machine_items += 1
                self.items -= 1
            self.board[node.position_x][node.position_y] = '0'
            self.board[best_action.position_x][best_action.position_y] = 'W'
            self.text_thinking = ""

        else:
            print("algo salio mal y no encontro la mejor opción de juego")
            self.text_thinking = ""


main_window = Main()

