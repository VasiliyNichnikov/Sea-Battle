from block import Block
from ship import Ship
from allConditions import ConditionMap, ConditionPlayerMap, ConditionBlock
from colorsAndMainParameters import WHITE, BLACK, RED, GREEN, YANDEX_COLOR, SEA_WATER
from colorsAndMainParameters import number_blocks, block_size, border, distance_between_blocks, \
    distance_screen_up_maps, height, width, distance_between_maps
import pygame
from pygame import Surface, Vector2
from scripts.game.block.block import Block
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

    def __convert_json_file_and_search_ships(self):
        for block in self.list_blocks:
            x, y = block.number_block
            if self.list_json_file[y][x] == '1':
                block.change_to_selected()
            else:
                block.change_to_empty()
        self.__searching_ships()

    def __create_blocks(self):
        list_blocks = self.__parameters.list_blocks
        for y in range(number_blocks):
            for x in range(number_blocks):
                new_block = Block(surface=self.__parameters.surface,
                                  number_block=Vector2(x, y),
                                  border=self.__parameters.border,
                                  block_size=block_size)
                list_blocks.append(new_block)

    def draw_map(self, condition_motion) -> None:
        color_frame = BLACK
        pos = block_size

        blocks_not_empty = list(filter(lambda b: b.condition_block != ConditionBlock.Empty, self.list_blocks))

        for block in self.list_blocks:
            block.draw_water()

        for line in range(number_blocks - 1):
            if self.condition_player_map == ConditionPlayerMap.Player:
                point_start_line_one, point_end_line_one = (border, pos + distance_screen_up_maps), (
                    height + border, pos + distance_screen_up_maps)
                point_start_line_two, point_end_line_two = (pos + border, distance_screen_up_maps), (
                    pos + border, height + distance_screen_up_maps)
                position_frame = (border, distance_screen_up_maps, height, width)

                if condition_motion == ConditionPlayerMap.Player:
                    color_frame = GREEN

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

                if condition_motion == ConditionPlayerMap.Enemy:
                    color_frame = RED

            pygame.draw.line(self.surface, SEA_WATER, point_start_line_one, point_end_line_one, distance_between_blocks)
            pygame.draw.line(self.surface, SEA_WATER, point_start_line_two, point_end_line_two, distance_between_blocks)
            pygame.draw.rect(self.surface, color_frame, position_frame, distance_between_blocks * 2)
            pos += block_size

        for block in blocks_not_empty:
            block.draw_images_ships(self.condition_player_map)

    def __searching_ships(self):
        for block in self.list_blocks:
            if block.condition_block == ConditionBlock.Selected and not self.__check_block_ship(block):
                new_ship = Ship(self.__search_nearest_blocks(block, []))
                self.list_ships.append(new_ship)

    def __search_nearest_blocks(self, start_block, list_block_passed):
        list_block_passed.append(start_block)
        block_nearby_cross = self.__get_blocks_nearby(start_block, condition='cross')
        for block in block_nearby_cross:
            if block.condition_block == ConditionBlock.Selected and block != start_block and block not in list_block_passed:
                self.__search_nearest_blocks(block, list_block_passed)
        return list_block_passed

    def __check_block_ship(self, block):
        for ship in self.list_ships:
            if block in ship.list_blocks_ship:
                return True
        return False

    def __get_blocks_nearby(self, select_block, condition='corners'):
        x, y = select_block.number_block
        if condition == 'corners':
            list_positions_blocks = [(x - 1, y - 1), (x - 1, y + 1), (x + 1, y - 1), (x + 1, y + 1)]
        else:
            list_positions_blocks = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        return [block for block in self.list_blocks if block.number_block in list_positions_blocks]

    def __get_blocks_nearby_cross_and_corners(self, block, select_condition_block):
        blocks_nearby_corners = self.__get_blocks_nearby(block, condition='corners')
        blocks_nearby_cross = list(filter(lambda b: b.condition_block != select_condition_block,
                                          self.__get_blocks_nearby(block, condition='cross')))
        return {'corners': blocks_nearby_corners, 'cross': blocks_nearby_cross}

    def get_block_using_position(self, position):
        for block in self.list_blocks:
            if block.number_block == tuple(position):
                return block
        # Ошибка, такого не должно быть
        return None

    def draw_ships_blocks(self, blocks):
        for block in blocks:
            blocks_cross_corners = self.__get_blocks_nearby_cross_and_corners(block, ConditionBlock.Hit)
            blocks_corners = blocks_cross_corners['corners']
            blocks_cross = blocks_cross_corners['cross']
            for block_cross_and_corner in blocks_corners + blocks_cross:
                block_cross_and_corner.change_to_lock(lock=True)

    def create_ship(self, list_blocks):
        new_ship = Ship(list_blocks)
        self.list_ships.append(new_ship)

    def get_block_input_map(self, mouse):
        if self.rect.topleft[0] < mouse[0] < self.rect.bottomright[0] and self.rect.topleft[1] < mouse[1] < \
                self.rect.bottomright[1] and self.condition_map != ConditionMap.Lock:
            # Проверка блока, на который нажали
            for block in self.list_blocks:
                if block.check_input(mouse) and (block.condition_block == ConditionBlock.Selected
                                                 or block.condition_block == ConditionBlock.Empty) \
                        and block.condition_block != ConditionBlock.Lock:
                    return block
        return None
