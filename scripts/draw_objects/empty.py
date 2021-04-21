from scripts.position.positioningOperation import PositioningOperation, PositionAndSize, SelectPositioning
from pygame import Surface, Rect
from scripts.colors import BLACK
from scripts.draw_objects.rectangle import Rectangle
from scripts.main_objects.transform import Transform
from scripts.main_objects.drawObject import DrawObject
from pygame import draw as draw_pg


class Empty:
    def __init__(self, surface: Surface = None):
        self.__surface = surface

        self.transform = Transform()
        self.rectangle = Rectangle()
        self.rectangle.color = BLACK

        self.__draw = False
        if self.__surface is not None:
            self.__draw = True

    def draw(self) -> None:
        if self.__draw:
            # self.transform.change_position_children()
            # x, y = self.transform.position
            x, y = self.transform.position
            # if local:
            #     x, y = self.transform.get_global_position()

            draw_pg.rect(self.__surface, self.rectangle.color, (x, y, self.transform.size.x, self.transform.size.y),
                         self.rectangle.outline)
