from pygame import draw as draw_pg
from pygame import Surface, Vector2
from scripts.colors import COLOR_GRAY_BLOCK
from scripts.lobby.lobbyParameters import WIDTH_BLOCK, HEIGHT_BLOCK
from scripts.draw_objects.rectangle import Rectangle
from scripts.main_objects.transform import Transform


class BackgroundBlock:
    def __init__(self, surface: Surface):
        self.transform = Transform()
        self.transform.size = Vector2(WIDTH_BLOCK, HEIGHT_BLOCK)

        self.__surface = surface
        self.__rectangle = Rectangle()
        self.__rectangle.color = COLOR_GRAY_BLOCK

    def draw(self) -> None:
        # self.transform.change_position_children()
        x, y = self.transform.position
        # if local:
        #     x, y = self.transform.get_global_position()

        draw_pg.rect(self.__surface, self.__rectangle.color, (x, y, self.transform.size.x, self.transform.size.y),
                     self.__rectangle.outline)
