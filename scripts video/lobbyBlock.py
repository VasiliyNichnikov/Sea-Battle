from colorsAndMainParameters import screen_height, screen_width, path_background_menu, FPS, size_field_top, \
    block_lobby, distance_between_block_lobby, path_font
from colorsAndMainParameters import WHITE, COLOR_TOP_BLOCK, GREEN, RED, YANDEX_COLOR
from textAndButton import Text
import pygame


class BlockLobby:
    def __init__(self, surface, name, lock=False):
        # Название блока
        self.__name = name
        # Позиция блока
        # self.__size = size
        # Является или нет блок заблокированным
        self.__lock = lock
        # Поле на котором будет происходить отрисовка
        self.__surface = surface
        # Текст пароля
        self.password_text = 'a'
        # Цвет блока
        self.color_block = WHITE
        # Цвет круга
        self.color_circle_lock = GREEN

        self.__name_text_obj = Text(self.__surface, name, 30, COLOR_TOP_BLOCK, anti_aliasing=True, path_font=path_font)

        if self.__lock:
            self.color_circle_lock = RED
            # Title пароля
            self.__password_title_obj = Text(self.__surface, 'Пароль:', 30, COLOR_TOP_BLOCK, anti_aliasing=True,
                                             path_font=path_font)

            # Текст пароля
            self.__password_text_obj = Text(self.__surface, self.password_text, 30, COLOR_TOP_BLOCK,
                                            anti_aliasing=True,
                                            path_font=path_font)

    # Отрисовка блока
    def draw_block(self, y, select_block=False):
        if select_block:
            self.color_block = YANDEX_COLOR
        else:
            self.color_block = WHITE

        pygame.draw.rect(self.__surface, self.color_block,
                         (distance_between_block_lobby, y,
                          screen_width - distance_between_block_lobby * 2, block_lobby))
        self.__name_text_obj.draw_text(
            position=(distance_between_block_lobby * 2, y + self.__name_text_obj.text_obj.get_height() // 2))

        pygame.draw.circle(self.__surface, self.color_circle_lock,
                           (screen_width - distance_between_block_lobby * 5, y + block_lobby // 2),
                           block_lobby // 4)

        if self.__lock:
            self.__password_text_obj.change_text(self.password_text)
            self.__password_title_obj.draw_text(
                position=(screen_width // 2 - self.__password_title_obj.text_obj.get_width() // 2,
                          y + self.__password_title_obj.text_obj.get_height() // 2))

            pygame.draw.rect(self.__surface, GREEN,
                             (screen_width // 2 + self.__password_title_obj.text_obj.get_width() // 2 + 10,
                              y + self.__password_title_obj.text_obj.get_height() // 2,
                              self.__password_text_obj.text_obj.get_width() + 10,
                              self.__password_title_obj.text_obj.get_height()), 0,
                             30)

            self.__password_text_obj.draw_text(
                position=(screen_width // 2 + self.__password_title_obj.text_obj.get_width() // 2 + 15,
                          y + self.__password_title_obj.text_obj.get_height() // 2))
