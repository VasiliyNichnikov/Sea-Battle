import pygame


class Text:
    """ Класс Text отвечает за отрисовку текста на экране """

    def __init__(self, surface, text, size_font, color, anti_aliasing=False, path_font='None'):
        self.surface = surface
        self.font = pygame.font.Font(path_font, size_font)
        self.text = self.font.render(text, anti_aliasing, color)

    # Отрисовка текста на экране
    def draw_text(self, position=(0, 0)) -> None:
        self.surface.blit(self.text, position)


class Button:
    """ Класс Button отвечает за отрисовку кнопки на экране """
    pass
