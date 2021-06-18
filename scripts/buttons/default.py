from pygame import Surface
from scripts.draw_objects.rectangle import Rectangle
from scripts.texts.text import Text
from scripts.position.positioningOperation import PositionAndSize, SelectPositioning


class ButtonDefault:
    def __init__(self, surface: Surface, parent: PositionAndSize, selected_positioning: SelectPositioning,
                 text: str, size_font: int, color_text: tuple, path_font: str, height: int = 0, width: int = 0,
                 shift_x: int = 0, shift_y: int = 0,
                 color_default: tuple = (0, 0, 0), color_pressed: tuple = (255, 255, 255)) -> None:
        self.__color_default = color_default
        self.__color_pressed = color_pressed

        self.__text = Text(surface, text, size_font, color_text, path_font, parent,
                           selected_positioning, shift_x, shift_y, anti_aliasing=True)

        self.__background = Rectangle(surface, self.__text, SelectPositioning.center,
                                      self.__text.height, self.__text.width, color=color_default)

    def check_input_button(self, mouse, is_click=False):
        if self.__background.rect.topleft[0] < mouse[0] < self.__background.rect.bottomright[0] \
                and self.__background.rect.topleft[1] < mouse[1] < \
                self.__background.rect.bottomright[1] and is_click:
            self.__background.change_color(self.__color_pressed)
        else:
            self.__background.change_color(self.__color_default)

    def draw(self):
        self.__background.draw()
        self.__text.draw()
