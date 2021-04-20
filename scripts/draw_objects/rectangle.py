# from scripts.position.positioning_operation import PositioningOperation, PositionAndSize, SelectPositioning
from pygame import Surface, Vector2
from pygame import Rect
from typing import List
from scripts.colors import BLACK
from scripts.main_objects.draw_object import DrawObject
from scripts.main_objects.transform import Transform
from pygame import draw as draw_pg


class Rectangle(DrawObject):
    def __init__(self, surface: Surface):
        super().__init__()

        self.color = BLACK
        self.outline = 0
        self.transform = Transform()

        self.__surface = surface
        self.__rect: Rect = Rect(0, 0, 0, 0)
        self.__update_rect()

    def __update_rect(self):
        self.__rect = Rect(self.transform.position.x, self.transform.position.y,
                           self.transform.size.x, self.transform.size.y)

    def draw(self):
        self.__update_rect()
        draw_pg.rect(self.__surface, self.color, self.__rect, self.outline)



