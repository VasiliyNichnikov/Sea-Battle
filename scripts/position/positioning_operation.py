# Анимацию
from scripts.animation import follow
from scripts.position.positioning import Positioning, PositionAndSize, SelectPositioning


class PositioningOperation(Positioning, PositionAndSize):
    def __init__(self, parent: PositionAndSize, selected_positioning: SelectPositioning,
                 height: int, width: int, shift_x: int = 0, shift_y: int = 0):
        super().__init__(parent, self, selected_positioning)
        self.__width = width
        self.__height = height
        self.__parent = parent
        self.__x = 0
        self.__y = 0
        self.__shift_x = shift_x
        self.__shift_y = shift_y
        self.__change_x_and_y()

    def __change_x_and_y(self, shift_x: int = 0, shift_y: int = 0):
        self.__shift_x += shift_x
        self.__shift_y += shift_y

        # self.__shift_x, self.__shift_y = follow((self.__shift_x, self.__shift_y), (self.__shift_x + shift_x, self.__shift_y + shift_y))

        if self.__parent is not None:
            self.__x, self.__y = self._calculations(self.__shift_x, self.__shift_y)

    def move(self, shift_x: int = 0, shift_y: int = 0):
        self.__change_x_and_y(shift_x, shift_y)

    def draw(self):
        self.__change_x_and_y()

    @property
    def height(self):
        return self.__height

    @property
    def width(self):
        return self.__width

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y
