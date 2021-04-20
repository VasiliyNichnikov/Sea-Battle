from scripts.position.positioning_operation import PositioningOperation, PositionAndSize, SelectPositioning
from pygame import Surface, Rect
from scripts.colors import BLACK
from scripts.main_objects.transform import Transform
from scripts.main_objects.draw_object import DrawObject
from pygame import draw as draw_pg


class Empty(DrawObject):
    def __init__(self, surface: Surface = None):
        self.__surface = surface
        self.color = BLACK
        self.outline = 0

        self.transform = Transform()
        self.__draw = False
        self.__rect = Rect(0, 0, 0, 0)
        if self.__surface is not None:
            self.__draw = True

    def __update_rect(self) -> None:
        self.__rect = self.transform.position.x, self.transform.position.y, self.transform.size.x, self.transform.size.y

    def draw(self) -> None:
        if self.__draw:
            self.__update_rect()
            draw_pg.rect(self.__surface, self.color, self.__rect, self.outline)

