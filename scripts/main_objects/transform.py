from typing import List
from pygame import Vector2


class Transform:
    def __init__(self) -> None:
        # self.__local_position = Vector2(0, 0)
        self.__position = Vector2(0, 0)
        self.__size = Vector2(0, 0)
        self.__parent: Transform = None
        # self.__children: List[Transform] = []

    # @property
    # def local_position(self) -> Vector2:
    #     return self.__local_position
    #
    # @local_position.setter
    # def local_position(self, value: Vector2) -> None:
    #     self.__local_position = value

    # def add_child(self, new_child):
    #     if type(new_child) is Transform:
    #         self.__children.append(new_child)

    def set_parent(self, parent):
        if type(parent) is Transform:
            self.__parent = parent
            # self.__position += self.__parent.position

    # def change_position_children(self):
    #     if len(self.__children) != 0:
    #         for child in self.__children:
    #             child.position = self.position + child.position
    #             print(child.position)

    # def get_global_position(self) -> Vector2:
    #     if self.__parent is not None and type(self.__parent) is Transform:
    #         return self.__parent.position + self.__position

    # def local_position(self) -> Vector2:
    #     return self.__position

    @property
    def position(self) -> Vector2:
        if self.__parent is not None:
            return self.__position + self.__parent.position
        return self.__position

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

    def lerp(self, a: Vector2, step: float):
        self.__position = a + step * (self.__position - a)
