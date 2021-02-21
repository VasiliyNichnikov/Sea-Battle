from Block import Block
from AllConditions import ConditionMap, ConditionPlayerMap, ConditionBlock
from ColorsAndMainParameters import WHITE, BLACK, RED, YANDEX_COLOR
from ColorsAndMainParameters import number_blocks, block_size, border, distance_between_blocks, \
    distance_screen_up_maps, height, width, distance_between_maps
import pygame

""" Класс отвечает за карту игрока или врага """


class Map:
    def __init__(self, surface, name, condition_player_map, list_json_file=None):
        # Имя карты
        self.name = name
        # Состояние карты игрока
        self.condition_player_map = condition_player_map
        # Состояние карты
        self.condition_map = ConditionMap.Default
        # Список блоков из json файла
        self.list_json_file = list_json_file

        # Граница по оси X
        self.border_x = distance_between_maps + width
        # Граница по оси Y
        self.border_y = distance_screen_up_maps

        if self.condition_player_map == ConditionPlayerMap.Player:
            # Граница по оси X
            self.border_x = border

        # Поле отрисовки
        self.surface = surface
        # Список с блоками
        self.list_blocks = []
        self.rect = pygame.Rect(self.border_x, self.border_y, block_size * number_blocks, block_size * number_blocks)

        # Создание блоков
        self.__create_blocks()

        # Преобразование блоков из json файла
        if self.list_json_file is not None:
            self.__convert_json_file()
            self.condition_map = ConditionMap.Lock

    # Преобразовать json файл блоков
    def __convert_json_file(self):
        for block in self.list_blocks:
            x, y = block.number_block
            if self.list_json_file[y][x] == '1':
                block.change_to_selected()
            else:
                block.change_to_empty()

    # Создание блоков
    def __create_blocks(self):
        for y in range(number_blocks):
            for x in range(number_blocks):
                new_block = Block(x=x, y=y,
                                  border_x=self.border_x,
                                  border_y=self.border_y,
                                  block_size=block_size,
                                  color_select=BLACK,
                                  color_default=WHITE,
                                  color_hit=RED,
                                  color_miss=YANDEX_COLOR,
                                  color_lock=RED)
                self.list_blocks.append(new_block)

    # Отрисовка карты
    def draw_map(self) -> None:
        for block in self.list_blocks:
            parameters_block = block.get_info_draw_block()
            pygame.draw.rect(self.surface, parameters_block['color_selected'], parameters_block['position'])

        color_frame = BLACK
        pos = block_size
        for line in range(number_blocks - 1):
            if self.condition_player_map == ConditionPlayerMap.Player:
                point_start_line_one, point_end_line_one = (border, pos + distance_screen_up_maps), (
                    height + border, pos + distance_screen_up_maps)
                point_start_line_two, point_end_line_two = (pos + border, distance_screen_up_maps), (
                    pos + border, height + distance_screen_up_maps)
                position_frame = (border, distance_screen_up_maps, height, width)

            else:
                point_start_line_one, point_end_line_one = (distance_between_maps + width,
                                                            pos + distance_screen_up_maps), (
                                                               distance_between_maps + width * 2,
                                                               pos + distance_screen_up_maps)
                point_start_line_two, point_end_line_two = (distance_between_maps + width + pos,
                                                            distance_screen_up_maps), (
                                                               distance_between_maps + width + pos,
                                                               height + distance_screen_up_maps)
                position_frame = (width + distance_between_maps, distance_screen_up_maps, width, height)

            pygame.draw.line(self.surface, BLACK, point_start_line_one, point_end_line_one, distance_between_blocks)
            pygame.draw.line(self.surface, BLACK, point_start_line_two, point_end_line_two, distance_between_blocks)
            pygame.draw.rect(self.surface, color_frame, position_frame, distance_between_blocks * 2)

            pos += block_size

    # Получение блока по position блока
    def get_block_using_position(self, position):
        for block in self.list_blocks:
            if block.number_block == tuple(position):
                return block
        # Ошибка, такого не должно быть
        return None

    # Возвращает блок на который нажал игрок
    def get_block_input_map(self, mouse):
        if self.rect.topleft[0] < mouse[0] < self.rect.bottomright[0] and self.rect.topleft[1] < mouse[1] < \
                self.rect.bottomright[1] and self.condition_map != ConditionMap.Lock:
            # Проверка блока, на который нажали
            for block in self.list_blocks:
                if block.check_input_block(mouse) and (block.condition_block == ConditionBlock.Selected
                                                       or block.condition_block == ConditionBlock.Empty):
                    return block
        return None
