import pygame
from pygame import Surface
from scripts.position.positioning_operation import PositionAndSize, SelectPositioning
from scripts.texts.text import Text
# Прямоугольник
from scripts.draw_objects.rectangle import Rectangle
# Изображения
from scripts.images.image import Image
# Дополнительные параметры
from scripts.lobby.lobbyParameters import BACKGROUND_BLOCK_LINE, BACKGROUND_NAME, HEIGHT_LINE, \
    DISTANCE_BETWEEN_BLOCK_AND_TEXT
from scripts.main.mainParameters import DEFAULT_PATH_FONT
from scripts.colorsParameters import WHITE, COLOR_GRAY_BLOCK, COLOR_BLOCK

"""
    Создание блока лобби 
"""


class LobbyBlock:
    def __init__(self, surface: Surface, name: str, index: int, parent: PositionAndSize,
                 selected_positioning: SelectPositioning,
                 height: int, width: int, shift_x: int = 0, shift_y: int = 0, lock: bool = False) -> None:
        self.__surface = surface
        self.__parent = parent
        self.__selected_positioning = selected_positioning
        self.__lock = lock
        self.__index_block = index

        # Текст пароля
        self.__text_password = ''

        # self.__name_lobby = Text(self.__surface, name, 30, COLOR_GRAY_BLOCK, anti_aliasing=True, path_font=path_font)
        # Создание текста пароль
        # self.__title_password = Text(self.__surface, 'Пароль:', 30, WHITE, anti_aliasing=True, path_font=path_font)

        # Создание текста, пароль, который ввел пользователь
        # self.__password = Text(self.__surface, self.__text_password, 30, WHITE, anti_aliasing=True, path_font=path_font)
        self.__password = Text(surface=self.__surface, text=self.__text_password, size_font=30, color=COLOR_GRAY_BLOCK,
                               path_font=DEFAULT_PATH_FONT,
                               parent=self.__parent, selected_positioning=SelectPositioning.left, anti_aliasing=True)

        # Блок изображения (Блок не выбран)
        # self.__block_image_not_selected = load_image(path_block_lobby_not_selected, width=self.width,
        #                                              height=self.height,
        #                                              proportionately=False)

        # Image(self.__surface, BACKGROUND_BLOCK, self.__parent,
        #       self.__selected_positioning, height, width, shift_x, shift_y)

        self.__background = Rectangle(self.__surface, self.__parent, self.__selected_positioning,
                                      height, width, shift_x, shift_y, color=COLOR_BLOCK)

        # Имя лобби
        self.__name = Text(surface=self.__surface, text=name, size_font=30, color=WHITE, path_font=DEFAULT_PATH_FONT,
                           parent=self.__background, selected_positioning=SelectPositioning.left, anti_aliasing=True,
                           shift_x=DISTANCE_BETWEEN_BLOCK_AND_TEXT, shift_y=-HEIGHT_LINE // 2)

        # Задний фон текста
        self.__background_name = Image(surface=self.__surface,
                                       parent=self.__name,
                                       selected_positioning=SelectPositioning.center,
                                       height=self.__name.height,
                                       width=self.__name.width, path=BACKGROUND_NAME)

        self.__line = Image(self.__surface, BACKGROUND_BLOCK_LINE, self.__background, SelectPositioning.down,
                            height=HEIGHT_LINE, width=self.__background.width)
        # load_image(path_block_lobby_not_selected, width=self.width, height=10,
        #                                        proportionately=False)
        #
        # Задний фон текстов
        # self.__background_image_text = load_image(path_text_selection, size_x=self.__name_lobby.__object.get_width(),
        #                                           size_y=self.__name_lobby.__object.get_height(), select_size=False)

        # Цвет круга (По умолчанию зеленый)
        self.__color_circle = (114, 166, 124)
        if self.__lock:
            self.__color_circle = (166, 114, 124)

    # Получение id блока
    def get_index(self) -> int:
        return self.__index_block

    @property
    def text_password(self) -> str:
        return self.__text_password

    @text_password.setter
    def text_password(self, value) -> None:
        if len(value) <= 4:
            self.__text_password = value

    @property
    def lock(self):
        return self.__lock

    @property
    def x(self):
        return self.__background.x

    @property
    def y(self):
        return self.__background.y

    # Отрисовка блока
    def draw(self) -> None:
        self.__background.draw()
        self.__line.draw()
        self.__background_name.draw()
        self.__name.draw()
        # self.__surface.blit(self.__block_image_not_selected, (distance_between_block_lobby, y))
        #
        # # self.__surface.blit(self.__background_image_text,
        # #                     (distance_between_block_lobby * 2, y + self.__name_lobby.height // 2))
        #
        # self.__name_lobby.draw_text(position=(distance_between_block_lobby * 2,
        #                                       y + self.__name_lobby.height // 2))
        #
        # pygame.draw.circle(self.__surface, self.__color_circle,
        #                    (screen_width - distance_between_block_lobby * 7, y + block_lobby_height // 2),
        #                    block_lobby_height // 4)
        #
        # if select_block:
        #     self.__surface.blit(self.__line_image, (distance_between_block_lobby, y +
        #                                             self.__block_image_not_selected.get_height()))
        #
        #     if self.__lock:
        #         self.__title_password.draw_text(
        #             position=(screen_width // 2,
        #                       y + self.__title_password.height // 2))
        #         # self.__surface.blit(self.__background_image_text,
        #         #                     (screen_width // 2 +
        #         #                      self.__title_password.width + 10,
        #         #                      y + self.__name_lobby.height // 2))
        #
        #         self.__password.render_text(self.__text_password)
        #         # self.__password.draw_text(
        #         #     position=(screen_width // 2 +
        #         #               self.__title_password.width + 10 +
        #         #               self.__background_image_text.get_width() // 2 - self.__password.width // 2,
        #         #               y + self.__title_password.height // 2))
