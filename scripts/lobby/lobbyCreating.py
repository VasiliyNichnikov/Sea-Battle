import pygame
from scripts.colorsAndMainParameters import path_font
# from scripts.textAndButtonAndInputPanel import Text, InputPanel


class CreatingLobby:
    DISTANCE_BETWEEN_PARAMETERS = 10
    WIDTH_INPUT_PANEL = 120

    def __init__(self, surface, height, width):
        self.__surface = surface
        self.__height = height
        self.__width = width
        self.draw_block = False

        # self.name_block = Text(self.__surface, 'СОЗДАТЬ ЛОББИ', 40, (255, 255, 255), anti_aliasing=True,
        #                        path_font=path_font)
        #
        # self.name_lobby = Text(self.__surface, 'Название лобби', 30, (255, 100, 255), anti_aliasing=True,
        #                        path_font=path_font)
        # self.set_name_lobby = InputPanel(self.__surface, self.WIDTH_INPUT_PANEL, self.name_lobby.height,
        #                                  path_font)
        #
        # self.password_lobby = Text(self.__surface, 'Пароль Лобби', 30, (100, 255, 255), anti_aliasing=True,
        #                            path_font=path_font)
        # self.set_password_lobby = InputPanel(self.__surface, self.WIDTH_INPUT_PANEL,
        #                                      self.password_lobby.height, path_font=path_font)

        self.__select_panel = None
        self.__input_panels = [self.set_name_lobby, self.set_password_lobby]

    @property
    def height(self):
        return self.__height

    @property
    def width(self):
        return self.__width

    def input_block(self, event):
        for panel in self.__input_panels:
            if panel.check_input_button(event.pos):
                self.__select_panel = panel
                break
            else:
                self.__select_panel = None

    def entering_values(self, event):
        if self.__select_panel is not None:
            self.__select_panel.add_symbol_text(event)

    def draw(self, x, y):
        pygame.draw.rect(self.__surface, (100, 100, 100), (x, y, self.__height, self.__width))
        self.name_block.draw_text(position=(x + self.name_block.width // 2, y))

        self.name_lobby.draw_text(position=(x, y + self.name_block.y + self.DISTANCE_BETWEEN_PARAMETERS))
        self.set_name_lobby.draw(self.name_lobby.width + self.name_lobby.x + self.DISTANCE_BETWEEN_PARAMETERS,
                                 y + self.name_block.y + self.DISTANCE_BETWEEN_PARAMETERS)

        self.password_lobby.draw_text(position=(x, y + self.name_lobby.y + self.DISTANCE_BETWEEN_PARAMETERS))
        self.set_password_lobby.draw(self.name_lobby.width + self.name_lobby.x + self.DISTANCE_BETWEEN_PARAMETERS,
                                     y + self.name_lobby.y + self.DISTANCE_BETWEEN_PARAMETERS)
