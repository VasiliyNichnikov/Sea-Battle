import pygame
import json
from enum import Enum


class ConditionBlock(Enum):
    Empty = 0
    Selected = 1
    Lock = 2


class ConditionMotion(Enum):
    Player = 0
    Enemy = 1


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Button:
    def __init__(self, surface, pos_x, pos_y, height, width, color_btn=(0, 0, 0), text='None',
                 color_text=(255, 255, 255), path_font='None', size_font=30):
        self.surface = surface
        self.pos_x = pos_x
        self.pos_y = pos_y

        self.height = height
        self.width = width
        self.rect = pygame.Rect(pos_x, pos_y, width, height)

        self.color_btn = color_btn
        self.text = text
        self.color_text = color_text
        self.path_font = path_font
        self.size_font = size_font
        self.input_btn = False

    def draw_button(self):
        if self.input_btn:
            pygame.draw.rect(self.surface, self.color_btn, (self.pos_x, self.pos_y, self.width, self.height))
        else:
            pygame.draw.rect(self.surface, self.color_btn, (self.pos_x, self.pos_y, self.width, self.height), 2)
        text_btn = self.__draw_text()
        surface.blit(text_btn, (
            self.pos_x + (self.width - text_btn.get_width()) // 2,
            self.pos_y + (self.height - text_btn.get_height()) // 2))

    def check_input_button(self, mouse, click=False):
        if self.rect.topleft[0] < mouse[0] < self.rect.bottomright[0] and self.rect.topleft[1] < mouse[1] < \
                self.rect.bottomright[1] and click:
            self.input_btn = True
        else:
            self.input_btn = False
        return self.input_btn

    def __draw_text(self):
        font = pygame.font.Font(self.path_font, self.size_font)
        text = font.render(self.text, True, self.color_text)
        return text


# Класс кораблей
class Ship:
    def __init__(self, list_blocks_ship):
        self.len_ship = len(list_blocks_ship)
        self.list_blocks_ship = list_blocks_ship

        for block in self.list_blocks_ship:
            block.len_ship = self.len_ship


class Block:
    def __init__(self, x, y, border_x, border_y, block_size, color_default, color_select, color_lock):
        self.pos_x = x * block_size + border_x
        self.pos_y = y * block_size + border_y
        self.size_block = block_size
        self.number_block = (x, y)
        self.len_ship = 0

        self.pos_left_up = Point(self.pos_x, self.pos_y)
        self.pos_right_up = Point(self.pos_x + block_size, self.pos_y)
        self.pos_left_down = Point(self.pos_x, self.pos_y + block_size)
        self.pos_right_down = Point(self.pos_x + block_size, self.pos_y + block_size)

        self.color_default = color_default
        self.color_select = color_select
        self.color_lock = color_lock

        self.color_selected = self.color_default

        self.list_main_blocks = []
        self.condition_block = ConditionBlock.Empty

    def __change_condition_color(self, new_condition, new_color):
        self.condition_block = new_condition
        self.color_selected = new_color
        # self.draw_block()

    def change_to_lock(self, lock=False):

        if lock:
            self.condition_block = ConditionBlock.Lock
        self.color_selected = self.color_lock

    def change_to_empty(self):
        self.__change_condition_color(ConditionBlock.Empty, self.color_default)

    def change_to_selected(self):
        if self.condition_block == ConditionBlock.Empty:
            self.__change_condition_color(ConditionBlock.Selected, self.color_select)
        else:
            self.__change_condition_color(ConditionBlock.Empty, self.color_default)

    def draw_block(self):
        pygame.draw.rect(surface, self.color_selected, (self.pos_x, self.pos_y, self.size_block, self.size_block))


def change_block(block):
    block.change_to_selected()
    if block.condition_block == ConditionBlock.Selected:
        list_selected_blocks.append(block)
    elif block.condition_block == ConditionBlock.Empty:
        list_selected_blocks.remove(block)
        list_remove_selected_blocks.append(block)

    if len(list_remove_selected_blocks) > 0:
        for block_remove_selected in list_remove_selected_blocks:
            dict_blocks_corners_cross = get_blocks_nearby_cross_and_corners(block_remove_selected)
            for block_remove in dict_blocks_corners_cross['corners'] + dict_blocks_corners_cross['cross']:
                block_remove.len_ship = 0
                block_remove.change_to_empty()
            list_remove_selected_blocks.clear()

    for selected_blocks in list_selected_blocks:
        dict_blocks_corners_cross = get_blocks_nearby_cross_and_corners(selected_blocks)
        for block_nearby_corners in dict_blocks_corners_cross['corners']:
            block_nearby_corners.change_to_lock(lock=True)
        for block_nearby_cross in dict_blocks_corners_cross['cross']:
            block_nearby_cross.change_to_lock()

    list_ships.clear()
    for block in list_blocks:
        if block.condition_block == ConditionBlock.Selected and not check_block_ship(block):
            new_ship = Ship(search_nearest_blocks(block, 1, []))
            list_ships.append(new_ship)


# Проверяем на какой блок нажала мышь
def check_input_mouse(pos_mouse):
    # global end_input_mouse_block
    pos_mouse_x, pos_mouse_y = pos_mouse

    for block in list_blocks:
        pos_left_up_y = block.pos_left_up.y
        pos_right_down_y = block.pos_right_down.y

        pos_left_down_x = block.pos_left_down.x
        pos_right_down_x = block.pos_right_down.x

        if pos_left_down_x < pos_mouse_x < pos_right_down_x and pos_left_up_y < pos_mouse_y < pos_right_down_y and \
                block.condition_block != ConditionBlock.Lock and \
                (check_ship_nearest(block) or block.condition_block == ConditionBlock.Selected):
            block.change_to_selected()
            change_motion()
            break


def get_blocks_nearby_cross_and_corners(block):
    blocks_nearby_corners = get_blocks_nearby(block, condition='corners')
    blocks_nearby_cross = list(filter(lambda b: b.condition_block != ConditionBlock.Selected,
                                      get_blocks_nearby(block, condition='cross')))
    return {'corners': blocks_nearby_corners, 'cross': blocks_nearby_cross}


# Получение угловых блоков
def get_blocks_nearby(select_block, condition='corners'):
    x, y = select_block.number_block
    if condition == 'corners':
        list_positions_blocks = [(x - 1, y - 1), (x - 1, y + 1), (x + 1, y - 1), (x + 1, y + 1)]
    else:
        list_positions_blocks = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    return [block for block in list_blocks if block.number_block in list_positions_blocks]


# Получение текста
def get_text(text, size_font, color, anti_aliasing=False, path='None'):
    font = pygame.font.Font(path, size_font)
    text = font.render(text, anti_aliasing, color)
    return text


def search_nearest_blocks(start_block, number, list_block_passed):
    list_block_passed.append(start_block)
    block_nearby_cross = get_blocks_nearby(start_block, condition='cross')
    for block in block_nearby_cross:
        if block.condition_block == ConditionBlock.Selected and block != start_block and block not in list_block_passed:
            search_nearest_blocks(block, number, list_block_passed)
    return list_block_passed


def check_ship_nearest(block):
    for ship in list_ships:
        ready_len_ship = 0
        for block_nearby in list(filter(lambda b: b.condition_block == ConditionBlock.Selected,
                                        get_blocks_nearby(block, condition='cross'))):
            ready_len_ship += block_nearby.len_ship
            if block_nearby in ship.list_blocks_ship and ship.len_ship == 4:
                return False
        if ready_len_ship >= 4:
            return False
    return True


def check_block_ship(block):
    for ship in list_ships:
        if block in ship.list_blocks_ship:
            return True
    return False


# Сохранение карты
def save_map():
    with open(path_save_map + 'map_player.json', 'w', encoding='utf-8') as json_write:
        ready_list = []
        number = 0
        for i in range(number_blocks):
            string_list = []
            for j in range(number_blocks):
                if list_blocks[number].condition_block == ConditionBlock.Selected:
                    string_list.append('1')
                else:
                    string_list.append('0')
                number += 1
            ready_list.append(string_list)
        file_map = {
            'description': ready_list
        }
        json.dump(file_map, json_write)


def create_blocks(border_x=0, border_y=0):
    for y in range(number_blocks):
        for x in range(number_blocks):
            new_block = Block(x=x, y=y,
                              border_x=border_x,
                              border_y=border_y,
                              block_size=block_size,
                              color_select=BLACK,
                              color_default=WHITE,
                              color_lock=RED)
            list_blocks.append(new_block)


# Рисование карты
def draw_map():
    for block in list_blocks:
        block.draw_block()

    pos = block_size
    for line in range(number_blocks - 1):
        pygame.draw.line(surface, BLACK, (border, pos + shift_along_axis_y),
                         (height + border, pos + shift_along_axis_y), distance_between_blocks)
        pygame.draw.line(surface, BLACK, (pos + border, shift_along_axis_y),
                         (pos + border, height + shift_along_axis_y), distance_between_blocks)
        pos += block_size

    pos = block_size
    for line in range(number_blocks - 1):
        pygame.draw.line(surface, BLACK,
                         (distance_between_maps + width, pos + shift_along_axis_y),
                         (distance_between_maps + width * 2, pos + shift_along_axis_y), distance_between_blocks)
        pygame.draw.line(surface, BLACK,
                         (distance_between_maps + width + pos, shift_along_axis_y),
                         (distance_between_maps + width + pos, height + shift_along_axis_y), distance_between_blocks)
        pos += block_size

    color_player, color_enemy = BLACK, RED
    if condition_motion == ConditionMotion.Player:
        color_player, color_enemy = GREEN, BLACK

    pygame.draw.rect(surface, color_player, (border, shift_along_axis_y, height, width), distance_between_blocks * 2)
    pygame.draw.rect(surface, color_enemy, (width + distance_between_maps, shift_along_axis_y, width, height), distance_between_blocks * 2)


# Смена хода
def change_motion():
    global condition_motion
    if condition_motion == ConditionMotion.Enemy:
        condition_motion = ConditionMotion.Player
    else:
        condition_motion = ConditionMotion.Enemy


# Основные переменные
height = width = 500
distance_between_maps = 40
shift_along_axis_y = 50
border = 5
FPS = 60
condition_motion = ConditionMotion.Player
number_blocks = 10
block_size = height // number_blocks
distance_between_blocks = 2
list_blocks = []
# additional_area_width = 250
path_save_map = 'static/'
end_input_mouse_block = None
number_finished_ships = 0
list_ships = []
list_selected_blocks = []
list_remove_selected_blocks = []
path_font = 'Fonts/main_font.otf'

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE_AZURE = (42, 82, 190)
GREEN = (0, 128, 0)

# Инициализация игры
pygame.init()
surface = pygame.display.set_mode((width * 2 + distance_between_maps + border, height + shift_along_axis_y + border))
clock = pygame.time.Clock()
pygame.display.set_caption('Sea Battle')
surface.fill(WHITE)
create_blocks(border_x=border, border_y=shift_along_axis_y)
create_blocks(border_x=distance_between_maps + width, border_y=shift_along_axis_y)
runner = True

# Создание кнопок
# button_save = Button(surface, width + (additional_area_width - block_size * 4) // 2, height - block_size - 10,
#                      block_size, block_size * 4, BLACK, 'СОХРАНИТЬ', BLUE_AZURE, path_font, 30)

# Запуск игры
while runner:
    clock.tick(FPS)
    draw_map()

    text_player = get_text('PLAYER', 40, BLUE_AZURE, True, path_font)
    surface.blit(text_player, (border + width // 2 - text_player.get_width() // 2,
                               shift_along_axis_y // 2 - text_player.get_height() // 2 + border))

    text_enemy = get_text('ENEMY_251', 40, RED, True, path_font)
    surface.blit(text_enemy, (border + width // 2 - text_enemy.get_width() // 2 + width + distance_between_maps,
                              shift_along_axis_y // 2 - text_enemy.get_height() // 2 + border))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runner = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                check_input_mouse(event.pos)
                # check_input_mouse(event.pos)
                # if button_save.check_input_button(event.pos, True):
                #     save_map()
        elif event.type == pygame.MOUSEBUTTONUP:
            pass
            # if event.button == 1:
            #     button_save.check_input_button(event.pos)

    pygame.display.flip()
    surface.fill(WHITE)
pygame.quit()
