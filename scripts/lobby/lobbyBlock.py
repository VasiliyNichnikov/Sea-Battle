import pygame
from pygame import Surface, Vector2
from scripts.position.positioningOperation import PositionAndSize, SelectPositioning
from scripts.lobby.backgroundBlock import BackgroundBlock
from scripts.lobby.backgroundLine import BackgroundLine
from scripts.main_objects.transform import Transform
from scripts.texts.text import Text
# Прямоугольник
from scripts.draw_objects.rectangle import Rectangle
# Изображения
from scripts.images.image import Image
# Кнопки
from scripts.buttons.default import ButtonDefault
# Дополнительные параметры
from scripts.lobby.lobbyParameters import BACKGROUND_BLOCK_LINE, BACKGROUND_NAME, HEIGHT_LINE, \
    DISTANCE_BETWEEN_BLOCK_AND_TEXT, SIZE_FONT
from scripts.main.mainParameters import DEFAULT_PATH_FONT
from scripts.colors import WHITE, COLOR_GRAY_BLOCK, COLOR_BLOCK, COLOR_TEXT_LOBBY

"""
    Создание блока лобби 
"""


class LobbyBlock:
    def __init__(self, surface: Surface, name: str, index: int, parent: Transform,
                 selected_positioning: SelectPositioning,
                 height: int, width: int, shift_x: int = 0, shift_y: int = 0, lock: bool = False) -> None:
        self.__surface = surface
        self.__parent = parent
        self.__selected_positioning = selected_positioning
        self.__lock = lock
        self.__index_block = index

        self.__text_password = ''

        self.__background = BackgroundBlock(surface)
        self.__background.transform.set_parent(parent)
        self.__background.transform.position = Vector2(shift_x, shift_y)

        self.__line = BackgroundLine(surface)
        self.__line.transform.set_parent(self.__background.transform)
        self.__line.transform.position = Vector2(0, self.__background.transform.size.y - HEIGHT_LINE)
        self.__line.loading_image()

        # Создание текста, пароль, который ввел пользователь
        # self.__password = Text(surface=self.__surface, text=self.__text_password, size_font=SIZE_FONT,
        #                        color=COLOR_GRAY_BLOCK,
        #                        path_font=DEFAULT_PATH_FONT,
        #                        parent=self.__parent, selected_positioning=SelectPositioning.left, anti_aliasing=True)

        # self.__background = Rectangle(self.__surface, self.__parent, self.__selected_positioning,
        #                               height, width, shift_x, shift_y, color=COLOR_BLOCK)

        # Имя лобби
        # self.__name = Text(surface=self.__surface, text=name, size_font=SIZE_FONT, color=WHITE,
        #                    path_font=DEFAULT_PATH_FONT,
        #                    parent=self.__background, selected_positioning=SelectPositioning.left, anti_aliasing=True,
        #                    shift_x=DISTANCE_BETWEEN_BLOCK_AND_TEXT, shift_y=-HEIGHT_LINE // 2)

        # Задний фон текста
        # self.__background_name = Image(surface=self.__surface,
        #                                parent=self.__name,
        #                                selected_positioning=SelectPositioning.center,
        #                                height=self.__name.height,
        #                                width=self.__name.width, path=BACKGROUND_NAME)

        # self.__line = Image(self.__surface, BACKGROUND_BLOCK_LINE, self.__background, SelectPositioning.down,
        #                     height=HEIGHT_LINE, width=self.__background.width)

        # self.__button_connection = ButtonDefault(surface=self.__surface, parent=self.__background,
        #                                          selected_positioning=SelectPositioning.right, text="Вход",
        #                                          size_font=SIZE_FONT, color_text=COLOR_TEXT_LOBBY,
        #                                          path_font=DEFAULT_PATH_FONT,
        #                                          shift_x=-DISTANCE_BETWEEN_BLOCK_AND_TEXT, shift_y=-HEIGHT_LINE // 2)

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

    # @property
    # def x(self):
    #     return self.__background.x

    # @property
    # def y(self):
    #     return self.__background.y

    # def checking_clicks(self, mouse, is_clicked=False):
    #     self.__button_connection.check_input_button(mouse, is_clicked)

    # Отрисовка блока
    def draw(self) -> None:
        self.__background.draw()
        self.__line.draw()
    #     self.__line.draw()
    #     self.__background_name.draw()
    #     self.__name.draw()
    #     self.__button_connection.draw()
