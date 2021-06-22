from typing import List, Type
from pygame import Surface, Vector2, Rect
from scripts.game.map.condition import EnumMap


class ParametersMap:
    def __init__(self, name: str, surface: Surface, condition: EnumMap, size: Vector2, border: Vector2):
        self.__name = name
        self.__surface = surface
        self.__border = border
        self.__condition = condition
        self.__blocks = [[object] * 10] * 10
        self.__size = size
        self.__rect = Rect(self.__border.x, self.__border.y, size.x, size.y)

    @property
    def surface(self) -> Surface:
        return self.__surface

    @property
    def name(self) -> str:
        return self.__name

    @property
    def border(self) -> Vector2:
        return self.__border

    @property
    def blocks(self) -> List[List[Type[object]]]:
        return self.__blocks

    @property
    def rect(self) -> Rect:
        return self.__rect

    @property
    def size(self) -> Vector2:
        return self.__size

    @property
    def condition(self) -> EnumMap:
        return self.__condition
