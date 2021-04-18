from pygame import Surface
from pygame.font import Font
from scripts.position.positioning_operation import PositioningOperation, PositionAndSize, SelectPositioning


class Text(PositioningOperation):
    """ Класс Text отвечает за отрисовку текста на экране """

    def __init__(self, surface: Surface, text: str, size_font: int, color: tuple, path_font: str,
                 parent: PositionAndSize, selected_positioning: SelectPositioning, shift_x: int = 0, shift_y: int = 0,
                 anti_aliasing: bool = False) -> None:
        self.__surface = surface
        self.__font = Font(path_font, size_font)
        self.__text = text
        self.__anti_aliasing = anti_aliasing
        self.__color = color
        self.render_text(self.__text)
        super().__init__(parent, selected_positioning, self.__height, self.__width, shift_x, shift_y)

    def render_text(self, new_text) -> None:
        self.__object = self.__font.render(new_text, self.__anti_aliasing, self.__color)
        self.__width = self.__object.get_width()
        self.__height = self.__object.get_height()

    def draw(self) -> None:
        super(Text, self).draw()
        self.__surface.blit(self.__object, (self.x, self.y))
