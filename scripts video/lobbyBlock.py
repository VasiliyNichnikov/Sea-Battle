import pygame
from textAndButtonAndInputPanel import Text
from imagesAndAnimations import load_image
from colorsAndMainParameters import screen_width, block_lobby, distance_between_block_lobby, \
    path_font, path_block_lobby_not_selected, path_text_selection, \
    path_block_lobby_pressed
from colorsAndMainParameters import WHITE, COLOR_GRAY_BLOCK

"""
    Создание лобби блока
"""


class LobbyBlock:
    def __init__(self, surface, name, index, lock=False) -> None:
        self.__surface = surface
        self.__lock = lock
        self.__index_block = index

        # Текст пароля
        self.__text_password = ''

        # Создание текста лобби
        self.__name_lobby = Text(self.__surface, name, 30, COLOR_GRAY_BLOCK, anti_aliasing=True, path_font=path_font)
        # Создание текста пароль
        self.__title_password = Text(self.__surface, 'Пароль:', 30, WHITE, anti_aliasing=True, path_font=path_font)

        # Создание текста, пароль, который ввел пользователь self.__text_password
        self.__password = Text(self.__surface, self.__text_password, 30, WHITE, anti_aliasing=True, path_font=path_font)

        # Блок изображения (Блок не выбран)
        self.__block_image_not_selected = load_image(path_block_lobby_not_selected, size_x=screen_width - 10,
                                                     size_y=block_lobby,
                                                     select_size=False)
        # Линия, которая отрисовывается, если блок выбран
        self.__line_image = load_image(path_block_lobby_pressed, size_x=screen_width - 10, size_y=10, select_size=False)

        # Задний фон текстов
        self.__background_image_text = load_image(path_text_selection, size_x=self.__name_lobby.text_obj.get_width(),
                                                  size_y=self.__name_lobby.text_obj.get_height(), select_size=False)

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

    # Отрисовка блока
    def draw_block(self, y, select_block) -> None:
        self.__surface.blit(self.__block_image_not_selected, (distance_between_block_lobby, y))

        self.__surface.blit(self.__background_image_text,
                            (distance_between_block_lobby * 2, y + self.__name_lobby.text_obj.get_height() // 2))

        self.__name_lobby.draw_text(position=(distance_between_block_lobby * 2,
                                              y + self.__name_lobby.text_obj.get_height() // 2))

        pygame.draw.circle(self.__surface, self.__color_circle,
                           (screen_width - distance_between_block_lobby * 7, y + block_lobby // 2),
                           block_lobby // 4)

        if select_block:
            self.__surface.blit(self.__line_image, (distance_between_block_lobby, y +
                                                    self.__block_image_not_selected.get_height()))

            if self.__lock:
                self.__title_password.draw_text(
                    position=(screen_width // 2,
                              y + self.__title_password.text_obj.get_height() // 2))
                self.__surface.blit(self.__background_image_text,
                                    (screen_width // 2 +
                                     self.__title_password.text_obj.get_width() + 10,
                                     y + self.__name_lobby.text_obj.get_height() // 2))

                self.__password.change_text(self.__text_password)
                self.__password.draw_text(
                    position=(screen_width // 2 +
                              self.__title_password.text_obj.get_width() + 10 +
                              self.__background_image_text.get_width() // 2 - self.__password.text_obj.get_width() // 2,
                              y + self.__title_password.text_obj.get_height() // 2))
