"""
    Данный класс используется для позиционирование объекта относительно родителя
"""
from pygame import Vector2
from scripts.animation import follow
from scripts.position.positionAndSize import PositionAndSize
from scripts.transfers.enumPosition import SelectPositioning


class Positioning:
    def __init__(self, parent: PositionAndSize, child: PositionAndSize, selected_positioning: SelectPositioning):
        self.__parent = parent
        self.__child = child
        self.__selectedPosition = selected_positioning

    # Lerp(a, b, t) = a + (b - a) * t

    def _calculations(self, shift_x: int = 0, shift_y: int = 0):
        try:
            x, y = self.__get_calculation()()
            return x + self.__parent.x + shift_x, y + self.__parent.y + shift_y
        except KeyError as e:
            raise ValueError('Undefined unit: {}'.format(e.args[0]))

    # def __lerp(self, a: tuple, b: tuple, t: float):
    #     start = Vector2(a)
    #     end = Vector2(b)
    #     return start + (end - start) * t

    def __get_calculation(self):
        return {
            SelectPositioning.center: self.__center,
            SelectPositioning.right: self.__right,
            SelectPositioning.left: self.__left,
            SelectPositioning.down: self.__down,
            SelectPositioning.up: self.__up,
            SelectPositioning.right_up: self.__right_up,
            SelectPositioning.right_down: self.__right_down,
            SelectPositioning.left_up: self.__left_up,
            SelectPositioning.left_down: self.__left_down
        }.get(self.__selectedPosition)

    def __center(self) -> (int, int):
        x = self.__parent.width // 2 - self.__child.width // 2
        y = self.__parent.height // 2 - self.__child.height // 2
        return x, y

    def __right(self) -> (int, int):
        x = self.__parent.width - self.__child.width
        y = self.__parent.height // 2 - self.__child.height // 2
        return x, y

    def __left(self) -> (int, int):
        x = 0
        y = self.__parent.height // 2 - self.__child.height // 2
        return x, y

    def __down(self):
        x = self.__parent.width // 2 - self.__child.width // 2
        y = self.__parent.height - self.__child.height
        return x, y

    def __up(self) -> (int, int):
        x = self.__parent.width // 2 - self.__child.width // 2
        y = 0
        return x, y

    def __right_up(self) -> (int, int):
        x = self.__right()[0]
        y = self.__up()[1]
        return x, y

    def __right_down(self) -> (int, int):
        x = self.__right()[0]
        y = self.__down()[1]
        return x, y

    def __left_up(self) -> (int, int):
        x = self.__left()[0]
        y = self.__up()[1]
        return x, y

    def __left_down(self) -> (int, int):
        x = self.__left()[0]
        y = self.__down()[1]
        return x, y
