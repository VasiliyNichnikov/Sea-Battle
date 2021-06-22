from pygame import Rect


class FieldBorderDrawParameters:
    def __init__(self, position: Rect, color: tuple):
        self.__position = position
        self.__color = color

    @property
    def position(self) -> Rect:
        return self.__position

    @property
    def color(self) -> tuple:
        return self.__color
