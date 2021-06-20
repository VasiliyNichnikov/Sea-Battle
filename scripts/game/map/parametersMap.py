from typing import List, Type
from pygame import Surface, Vector2, Rect
from scripts.colorsAndMainParameters import number_blocks, block_size


class ParametersMap:
    def __init__(self, surface: Surface, name: str, border: Vector2):
        self.__surface = surface
        self.__name = name
        self.__border = border
        self.__blocks = [[object] * 10] * 10
        self.__rect = Rect(self.__border.x,
                           self.__border.y,
                           block_size * number_blocks,
                           block_size * number_blocks)

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
