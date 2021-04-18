from scripts.position.positioning_operation import PositioningOperation, PositionAndSize, SelectPositioning
from pygame import Surface
from pygame import Rect
from pygame import draw as draw_pg


class Rectangle(PositioningOperation):
    def __init__(self, surface: Surface, parent: PositionAndSize, selected_positioning: SelectPositioning, height: int, width: int,
                 shift_x: int = 0, shift_y: int = 0, color: tuple = (0, 0, 0), outline: int = 0):
        super().__init__(parent, selected_positioning, height, width, shift_x, shift_y)
        self.__surface = surface
        self.__color = color
        self.__outline = outline
        self.__rect = Rect(self.x, self.y, self.width, self.height)

    def change_color(self, color: tuple):
        self.__color = color

    @property
    def rect(self) -> Rect:
        return self.__rect

    def draw(self):
        super(Rectangle, self).draw()
        self.__rect.x, self.__rect.y, self.__rect.width, self.__rect.height = self.x, self.y, self.width, self.height
        draw_pg.rect(self.__surface, self.__color, self.__rect, self.__outline)



