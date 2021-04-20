import typing

from pygame import Vector2
from scripts.main_objects.draw_object import DrawObject


class Transform:
    def __init__(self) -> None:
        self.__position = Vector2(0, 0)
        self.__local_position = Vector2(0, 0)
        self.__rotation = Vector2(0, 0)
        self.__size = Vector2(0, 0)

        self.__parent: Transform = None

    @property
    def parent(self):
        return self.__parent

    def change_parent(self, value):
        if type(value) == Transform:
            self.__parent = value
            self.__local_position = self.__parent.position

    @property
    def position(self) -> Vector2:
        return self.__position + self.__local_position

    @position.setter
    def position(self, value: Vector2) -> None:
        self.__position = value

    @property
    def size(self) -> Vector2:
        return self.__size

    @size.setter
    def size(self, value: Vector2) -> None:
        if value.x >= 0 and value.y >= 0:
            self.__size = value
