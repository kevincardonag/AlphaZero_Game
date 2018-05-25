import pygame


class Image(pygame.sprite.Sprite):

    """
    Autor: carlos Almario
    Fecha: mayo 20 2018
    Clase Image

    clase que se usará para pintar las imagenes del juego
    """

    def __init__(self, pos_i, pos_j, image):
        """
        Autor: Carlos Almario
        Fecha: mayo 20 2018
        Se sobrescribe el init para crear las variables de la clase Image.
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.left = pos_i
        self.rect.top = pos_j

    def draw(self, window):
        """
        Autor: Carlos Almario
        Fecha: mayo 20 2018
        Metodo para dibujar la imagen en el la pantalla
        :param window: panatalla que recibe y donde se va a dibujar
        :return:
        """
        window.blit(self.image, self.rect)


class Cursor(pygame.Rect):
    """
    Autor: carlos Almario
    Fecha: mayo 20 2018
    Clase Image

    clase que se usará para pintar un rectangulo invicible para capturar las posiciones cuando se de click
    en el tablero
    """

    def __init__(self):
        """
        Autor: Carlos Almario
        Fecha: mayo 20 2018
        Se sobrescribe el init para crear las variables de la clase Cursor.
        """
        pygame.Rect.__init__(self,0,0,1,1)

    def update(self):
        """
        Autor: Carlos Almario
        Fecha: mayo 20 2018
        Metodo para dibujar el rectangulo invisible para capturar la colision
        :return:
        """
        self.left, self.top = pygame.mouse.get_pos()

