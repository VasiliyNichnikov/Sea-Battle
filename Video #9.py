import pygame
import json
from enum import Enum
import requests
from threading import Thread
from requests.exceptions import HTTPError


class ConditionBlock(Enum):
    Empty = 0
    Selected = 1
    Lock = 2
    Miss = 3
    Hit = 4


class ConditionMotion(Enum):
    Player = 0
    Enemy = 1


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


# Класс корабля
class Ship:
    def __init__(self, list_blocks_ship):
        self.len_ship = len(list_blocks_ship)
        self.list_blocks_ship = list_blocks_ship

        for block in self.list_blocks_ship:
            block.len_ship = self.len_ship


# Класс блока
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

    def __change_condition_color(self, new_condition, new_color) -> None:
        self.condition_block = new_condition
        self.color_selected = new_color

    def change_to_lock(self, lock=False) -> None:
        if lock:
            self.condition_block = ConditionBlock.Lock
        self.color_selected = self.color_lock

    def change_to_empty(self) -> None:
        self.__change_condition_color(ConditionBlock.Empty, self.color_default)

    def change_to_selected(self) -> None:
        self.__change_condition_color(ConditionBlock.Selected, self.color_select)

    def draw_block(self) -> None:
        pygame.draw.rect(surface, self.color_selected, (self.pos_x, self.pos_y, self.size_block, self.size_block))


# Отправка данных на сервер
class ServerThread(Thread):
    def __init__(self, method_name, method_finished, json_parameters=None):
        Thread.__init__(self)
        self.session = requests.Session()
        self.method_name = method_name
        self.method_finished = method_finished
        self.json_parameters = json_parameters
        self.result = None

    def check_json_parameters(self):
        return self.json_parameters is None

    def run(self):
        try:
            if self.check_json_parameters():
                print(url_server + self.method_name + '/' + player_id)
                result = self.session.get(url_server + self.method_name + '/' + player_id)
                if result.status_code == 200 and result.json()['condition']:
                    self.method_finished()
            else:
                pass
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  # Python 3.6
        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6


# Получение и отправка информации на сервер
# def get_send_information_server(method_name, user_id, json_parameters=None):
#     if json_parameters is None:
#         return session.get(url_server + method_name + user_id)
#     else:
#         pass

# def change_block(block):
#     block.change_to_selected()
#     if block.condition_block == ConditionBlock.Selected:
#         list_selected_blocks.append(block)
#     elif block.condition_block == ConditionBlock.Empty:
#         list_selected_blocks.remove(block)
#         list_remove_selected_blocks.append(block)
#
#     if len(list_remove_selected_blocks) > 0:
#         for block_remove_selected in list_remove_selected_blocks:
#             dict_blocks_corners_cross = get_blocks_nearby_cross_and_corners(block_remove_selected)
#             for block_remove in dict_blocks_corners_cross['corners'] + dict_blocks_corners_cross['cross']:
#                 block_remove.len_ship = 0
#                 block_remove.change_to_empty()
#             list_remove_selected_blocks.clear()
#
#     for selected_blocks in list_selected_blocks:
#         dict_blocks_corners_cross = get_blocks_nearby_cross_and_corners(selected_blocks)
#         for block_nearby_corners in dict_blocks_corners_cross['corners']:
#             block_nearby_corners.change_to_lock(lock=True)
#         for block_nearby_cross in dict_blocks_corners_cross['cross']:
#             block_nearby_cross.change_to_lock()
#
#     list_ships.clear()
#     for block in list_blocks:
#         if block.condition_block == ConditionBlock.Selected and not check_block_ship(block):
#             new_ship = Ship(search_nearest_blocks(block, 1, []))
#             list_ships.append(new_ship)


# Проверяем на какой блок нажала мышь
def check_input_mouse(pos_mouse) -> None:
    # global end_input_mouse_block
    pos_mouse_x, pos_mouse_y = pos_mouse

    for block in list_blocks_enemy:
        pos_left_up_y = block.pos_left_up.y
        pos_right_down_y = block.pos_right_down.y

        pos_left_down_x = block.pos_left_down.x
        pos_right_down_x = block.pos_right_down.x

        if pos_left_down_x < pos_mouse_x < pos_right_down_x and pos_left_up_y < pos_mouse_y < pos_right_down_y and \
                block.condition_block != ConditionBlock.Lock:
            block.change_to_selected()
            change_motion()
            break


# def get_blocks_nearby_cross_and_corners(block):
#     blocks_nearby_corners = get_blocks_nearby(block, condition='corners')
#     blocks_nearby_cross = list(filter(lambda b: b.condition_block != ConditionBlock.Selected,
#                                       get_blocks_nearby(block, condition='cross')))
#     return {'corners': blocks_nearby_corners, 'cross': blocks_nearby_cross}


