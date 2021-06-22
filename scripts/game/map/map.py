# from block import Block
# from ship import Ship
# from allConditions import ConditionMap, ConditionPlayerMap, ConditionBlock
from scripts.colorsAndMainParameters import BLACK, RED, SEA_WATER
from scripts.colorsAndMainParameters import number_blocks, block_size, distance_between_blocks
import pygame
from pygame import Surface, Vector2, Rect
from scripts.game.block.block import Block
from scripts.game.map.condition import EnumMap
from scripts.game.map.fieldBorderDrawParameters import FieldBorderDrawParameters
from scripts.game.map.parametersMap import ParametersMap


class Map:
    def __init__(self, parameters: ParametersMap):
        self.__parameters = parameters

    def __create_blocks(self):
        blocks = self.__parameters.blocks
        for y in range(number_blocks):
            for x in range(number_blocks):
                new_block = Block(surface=self.__parameters.surface,
                                  number_block=Vector2(x, y),
                                  border=self.__parameters.border,
                                  block_size=block_size)
                blocks[x][y] = new_block

    def draw(self) -> None:
        self.__draw_fields()

    def check_input(self, mouse: Vector2) -> bool:
        rect = self.__parameters.rect
        if rect.topleft[0] < mouse[0] < rect.bottomright[0] and rect.topleft[1] < mouse[1] < rect.bottomright[1]:
            return True
        return False

    def __draw_fields(self):
        position = block_size
        condition = self.__parameters.condition
        rect = self.__parameters.rect

        if condition == EnumMap.Player:
            field_draw_parameters = FieldBorderDrawParameters(position=rect, color=BLACK)
        else:
            field_draw_parameters = FieldBorderDrawParameters(position=rect, color=RED)

        for line in range(number_blocks - 1):
            self.__draw_field(position, field_draw_parameters)
            position += block_size

    def __draw_field(self, position: int, field_draw_parameters: FieldBorderDrawParameters) -> None:
        points_line = self.__get_position_lines(position)
        self.__draw_lines(points_line)
        self.__draw_outline_field_border(field_draw_parameters.color,
                                         field_draw_parameters.position)

    def __get_position_lines(self, position: int) -> dict:
        border = self.__parameters.border
        size = self.__parameters.size

        point_start_line_one = (border.x, position + border.y)
        point_end_line_one = (size.x + border.x, position + border.y)
        point_start_line_two = (position + border.x, border.y)
        point_end_line_two = (position + border.x, size.y + border.y)

        return {
            'point_start_line_one': point_start_line_one,
            'point_end_line_one': point_end_line_one,
            'point_start_line_two': point_start_line_two,
            'point_end_line_two': point_end_line_two
        }

    def __draw_lines(self, points: dict) -> None:
        if 'point_start_line_one' not in points.keys() \
                or 'point_end_line_one' not in points.keys() \
                or 'point_start_line_two' not in points.keys() \
                or 'point_end_line_two' not in points.keys():
            raise Exception('Invalid dictionary passed')

        start_line_one, end_line_one = points['point_start_line_one'], points['point_end_line_one']
        start_line_two, end_line_two = points['point_start_line_two'], points['point_end_line_two']

        pygame.draw.line(self.__parameters.surface,
                         SEA_WATER, start_line_one, end_line_one, distance_between_blocks)
        pygame.draw.line(self.__parameters.surface,
                         SEA_WATER, start_line_two, end_line_two, distance_between_blocks)

    def __draw_outline_field_border(self, field_border_color: tuple, field_border_position: Rect) -> None:
        pygame.draw.rect(self.__parameters.surface, field_border_color, field_border_position,
                         distance_between_blocks * 2)

    # def draw_map(self, condition_motion) -> None:
    #     color_frame = BLACK
    #     pos = block_size
    #
    #     blocks_not_empty = list(filter(lambda b: b.condition_block != ConditionBlock.Empty, self.list_blocks))
    #
    #     for block in self.list_blocks:
    #         block.draw_water()
    #
    #     for line in range(number_blocks - 1):
    #         if self.condition_player_map == ConditionPlayerMap.Player:

    #
    #             if condition_motion == ConditionPlayerMap.Player:
    #                 color_frame = GREEN
    #
    #         else:

    #
    #             if condition_motion == ConditionPlayerMap.Enemy:
    #                 color_frame = RED
    #
    #         pygame.draw.line(self.surface, SEA_WATER, point_start_line_one, point_end_line_one, distance_between_blocks)
    #         pygame.draw.line(self.surface, SEA_WATER, point_start_line_two, point_end_line_two, distance_between_blocks)
    #         pygame.draw.rect(self.surface, color_frame, position_frame, distance_between_blocks * 2)
    #         pos += block_size
    #
    #     for block in blocks_not_empty:
    #         block.draw_images_ships(self.condition_player_map)

    # def __searching_ships(self):
    #     for block in self.list_blocks:
    #         if block.condition_block == ConditionBlock.Selected and not self.__check_block_ship(block):
    #             new_ship = Ship(self.__search_nearest_blocks(block, []))
    #             self.list_ships.append(new_ship)

    # def __search_nearest_blocks(self, start_block, list_block_passed):
    #     list_block_passed.append(start_block)
    #     block_nearby_cross = self.__get_blocks_nearby(start_block, condition='cross')
    #     for block in block_nearby_cross:
    #         if block.condition_block == ConditionBlock.Selected and block != start_block and block not in list_block_passed:
    #             self.__search_nearest_blocks(block, list_block_passed)
    #     return list_block_passed

    # def __check_block_ship(self, block):
    #     for ship in self.list_ships:
    #         if block in ship.list_blocks_ship:
    #             return True
    #     return False

    # def __get_blocks_nearby(self, select_block, condition='corners'):
    #     x, y = select_block.number_block
    #     if condition == 'corners':
    #         list_positions_blocks = [(x - 1, y - 1), (x - 1, y + 1), (x + 1, y - 1), (x + 1, y + 1)]
    #     else:
    #         list_positions_blocks = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    #     return [block for block in self.list_blocks if block.number_block in list_positions_blocks]

    # def __get_blocks_nearby_cross_and_corners(self, block, select_condition_block):
    #     blocks_nearby_corners = self.__get_blocks_nearby(block, condition='corners')
    #     blocks_nearby_cross = list(filter(lambda b: b.condition_block != select_condition_block,
    #                                       self.__get_blocks_nearby(block, condition='cross')))
    #     return {'corners': blocks_nearby_corners, 'cross': blocks_nearby_cross}

    # def get_block_using_position(self, position):
    #     for block in self.list_blocks:
    #         if block.number_block == tuple(position):
    #             return block
    #     # Ошибка, такого не должно быть
    #     return None

    # def draw_ships_blocks(self, blocks):
    #     for block in blocks:
    #         blocks_cross_corners = self.__get_blocks_nearby_cross_and_corners(block, ConditionBlock.Hit)
    #         blocks_corners = blocks_cross_corners['corners']
    #         blocks_cross = blocks_cross_corners['cross']
    #         for block_cross_and_corner in blocks_corners + blocks_cross:
    #             block_cross_and_corner.change_to_lock(lock=True)

    # def create_ship(self, list_blocks):
    #     new_ship = Ship(list_blocks)
    #     self.list_ships.append(new_ship)

    # def get_block_input_map(self, mouse):
    #     if self.rect.topleft[0] < mouse[0] < self.rect.bottomright[0] and self.rect.topleft[1] < mouse[1] < \
    #             self.rect.bottomright[1] and self.condition_map != ConditionMap.Lock:
    #         # Проверка блока, на который нажали
    #         for block in self.list_blocks:
    #             if block.check_input(mouse) and (block.condition_block == ConditionBlock.Selected
    #                                              or block.condition_block == ConditionBlock.Empty) \
    #                     and block.condition_block != ConditionBlock.Lock:
    #                 return block
    #     return None
