import pygame
import json
from enum import Enum


# Состояние блока
class ConditionBlock(Enum):
    Empty = 0
    Filled = 1
    Selected = 2
    Miss = 3
    Lock = 4


# Класс точки, которая хранит x и y
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


# Класс Block
class Block:
    def __init__(self, x, y, block_size, color_default, color_select, color_lock, color_miss):
        self.pos_x = x * block_size
        self.pos_y = y * block_size
        self.size_block = block_size
        self.number_block = (x, y)

        self.pos_left_up = Point(self.pos_x, self.pos_y)
        self.pos_right_up = Point(self.pos_x + block_size, self.pos_y)
        self.pos_left_down = Point(self.pos_x, self.pos_y + block_size)
        self.pos_right_down = Point(self.pos_x + block_size, self.pos_y + block_size)

        self.color_default = color_default
        self.color_select = color_select
        self.color_lock = color_lock
        self.color_miss = color_miss

        self.color_selected = self.color_default

        self.list_main_blocks = []
        self.rect = pygame.Rect(self.pos_x, self.pos_y, self.size_block, self.size_block)
        self.condition_block = ConditionBlock.Empty

    # Смена состояния блока
    def __change_condition_color(self, new_condition, new_color):
        self.condition_block = new_condition
        self.color_selected = new_color

    # Смена блока на блокированный
    def change_to_lock(self, lock=False):
        if lock:
            self.condition_block = ConditionBlock.Lock
        self.color_selected = self.color_lock

    # Смена блока на пустой
    def change_to_empty(self):
        self.__change_condition_color(ConditionBlock.Empty, self.color_default)

    # Смена блока на выбранный
    def change_to_selected(self):
        self.__change_condition_color(ConditionBlock.Selected, self.color_select)

    # Смена блока на промах
    def change_to_miss(self):
        self.__change_condition_color(ConditionBlock.Miss, self.color_miss)

    # Отрисовка блока
    def draw_block(self):
        pygame.draw.rect(surface, self.color_selected, (self.pos_x, self.pos_y, self.size_block, self.size_block))

    # Проверка нажатия на блок
    def check_input_button(self, mouse):
        if self.rect.topleft[0] < mouse[0] < self.rect.bottomright[0] and self.rect.topleft[1] < mouse[1] < \
                self.rect.bottomright[1]:
            return True
        return False


# Класс корабля
class Ship:
    def __init__(self, list_blocks_ship):
        self.len_ship = len(list_blocks_ship)
        self.list_blocks_ship = list_blocks_ship


# Смегна блока
def change_block(block):
    block.change_to_selected()

    if block.condition_block == ConditionBlock.Selected:
        list_blocks_selected.append(block)
    elif block.condition_block == ConditionBlock.Empty:
        list_blocks_selected.remove(block)
        list_blocks_remove_selected.append(block)

    if len(list_blocks_remove_selected) > 0:
        for block_remove_selected in list_blocks_remove_selected:
            dict_blocks_corners_cross = get_blocks_nearby_cross_and_corners(block_remove_selected)
            for block_nearby in dict_blocks_corners_cross['corners'] + dict_blocks_corners_cross['cross']:
                block_nearby.change_to_empty()
        list_blocks_remove_selected.clear()

    for block_selected in list_blocks_selected:
        dict_blocks_corners_cross = get_blocks_nearby_cross_and_corners(block_selected)
        for block_nearby_corners in dict_blocks_corners_cross['corners']:
            block_nearby_corners.change_to_lock(lock=True)
        for block_nearby_cross in dict_blocks_corners_cross['cross']:
            block_nearby_cross.change_to_lock()


# Получение блоков рядом
def get_blocks_nearby(select_block, condition='corners'):
    x, y = select_block.number_block
    if condition == 'corners':
        list_positions_blocks = [(x - 1, y - 1), (x - 1, y + 1), (x + 1, y - 1), (x + 1, y + 1)]
    else:
        list_positions_blocks = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    return [block for block in list_blocks if block.number_block in list_positions_blocks]


# Возвращает блоки вокруг блока
def get_blocks_nearby_cross_and_corners(block):
    blocks_nearby_corners = get_blocks_nearby(block, condition='corners')
    blocks_nearby_cross = list(filter(lambda b: b.condition_block != ConditionBlock.Selected,
                                      get_blocks_nearby(block, condition='cross')))
    return {'corners': blocks_nearby_corners, 'cross': blocks_nearby_cross}


