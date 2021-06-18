from pygame import Rect, Vector2
from scripts.game.block.pointsPerimeter import PointsPerimeter


class PositionBlock:
    def __init__(self, number_block: Vector2, border: Vector2, block_size: int):
        self.__init_position(number_block, border, block_size)
        self.__points_perimeter = PointsPerimeter(self.__pos, block_size)
        self.__rect = Rect(self.__pos.x, self.__pos.y, block_size, block_size)

    def __init_position(self, number_block: Vector2, border: Vector2, block_size: int):
        pos_x = number_block.x * block_size + border.x
        pos_y = number_block.y * block_size + border.y
        self.__pos = Vector2(pos_x, pos_y)

    @property
    def points_perimeter(self) -> PointsPerimeter:
        return self.__points_perimeter

    @property
    def rect(self) -> Rect:
        return self.__rect

    @property
    def position(self) -> Vector2:
        return self.__pos
