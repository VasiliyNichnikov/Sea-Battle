# from block import Block
# from ship import Ship
# from allConditions import ConditionMap, ConditionPlayerMap, ConditionBlock
from scripts.colorsAndMainParameters import WHITE, BLACK, RED, GREEN, YANDEX_COLOR, SEA_WATER
from scripts.colorsAndMainParameters import number_blocks, block_size, border, distance_between_blocks, \
    distance_screen_up_maps, height, width, distance_between_maps
import pygame
from pygame import Surface, Vector2, Rect
from scripts.game.block.block import Block
from scripts.game.map.condition import EnumMap
from scripts.game.map.fieldBorderDrawParameters import FieldBorderDrawParameters
from scripts.game.map.parametersMap import ParametersMap


class Map:
    def __init__(self, surface: Surface, name: str):
        self.__parameters = ParametersMap(surface, name, Vector2(distance_between_maps + width,
                                                                 distance_screen_up_maps))
        # self.condition_player_map = condition_player_map
        # self.condition_map = ConditionMap.Default
        # self.list_json_file = list_json_file

        # self.border_x = distance_between_maps + width
        # self.border_y = distance_screen_up_maps

        # if self.condition_player_map == ConditionPlayerMap.Player:
        #     self.border_x = border

        # self.surface = surface
        # self.list_blocks = []
        # self.list_ships = []
        # self.rect = pygame.Rect(self.border_x, self.border_y, block_size * number_blocks, block_size * number_blocks)

        # self.__create_blocks()

        # if self.list_json_file is not None:
        #     self.__convert_json_file_and_search_ships()
        #     self.condition_map = ConditionMap.Lock

    # def __convert_json_file_and_search_ships(self):
    #     for block in self.list_blocks:
    #         x, y = block.number_block
    #         if self.list_json_file[y][x] == '1':
    #             block.change_to_selected()
    #         else:
    #             block.change_to_empty()
    #     self.__searching_ships()

    def __create_blocks(self):
        blocks = self.__parameters.blocks
        for y in range(number_blocks):
            for x in range(number_blocks):
                new_block = Block(surface=self.__parameters.surface,
                                  number_block=Vector2(x, y),
                                  border=self.__parameters.border,
                                  block_size=block_size)
                blocks[x][y] = new_block
                print(blocks[x][y])

    def draw(self) -> None:
        self.__draw_fields()

    def __draw_fields(self):
        position = block_size

        player_field_draw_parameters = FieldBorderDrawParameters(
            position=Rect(border, distance_screen_up_maps, height, width), color=BLACK)
        enemy_field_draw_parameters = FieldBorderDrawParameters(
            position=Rect(width + distance_between_maps, distance_screen_up_maps, width, height), color=RED)

        for line in range(number_blocks - 1):
            self.__draw_field(EnumMap.Player, position, player_field_draw_parameters)
            self.__draw_field(EnumMap.Enemy, position, enemy_field_draw_parameters)
            position += block_size

    def __draw_field(self, enum_map: EnumMap, position: int, field_draw_parameters: FieldBorderDrawParameters) -> None:
        if enum_map == EnumMap.Player:
            player_points_line = self.__get_position_lines(EnumMap.Player, position)
            self.__draw_lines(player_points_line)
        else:
            enemy_points_line = self.__get_position_lines(EnumMap.Enemy, position)
            self.__draw_lines(enemy_points_line)
        self.__draw_outline_field_border(field_draw_parameters.color,
                                         field_draw_parameters.position)

    @staticmethod
    def __get_position_lines(enum_map: EnumMap, position: int) -> dict:
        if enum_map == EnumMap.Player:
            point_start_line_one = (border, position + distance_screen_up_maps)
            point_end_line_one = (height + border, position + distance_screen_up_maps)
            point_start_line_two = (position + border, distance_screen_up_maps)
            point_end_line_two = (position + border, height + distance_screen_up_maps)
        else:
            point_start_line_one = (distance_between_maps + width, position + distance_screen_up_maps)
            point_end_line_one = (distance_between_maps + width * 2, position + distance_screen_up_maps)
            point_start_line_two = (distance_between_maps + width + position, distance_screen_up_maps)
            point_end_line_two = (distance_between_maps + width + position, height + distance_screen_up_maps)

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

    def __draw_outline_field_border(self, field_border_color: tuple, field_border_position: tuple) -> None:
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
