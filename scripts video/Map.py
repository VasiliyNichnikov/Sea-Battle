from Block import Block
from AllConditions import ConditionMap
from ColorsAndMainParameters import WHITE, BLACK, RED
from ColorsAndMainParameters import number_blocks, block_size, border, distance_between_blocks, \
    distance_screen_up_maps, height, width, distance_between_maps
import pygame

""" Класс отвечает за карту игрока или врага """


class Map:
    def __init__(self, surface, name, condition_map):
        # Экран на котором будет отрисовываться карта
        # self.surface = surface
        # Имя карты
        self.name = name
        # Состояние карты
        self.condition_map = condition_map

        # Граница по оси X
        self.border_x = distance_between_maps + width
        # Граница по оси Y
        self.border_y = distance_screen_up_maps

        if self.condition_map == ConditionMap.Player:
            # Граница по оси X
            self.border_x = border

        # Поле отрисовки
        self.surface = surface
        # Список с блоками
        self.list_blocks = []

    # Создание блоков
    def create_blocks(self):
        for y in range(number_blocks):
            for x in range(number_blocks):
                new_block = Block(x=x, y=y,
                                  border_x=self.border_x,
                                  border_y=self.border_y,
                                  block_size=block_size,
                                  color_select=BLACK,
                                  color_default=WHITE,
                                  color_lock=RED)
                self.list_blocks.append(new_block)

    # Отрисовка карты
    def draw_map(self) -> None:
        pos = block_size
        for line in range(number_blocks - 1):
            if self.condition_map == ConditionMap.Player:
                point_start_line_one, point_end_line_one = (border, pos + distance_screen_up_maps), (height + border, pos + distance_screen_up_maps)
                point_start_line_two, point_end_line_two = (pos + border, distance_screen_up_maps), (pos + border, height + distance_screen_up_maps)
            else:
                point_start_line_one, point_end_line_one = (distance_between_maps + width, pos + distance_screen_up_maps), (distance_between_maps + width * 2, pos + distance_screen_up_maps)
                point_start_line_two, point_end_line_two = (distance_between_maps + width + pos, distance_screen_up_maps), (distance_between_maps + width + pos, height + distance_screen_up_maps),

            pygame.draw.line(self.surface, BLACK, point_start_line_one, point_end_line_one, distance_between_blocks)
            pygame.draw.line(self.surface, BLACK, point_start_line_two, point_end_line_two, distance_between_blocks)
            pos += block_size

        # Отрисовка рамки врага и игрока
        color_player, color_enemy = BLACK, BLACK
        pygame.draw.rect(self.surface, color_player, (border, distance_screen_up_maps, height, width),
                         distance_between_blocks * 2)
        pygame.draw.rect(self.surface, color_enemy, (width + distance_between_maps, distance_screen_up_maps, width, height),
                         distance_between_blocks * 2)

