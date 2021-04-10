from scripts.position.positioning_operation import PositioningOperation, PositionAndSize, SelectPositioning
from pygame import Surface
from pygame import draw as draw_pg


class Empty(PositioningOperation):
    def __init__(self, parent: PositionAndSize, selected_positioning: SelectPositioning, height: int, width: int,
                 shift_x: int = 0, shift_y: int = 0,
                 surface: Surface = None, color: tuple = (0, 0, 0), outline: int = 0):
        super().__init__(parent, selected_positioning, height, width, shift_x, shift_y)
        self.__surface = surface
        self.__color = color
        self.__outline = outline
        self.__draw = False
        if self.__surface is not None:
            self.__draw = True

    def draw(self):
        super(Empty, self).draw()
        if self.__draw:
            draw_pg.rect(self.__surface, self.__color, (self.x, self.y, self.width, self.height), self.__outline)


