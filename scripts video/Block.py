from AllConditions import ConditionBlock, ConditionFunctionMap
import pygame


# Класс служит вектором 2
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Block:
    """  Класс блока, используется для проверки, что в данный момент происходит с конкретным блоком """

    def __init__(self, x, y, border_x, border_y, block_size, color_default, color_select, color_hit, color_miss,
                 color_lock) -> None:
        # Позиция блока по оси X
        self.pos_x = x * block_size + border_x
        # Позиция блока по оси Y
        self.pos_y = y * block_size + border_y
        # Размер блока
        self.block_size = block_size
        # Номер блока
        self.number_block = (x, y)
        # Длина корабля в котором находится данный блок
        self.len_ship_which_block_located = 0

        # Позиция точек блока
        self.pos_left_up = Point(self.pos_x, self.pos_y)
        self.pos_right_up = Point(self.pos_x + block_size, self.pos_y)
        self.pos_left_down = Point(self.pos_x, self.pos_y + block_size)
        self.pos_right_down = Point(self.pos_x + block_size, self.pos_y + block_size)

        # Цвета, которые может принимать блока
        self.color_default = color_default
        self.color_select = color_select
        self.color_lock = color_lock
        self.color_hit = color_hit
        self.color_miss = color_miss

        self.rect = pygame.Rect(self.pos_x, self.pos_y, self.block_size, self.block_size)

        # Цвет, который выбран в данный момент у блока
        self.color_selected = self.color_default
        # Состояние блока
        self.condition_block = ConditionBlock.Empty

    # Смена состояния блока
    def __change_condition_color(self, new_condition, new_color) -> None:
        self.condition_block = new_condition
        self.color_selected = new_color

    # Смена состояния блока на блокированное
    def change_to_lock(self, lock=False) -> None:
        if lock:
            self.condition_block = ConditionBlock.Lock
        self.color_selected = self.color_lock

    # Смена состояния блока на пустое
    def change_to_empty(self) -> None:
        self.__change_condition_color(ConditionBlock.Empty, self.color_default)

    # Смена состояния блока на поврежденный
    def change_to_hit(self) -> None:
        self.__change_condition_color(ConditionBlock.Hit, self.color_hit)

    # Смена состояния блока на промах
    def change_to_miss(self) -> None:
        self.__change_condition_color(ConditionBlock.Miss, self.color_miss)

    # Смена состояния блока на выбранный
    def change_to_selected(self) -> None:
        self.__change_condition_color(ConditionBlock.Selected, self.color_select)

    # Проверка нажатия на блок
    def check_input_block(self, mouse) -> bool:
        if self.rect.topleft[0] < mouse[0] < self.rect.bottomright[0] and self.rect.topleft[1] < mouse[1] < self.rect.bottomright[1]:
            return True
        return False

    # Получение информации о блоке, для того, чтобы разукрасить
    def get_info_draw_block(self) -> dict:
        return {'color_selected': self.color_selected, 'position': self.rect, 'number_block': self.number_block}

    # Проверка состояния блока
    def check_condition_block(self):
        function_block = {}
        # По блоку попали
        if self.condition_block == ConditionBlock.Selected:
            function_block = {'function': 'hit', 'next_motion': False}
            self.change_to_hit()
        # Промах
        elif self.condition_block == ConditionBlock.Empty:
            function_block = {'function': 'miss', 'next_motion': True}
            self.change_to_miss()
        return function_block
