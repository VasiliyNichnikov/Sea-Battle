import pygame
import json
from enum import Enum

"""
    Видеоурок №8. Создание самой игры. Ход игрока.
"""


class ConditionBlock(Enum):
    Empty = 0
    Selected = 1
    Lock = 2
    Miss = 3
    Hit = 4
    Hide_Selected = 5


# Выбранная карта у игрока
class ConditionMotion(Enum):
    Player = 0
    Enemy = 1


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


# Класс кораблей
class Ship:
    def __init__(self, list_blocks_ship):
        self.len_ship = len(list_blocks_ship)
        self.list_blocks_ship = list_blocks_ship
        self.ship_sank = False

        for block in self.list_blocks_ship:
            block.len_ship = self.len_ship

    # Проверяет, потонул корабль или нет
    def check_sank_ship(self):
        number_selected_blocks = 0
        for block in self.list_blocks_ship:
            if block.condition_block == ConditionBlock.Selected:
                number_selected_blocks += 1
        return len(self.list_blocks_ship) == number_selected_blocks


# Класс блока
class Block:
    def __init__(self, x, y, block_size, border_x, border_y, color_default, color_select, color_lock, color_miss,
                 color_hit):
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
        self.color_miss = color_miss
        self.color_hit = color_hit

        self.color_selected = self.color_default

        self.condition_block = ConditionBlock.Empty

    def __change_condition_color(self, new_condition, new_color):
        self.condition_block = new_condition
        self.color_selected = new_color

    def change_to_empty(self):
        self.__change_condition_color(ConditionBlock.Empty, self.color_default)

    def change_to_selected(self):
        self.__change_condition_color(ConditionBlock.Selected, self.color_select)

    def change_to_hide_selected(self):
        self.__change_condition_color(ConditionBlock.Hide_Selected, self.color_default)

    def change_to_miss(self):
        self.__change_condition_color(ConditionBlock.Miss, self.color_miss)

    def change_to_lock(self):
        self.__change_condition_color(ConditionBlock.Lock, self.color_lock)

    def change_to_hit(self):
        self.__change_condition_color(ConditionBlock.Hit, self.color_hit)

    def draw_block(self):
        pygame.draw.rect(surface, self.color_selected, (self.pos_x, self.pos_y, self.size_block, self.size_block))


# Класс карты
class Map:
    def __init__(self, name_map, list_blocks_map):
        self.name_map = name_map
        self.list_blocks_map = list_blocks_map

    def check_belongs_block_map(self, block):
        return block in self.list_blocks_map


# Смена блока
def change_block(block):
    if block.condition_block == ConditionBlock.Hide_Selected:
        list_blocks_selected.append(block)
        block.change_to_selected()
    elif block.condition_block == ConditionBlock.Empty:
        block.change_to_miss()
        change_motion()

    # Отрисовка кораблей, когда весь корабль уничтожен
    select_ship = get_ship_class(block)
    if select_ship is not None and not select_ship.ship_sank and select_ship.check_sank_ship():
        select_ship.ship_sank = True

        for block_ship in select_ship.list_blocks_ship:
            dict_blocks_corners_cross = get_blocks_nearby_cross_and_corners(block_ship)
            for block_nearby_corners in dict_blocks_corners_cross['corners'] + dict_blocks_corners_cross['cross']:
                block_nearby_corners.change_to_lock()


# Проверяем на какой блок нажала мышь
def check_input_mouse(pos_mouse):
    pos_mouse_x, pos_mouse_y = pos_mouse

    for block in list_blocks_select:
        pos_left_up_y = block.pos_left_up.y
        pos_right_down_y = block.pos_right_down.y

        pos_left_down_x = block.pos_left_down.x
        pos_right_down_x = block.pos_right_down.x

        if pos_left_down_x < pos_mouse_x < pos_right_down_x and pos_left_up_y < pos_mouse_y < pos_right_down_y and \
                not map_player.check_belongs_block_map(block):
            change_block(block)
            break


# Возвращает блоки вокруг блока
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
    return [block for block in list_blocks_select if block.number_block in list_positions_blocks]


# Поиск ближайших блоков, которые создают корабли
def search_nearest_blocks(start_block, list_block_passed, condition_block=ConditionBlock.Hide_Selected):
    list_block_passed.append(start_block)
    block_nearby_cross = get_blocks_nearby(start_block, condition='cross')
    for block in block_nearby_cross:
        if block.condition_block == condition_block and block != start_block and block not in list_block_passed:
            search_nearest_blocks(block, list_block_passed, condition_block)
    return list_block_passed


# Проверка, принадлежит ли блок одному из кораблей
def check_block_ship(block):
    for ship in list_select_ships:
        if block in ship.list_blocks_ship:
            return True
    return False


# Получение класса корабля
def get_ship_class(block):
    for ship in list_select_ships:
        if block in ship.list_blocks_ship:
            return ship
    return None


# Получение текста
def get_text(text, size_font, color, anti_aliasing=False, path='None'):
    font = pygame.font.Font(path, size_font)
    text = font.render(text, anti_aliasing, color)
    return text


# Конвертирование блоков из json в классы
def conversion_blocks(list_blocks, list_ships_map, condition_motion=ConditionMotion.Player):
    for block in list_blocks:
        x, y = block.number_block
        if list_ships_map[y][x] == '1':
            if condition_motion == ConditionMotion.Player:
                block.change_to_selected()
            else:
                block.change_to_hide_selected()
        else:
            block.change_to_empty()


# Открытие json файла
def open_json(path_save_map) -> dict:
    with open(path_save_map, 'r', encoding='utf-8') as read_file:
        data = json.load(read_file)
    return data