# Поиск кораблей
def search_nearest_blocks(start_block, list_block_passed):
    list_block_passed.append(start_block)
    blocks_nearby_cross = get_blocks_nearby(start_block, condition='cross')
    for block in blocks_nearby_cross:
        if block.condition_block == ConditionBlock.Filled and block != start_block and block not in list_block_passed:
            search_nearest_blocks(block, list_block_passed)
    return list_block_passed


# Рисование карты
def draw_map(first_draw=False):
    global number_destroyed_ships
    number_destroyed_ships = 0
    pos = 0

    for ship in list_ships:
        if ship.len_ship == len(list(filter(lambda block: block.condition_block == ConditionBlock.Selected, ship.list_blocks_ship))):
            number_destroyed_ships += 1
            for block in ship.list_blocks_ship:
                change_block(block)

    for block in list_blocks:
        block.draw_block()

    for line in range(number_blocks + 1):
        pygame.draw.line(surface, BLACK, (0, pos), (height, pos), distance_between_blocks)
        pygame.draw.line(surface, BLACK, (pos, 0), (pos, height), distance_between_blocks)
        pos += block_size

    if first_draw:
        for y in range(number_blocks):
            for x in range(number_blocks):
                new_block = Block(x=x, y=y, block_size=block_size, color_select=BLACK, color_default=WHITE,
                                  color_lock=RED, color_miss=BLUE_AZURE)
                list_blocks.append(new_block)


# Проверяем на какой блок нажала мышь
def check_input_block(pos_mouse):
    for block in list_blocks:
        if block.check_input_button(pos_mouse) and block.condition_block != ConditionBlock.Lock and \
                block.condition_block != ConditionBlock.Miss:
            if block.condition_block == ConditionBlock.Filled:
                block.change_to_selected()
            elif block.condition_block == ConditionBlock.Empty:
                block.change_to_miss()
            break


# Проверка того, что блок есть в каком либо корабле
def check_block_ship(block):
    for ship in list_ships:
        if block in ship.list_blocks_ship:
            return True
    return False


# Создание блоков на основе json файла
def conversion_blocks():
    for block in list_blocks:
        x, y = block.number_block
        if list_ships_map[y][x] == '1':
            block.condition_block = ConditionBlock.Filled
        else:
            block.condition_block = ConditionBlock.Empty


# Открытие json файла
def open_json() -> dict:
    with open(path_save_map, 'r', encoding='utf-8') as read_file:
        data = json.load(read_file)
    return data


# Основные переменные
# Высота и ширина
height = width = 500
# Кол-во FPS
FPS = 60
# Кол-во блоков
number_blocks = 10
# Размер одного блока
block_size = height // number_blocks
# Расстояние между двумя блоками
distance_between_blocks = 2
# Список блоков
list_blocks = []
# Спиок кораблей
list_ships = []
# Список выбранных кораблей
list_blocks_selected = []
# Список удаленных кораблей
list_blocks_remove_selected = []
# Путь до папки с сохранением карты
path_save_map = 'static/map_player.json'
# Карта в виде списка
list_ships_map = open_json()['description']
# Кол-во уничтоженных кораблей
number_destroyed_ships = 0

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE_AZURE = (42, 82, 190)
GREEN = (0, 128, 0)

# Инициализация игры
pygame.init()
pygame.font.init()
surface = pygame.display.set_mode((width, height), 0, 32)
clock = pygame.time.Clock()
pygame.display.set_caption('Sea Battle')
surface.fill(WHITE)
draw_map(first_draw=True)
runner = True
# Преобразовать блоки
conversion_blocks()
# Поиск кораблей
for block in list_blocks:
    if block.condition_block == ConditionBlock.Filled and not check_block_ship(block):
        new_ship = Ship(search_nearest_blocks(block, []))
        list_ships.append(new_ship)

# Запуск игры
while runner:
    clock.tick(FPS)

    if number_destroyed_ships == 10:
        print('Вы выиграли')

    # Рисование карты
    draw_map()
    # Проверка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runner = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                check_input_block(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                pass

    pygame.display.flip()
    surface.fill(WHITE)
pygame.quit()
