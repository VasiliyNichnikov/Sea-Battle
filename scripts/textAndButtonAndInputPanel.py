import pygame
from pygame import display
from pygame.font import Font
# from allConditions import ConditionButton


# class SelectText(Text):
#     def __init__(self, surface, text, size_font, color_default, color_select, condition_button, select_text_obj=False,
#                  anti_aliasing=False, path_font='None'):
#         super().__init__(surface, text, size_font, color_default, anti_aliasing=anti_aliasing, path_font=path_font)
#         self.select_text_obj = select_text_obj
#         self.select_color = color_select
#         self.default_color = color_default
#         self.__condition_button = condition_button
#
#     def draw_text(self, position=(0, 0)) -> None:
#         if self.select_text_obj:
#             selected_color = self.select_color
#         else:
#             selected_color = self.default_color
#         self.text_obj = self.__font.render(self.__text, self.__anti_aliasing, selected_color)
#         super().draw_text(position)
#
#     def get_condition_button(self):
#         return self.__condition_button


class Button(object):
    def __init__(self, surface, border_height, border_width, color_bg=(0, 0, 0), text='None',
                 color_text=(255, 255, 255), path_font='None', size_font=30):
        self.__surface = surface

        self.__border_width = border_width
        self.__border_height = border_height

        self.__color_btn = color_bg
        self.__text = text
        self.__color_text = color_text
        self.__path_font = path_font
        self.__size_font = size_font
        self.__input_btn = False

        self.text = Text(self.__surface,
                         self.__text,
                         self.__size_font,
                         self.__color_text,
                         anti_aliasing=True,
                         path_font=self.__path_font)

        self.__width = self.text.width + self.__border_width
        self.__height = self.text.height + self.__border_height
        self.__rect = pygame.Rect(0, 0, 0, 0)

    def draw_button(self, x, y):
        self.__rect.x, self.__rect.y, self.__rect.width, self.__rect.height = x, y, self.__width, self.__height
        if self.__input_btn:
            pygame.draw.rect(self.__surface, self.__color_btn, (x, y, self.__width, self.__height))
        else:
            pygame.draw.rect(self.__surface, self.__color_btn, (x, y, self.__width, self.__height), 0)
        self.text.draw_text(position=(x + self.__border_width // 2, y + self.__border_height // 2))

    @property
    def height(self):
        return self.__height

    @property
    def width(self):
        return self.__width

    def check_input_button(self, mouse, click=False):
        if self.__rect.topleft[0] < mouse[0] < self.__rect.bottomright[0] and self.__rect.topleft[1] < mouse[1] < \
                self.__rect.bottomright[1] and click:
            self.__input_btn = True
        else:
            self.__input_btn = False
        return self.__input_btn


class InputPanel(object):
    def __init__(self, surface, width, height, path_font, max_symbols=10, color_bg=(0, 0, 0),
                 color_text=(255, 255, 255)):
        self.__surface = surface
        self.__width = width
        self.__height = height
        self.__color_bg = color_bg
        self.__color_text = color_text
        self.__max_symbols = max_symbols
        self.__rect = pygame.Rect(0, 0, 0, 0)

        self.__text_input_panel = ''
        self.__text_obj = Text(self.__surface, self.__text_input_panel, 30, color_text,
                               anti_aliasing=True, path_font=path_font)

    def draw(self, x, y):
        self.__rect.x, self.__rect.y, self.__rect.width, self.__rect.height = x, y, self.__width, self.__height
        pygame.draw.rect(self.__surface, self.__color_bg, (x, y, self.__width, self.__height))
        self.__text_obj.render_text(self.__text_input_panel)
        self.__text_obj.draw_text(
            position=(x + 5, y))

    def add_symbol_text(self, event):
        if event.key == pygame.K_RETURN:
            print(self.__text_input_panel)
        elif event.key == pygame.K_BACKSPACE:
            self.__text_input_panel = self.__text_input_panel[:-1]
        elif len(self.__text_input_panel) + 1 <= self.__max_symbols:
            self.__text_input_panel += event.unicode

    def check_input_button(self, mouse):
        input_btn = False
        if self.__rect.topleft[0] < mouse[0] < self.__rect.bottomright[0] and self.__rect.topleft[1] < mouse[1] < \
                self.__rect.bottomright[1]:
            input_btn = True
        return input_btn