# Получение угловых блоков
# def get_blocks_nearby(select_block, condition='corners'):
#     x, y = select_block.number_block
#     if condition == 'corners':
#         list_positions_blocks = [(x - 1, y - 1), (x - 1, y + 1), (x + 1, y - 1), (x + 1, y + 1)]
#     else:
#         list_positions_blocks = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
#     return [block for block in list_blocks if block.number_block in list_positions_blocks]


# Получение текста
def get_text(text, size_font, color, anti_aliasing=False, path='None'):
    font = pygame.font.Font(path, size_font)
    text = font.render(text, anti_aliasing, color)
    return text


# def search_nearest_blocks(start_block, number, list_block_passed):
#     list_block_passed.append(start_block)
#     block_nearby_cross = get_blocks_nearby(start_block, condition='cross')
#     for block in block_nearby_cross:
#         if block.condition_block == ConditionBlock.Selected and block != start_block and block not in list_block_passed:
#             search_nearest_blocks(block, number, list_block_passed)
#     return list_block_passed


# def check_ship_nearest(block):
#     for ship in list_ships:
#         ready_len_ship = 0
#         for block_nearby in list(filter(lambda b: b.condition_block == ConditionBlock.Selected,
#                                         get_blocks_nearby(block, condition='cross'))):
#             ready_len_ship += block_nearby.len_ship
#             if block_nearby in ship.list_blocks_ship and ship.len_ship == 4:
#                 return False
#         if ready_len_ship >= 4:
#             return False
#     return True


# def check_block_ship(block) -> bool:
#     for ship in list_ships:
#         if block in ship.list_blocks_ship:
#             return True
#     return False


# Сохранение карты
# def save_map():
#     with open(path_save_map + 'map_player.json', 'w', encoding='utf-8') as json_write:
#         ready_list = []
#         number = 0
#         for i in range(number_blocks):
#             string_list = []
#             for j in range(number_blocks):
#                 if list_blocks[number].condition_block == ConditionBlock.Selected:
#                     string_list.append('1')
#                 else:
#                     string_list.append('0')
#                 number += 1
#             ready_list.append(string_list)
#         file_map = {
#             'description': ready_list
#         }
#         json.dump(file_map, json_write)


# Создание классов блока
def create_blocks(list_blocks, border_x=0, border_y=0) -> None:
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
def draw_map() -> None:
    for block in list_blocks_player + list_blocks_enemy:
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
def change_motion() -> None:
    global condition_motion
    if condition_motion == ConditionMotion.Enemy:
        condition_motion = ConditionMotion.Player
    else:
        condition_motion = ConditionMotion.Enemy


# Действие, которое произойдет после решистрации на сервере
def player_entered():
    global player_logged
    player_logged = True


# Открытие json файла
def open_json(path_map) -> dict:
    with open(path_map, 'r', encoding='utf-8') as read_file:
        data = json.load(read_file)
    return data


# Создание блоков на основе json файла
def conversion_blocks(list_blocks, list_json):
    for block in list_blocks:
        x, y = block.number_block
        if list_json[y][x] == '1':
            block.change_to_selected()
        else:
            block.change_to_empty()


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
# Список блоков игрока
list_blocks_player = []
# Список блоков противника
list_blocks_enemy = []
path_save_map = 'static/'
number_finished_ships = 0
list_ships = []
list_selected_blocks = []
list_remove_selected_blocks = []
path_json_player = 'static/map_player.json'
path_font = 'fonts/main_font.otf'

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
# id игрока
player_id = 'user_vasiliy'
# ссылка на сервер
url_server = 'http://127.0.0.1:1000/'
# пользователь вошел в игру
player_logged = False

# Создание блоков игрока
create_blocks(list_blocks_player, border_x=border, border_y=shift_along_axis_y)
# Создание блоков врага
create_blocks(list_blocks_enemy, border_x=distance_between_maps + width, border_y=shift_along_axis_y)
list_json_player = open_json(path_json_player)['description']
conversion_blocks(list_blocks_player, list_json_player)
runner = True

# Регистрация игрока на сервере
login_player = ServerThread(method_name='login_player', method_finished=player_entered)
login_player.start()

# Запуск игры
while runner:
    clock.tick(FPS)

    if player_logged:
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

        elif event.type == pygame.MOUSEBUTTONUP:
            pass

    pygame.display.flip()
    surface.fill(WHITE)
pygame.quit()
