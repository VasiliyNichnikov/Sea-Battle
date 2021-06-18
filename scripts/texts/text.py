import os
from pygame import Surface
from pygame import Vector2
from pygame.font import Font
from typing import List

from scripts.main_objects.drawObject import DrawObject
from scripts.colors import BLACK
from scripts.main.mainParameters import DEFAULT_PATH_FONT
from scripts.main_objects.transform import Transform


class Text:
    """ Класс Text отвечает за отрисовку текста на экране """

    def __init__(self, surface: Surface) -> None:
        super().__init__()

        self.text = ''
        self.anti_aliasing = True
        self.color = BLACK
        self.size_font = 8

        self.__surface = surface
        self.__path_font = DEFAULT_PATH_FONT

        self.__font: Font = Font()
        self.__object = None

        self.get_size_update_text()

    @property
    def path_font(self) -> str:
        return self.__path_font

    @path_font.setter
    def path_font(self, value) -> None:
        if os.path.exists(value):
            self.__path_font = value

    def get_size_update_text(self) -> tuple:
        self.__font = Font(self.__path_font, self.size_font)
        self.__object = self.__font.render(self.text, self.anti_aliasing, self.color)
        return self.__object.get_width(), self.__object.get_height()

    def draw(self, position: Vector2):
        self.__surface.blit(self.__object, (position.x, position.y))
