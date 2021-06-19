from pygame import Vector2, Surface
from scripts.game2.block.conditionBlock import ConditionBlock
from scripts.game2.block.positionBlock import PositionBlock


class ParametersBlock:
    def __init__(self, surface: Surface, number_block: Vector2, border: Vector2, block_size: int):
        self.__surface = surface
        self.__block_size = block_size
        self.__number_block = number_block
        self.__position_block = PositionBlock(number_block, border, block_size)
        self.__condition_block = ConditionBlock()

    @property
    def surface(self):
        return self.__surface

    @property
    def block_size(self):
        return self.__block_size

    @property
    def number_block(self):
        return self.__number_block

    @property
    def position_block(self):
        return self.__position_block

    @property
    def condition_block(self):
        return self.__condition_block