# Создание классов Block
def create_blocks(list_blocks, border_x=0, border_y=0):
    for y in range(number_blocks):
        for x in range(number_blocks):
            new_block = Block(x=x, y=y,
                              border_x=border_x,
                              border_y=border_y,
                              block_size=block_size,
                              color_select=BLACK,
                              color_default=WHITE,
                              color_lock=RED,
                              color_hit=YELLOW,
                              color_miss=BLUE_AZURE)
            list_blocks.append(new_block)


# Рисование карты игрока и противника
def draw_map():
    for block in list_blocks_player + list_blocks_enemy:
        block.draw_block()

    # Отрисовка карты игрока
    pos = block_size
    for line in range(number_blocks - 1):
        pygame.draw.line(surface, BLACK, (border, pos + shift_along_axis_y),
                         (height + border, pos + shift_along_axis_y),
                         distance_between_blocks)
        pygame.draw.line(surface, BLACK, (pos + border, shift_along_axis_y),
                         (pos + border, height + shift_along_axis_y),
                         distance_between_blocks)
        pos += block_size

    # Отрисовка карты противника
    pos = block_size
    for line in range(number_blocks - 1):
        pygame.draw.line(surface, BLACK,
                         (distance_between_maps + width, pos + shift_along_axis_y),
                         (distance_between_maps + width * 2, pos + shift_along_axis_y),
                         distance_between_blocks)
        pygame.draw.line(surface, BLACK,
                         (distance_between_maps + width + pos, shift_along_axis_y),
                         (distance_between_maps + width + pos, shift_along_axis_y + height),
                         distance_between_blocks)
        pos += block_size

    if condition_motion == ConditionMotion.Player:
        color_player, color_enemy = GREEN, BLACK
    else:
        color_player, color_enemy = BLACK, RED

    # Выделение карты игрока
    pygame.draw.rect(surface, color_player, (border, shift_along_axis_y, height, width), distance_between_blocks * 2)
    # Выделение карты противника
    pygame.draw.rect(surface, color_enemy, (width + distance_between_maps, shift_along_axis_y, width, height),
                     distance_between_blocks * 2)


# Смена карты
def change_motion():
    global condition_motion, list_blocks_select
    if condition_motion == ConditionMotion.Enemy:
        condition_motion = ConditionMotion.Player
        list_blocks_select = list_blocks_player
    else:
        condition_motion = ConditionMotion.Enemy
        list_blocks_select = list_blocks_enemy


# Основные переменные
height = width = 500
# Расстояние между картами
distance_between_maps = 40
# Сдвиг по оси Y
shift_along_axis_y = 50
# Обводка
border = 5
FPS = 60
number_blocks = 10
block_size = height // number_blocks
distance_between_blocks = 2
# Состоянеи карты
condition_motion = ConditionMotion.Player
# Список блоков игрока
list_blocks_player = []
# Список блоков врага
list_blocks_enemy = []
# Путь до json файла игрока
path_save_player_map = 'static/map_player.json'
# Путь до json файла противника
path_save_enemy_map = 'static/map_enemy.json'
# Список кораблей
list_ships_enemy = []

# Список выбранных блоков
list_blocks_selected = []
path_font = 'fonts/main_font.otf'

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE_AZURE = (42, 82, 190)
GREEN = (0, 128, 0)
YELLOW = (255, 204, 0)

# Инициализация игры
pygame.init()
surface = pygame.display.set_mode((width * 2 + distance_between_maps + border, height + shift_along_axis_y + border))
clock = pygame.time.Clock()
pygame.display.set_caption('Sea Battle')
surface.fill(WHITE)
runner = True
# Список кораблей на карте
list_ships_player_map = open_json(path_save_player_map)['description']
# Список кораблей на карте врага
list_ships_enemy_map = open_json(path_save_enemy_map)['description']

# Создание блоков игрока
create_blocks(list_blocks_player, border_x=border, border_y=shift_along_axis_y)
# Создание блоков противника
create_blocks(list_blocks_enemy, border_x=distance_between_maps + width, border_y=shift_along_axis_y)

# Создание классов карты
map_player = Map(name_map='player', list_blocks_map=list_blocks_player)
map_enemy = Map(name_map='enemy', list_blocks_map=list_blocks_enemy)

# Преобразование блоков игрока
conversion_blocks(list_blocks_player, list_ships_player_map, condition_motion=ConditionMotion.Player)
# # Преобразование блоков противника
conversion_blocks(list_blocks_enemy, list_ships_enemy_map, condition_motion=ConditionMotion.Enemy)
# Выбранный список блоков
list_blocks_select = list_blocks_enemy

# Выбранный список кораблей
list_select_ships = list_ships_enemy

# Нахождение кораблей врага
for block in list_blocks_select:
    if block.condition_block == ConditionBlock.Hide_Selected and not check_block_ship(block):
        new_ship = Ship(search_nearest_blocks(block, []))
        list_ships_enemy.append(new_ship)

# Запуск игры
while runner:
    clock.tick(FPS)
    draw_map()

    # Отрисовка текста над картой игрока
    text_player = get_text('VASILIY', 40, BLUE_AZURE, True, path_font)
    surface.blit(text_player, (border + width // 2 - text_player.get_width() // 2,
                               shift_along_axis_y // 2 - text_player.get_height() // 2 + border))
    # Отрисовка текста над картой врага
    text_enemy = get_text('ENEMY_251', 40, RED, True, path_font)
    surface.blit(text_enemy, (border + width // 2 - text_enemy.get_width() // 2 + width + distance_between_maps,
                              shift_along_axis_y // 2 - text_enemy.get_height() // 2 + border))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runner = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and condition_motion == ConditionMotion.Player:
                check_input_mouse(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            pass

    pygame.display.flip()
    surface.fill(WHITE)
pygame.quit()
