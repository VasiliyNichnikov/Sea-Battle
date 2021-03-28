import pygame
from allConditions import ConditionButton


class Text(object):
    """ Класс Text отвечает за отрисовку текста на экране """

    def __init__(self, surface, text, size_font, color, anti_aliasing=False, path_font='None'):
        self.surface = surface
        self.font = pygame.font.Font(path_font, size_font)
        self.text = text
        self.anti_aliasing = anti_aliasing
        self.text_obj = self.font.render(self.text, self.anti_aliasing, color)

    # Отрисовка текста на экране
    def draw_text(self, position=(0, 0)) -> None:
        self.surface.blit(self.text_obj, position)


class SelectText(Text):
    def __init__(self, surface, text, size_font, color_default, color_select, condition_button, select_text_obj=False,
                 anti_aliasing=False, path_font='None'):
        super().__init__(surface, text, size_font, color_default, anti_aliasing=anti_aliasing, path_font=path_font)
        self.select_text_obj = select_text_obj
        self.select_color = color_select
        self.default_color = color_default
        self.__condition_button = condition_button

    def draw_text(self, position=(0, 0)) -> None:
        if self.select_text_obj:
            selected_color = self.select_color
        else:
            selected_color = self.default_color
        self.text_obj = self.font.render(self.text, self.anti_aliasing, selected_color)
        super().draw_text(position)

    def get_condition_button(self):
        return self.__condition_button


class Button(object):
    """ Класс Button отвечает за отрисовку кнопки на экране """
    pass
