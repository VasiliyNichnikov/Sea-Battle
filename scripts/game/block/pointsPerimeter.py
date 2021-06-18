from pygame import Vector2


class PointsPerimeter:
    def __init__(self, pos: Vector2, block_size: int):
        self.__pos_left_up = Vector2(pos.x, pos.y + block_size)
        self.__pos_right_up = Vector2(pos.x + block_size, pos.y + block_size)
        self.__pos_left_down = Vector2(pos.x, pos.y)
        self.__pos_right_down = Vector2(pos.x + block_size, pos.y)

    @property
    def pos_left_up(self) -> Vector2:
        return self.__pos_left_up

    @property
    def pos_right_up(self) -> Vector2:
        return self.__pos_right_up

    @property
    def pos_left_down(self) -> Vector2:
        return self.__pos_left_down

    @property
    def pos_right_down(self) -> Vector2:
        return self.__pos_right_down
