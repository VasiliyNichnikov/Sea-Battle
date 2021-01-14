import pygame
from enum import Enum


class ConditionBlock(Enum):
    Empty = 0
    Selected = 1
    Lock = 2


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Block:
    def __init__(self, x, y, block_size, color_default, color_select, color_lock):
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

        self.color_selected = self.color_default

        self.list_main_blocks = []
        # self.main_block_ship = None
        self.condition_block = ConditionBlock.Empty

    def __change_condition_color(self, new_condition, new_color):
        self.condition_block = new_condition
        self.color_selected = new_color
        # self.draw_block()

    def change_to_lock(self, lock=False):
        if lock:
            self.condition_block = ConditionBlock.Lock
        self.color_selected = self.color_lock
        # self.draw_block()

    def change_to_empty(self):
        self.__change_condition_color(ConditionBlock.Empty, self.color_default)

    def test_color(self):
        self.__change_condition_color(ConditionBlock.Selected, (255, 255, 0))

    def change_to_selected(self):
        if self.condition_block == ConditionBlock.Empty:
            # self.main_block_ship = self
            self.__change_condition_color(ConditionBlock.Selected, self.color_select)
        else:
            # self.main_block_ship = None
            self.__change_condition_color(ConditionBlock.Empty, self.color_default)

    def draw_block(self):
        pygame.draw.rect(surface, self.color_selected, (self.pos_x, self.pos_y, self.size_block, self.size_block))


# Класс корабля
class Ship:
    def __init__(self, list_blocks_ship):
        self.len_ship = len(list_blocks_ship)
        self.list_blocks_ship = list_blocks_ship


# Проверяем на какой блок нажала мышь
def check_input_mouse(pos_mouse):
    pos_mouse_x, pos_mouse_y = pos_mouse

    for block in list_blocks:
        pos_left_up_y = block.pos_left_up.y
        pos_right_down_y = block.pos_right_down.y

        pos_left_down_x = block.pos_left_down.x
        pos_right_down_x = block.pos_right_down.x

        if pos_left_down_x < pos_mouse_x < pos_right_down_x and pos_left_up_y < pos_mouse_y < pos_right_down_y and \
                block.condition_block != ConditionBlock.Lock:
            block.change_to_selected()

            for block_nearby_corners in get_blocks_nearby(block, condition='corners'):
                if block.condition_block == ConditionBlock.Selected:
                    block_nearby_corners.list_main_blocks.append(block)
                    block_nearby_corners.change_to_lock(lock=True)
                elif block.condition_block == ConditionBlock.Empty:
                    block_nearby_corners.list_main_blocks.remove(block)
                    if len(block_nearby_corners.list_main_blocks) == 0:
                        block_nearby_corners.change_to_empty()

            for block_nearby_cross in get_blocks_nearby(block, condition='cross'):
                if block.condition_block == ConditionBlock.Selected:
                    block_nearby_cross.list_main_blocks.append(block)
                    if block_nearby_cross.condition_block != ConditionBlock.Selected:
                        block_nearby_cross.change_to_lock()

                elif block.condition_block == ConditionBlock.Empty:
                    block_nearby_cross.list_main_blocks.remove(block)
                    if len(block_nearby_cross.list_main_blocks) == 0 \
                            and block_nearby_cross.condition_block != ConditionBlock.Selected:
                        block_nearby_cross.change_to_empty()
                    elif block_nearby_cross.condition_block == ConditionBlock.Selected:
                        block.change_to_lock()

            break


# Получение угловых блоков
def get_blocks_nearby(select_block, condition='corners'):
    x, y = select_block.number_block
    if condition == 'corners':
        list_positions_blocks = [(x - 1, y - 1), (x - 1, y + 1), (x + 1, y - 1), (x + 1, y + 1)]
    else:
        list_positions_blocks = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    return [block for block in list_blocks if block.number_block in list_positions_blocks]


# Поиск ближайших блоков
def search_nearest_blocks(start_block, number, list_block_passed):
    list_block_passed.append(start_block)
    blocks_nearby_cross = get_blocks_nearby(start_block, condition='cross')
    for block in blocks_nearby_cross:
        if block.condition_block == ConditionBlock.Selected and block != start_block and block not in list_block_passed:
            search_nearest_blocks(block, number, list_block_passed)
    return list_block_passed


# Проверка того, что блок есть в каком либо корабле
def check_block_ship(block):
    for ship in list_ships:
        if block in ship.list_blocks_ship:
            return True
    return False


# Рисование карты
def draw_map(first_draw=False):
    pos = 0

    for block in list_blocks:
        block.draw_block()

    for line in range(number_blocks + 1):
        pygame.draw.line(surface, BLACK, (0, pos), (height, pos), distance_between_blocks)
        pygame.draw.line(surface, BLACK, (pos, 0), (pos, height), distance_between_blocks)
        pos += block_size

    list_ships.clear()
    if len(list_blocks) != 0:
        for block in list_blocks:
            if block.condition_block == ConditionBlock.Selected and not check_block_ship(block):
                list_ships.append(Ship(search_nearest_blocks(block, 1, [])))

    if first_draw:
        for y in range(number_blocks):
            for x in range(number_blocks):
                new_block = Block(x=x, y=y, block_size=block_size, color_select=BLACK, color_default=WHITE,
                                  color_lock=RED)
                list_blocks.append(new_block)


# Рисование лимита кораблей
def draw_limit_ship(size_text_ships):
    dict_number_ships = {
        1: 4,
        2: 3,
        3: 2,
        4: 1
    }

    for ship in list_ships:
        if ship.len_ship in dict_number_ships.keys():
            dict_number_ships[ship.len_ship] -= 1

    border = (additional_area_width - block_size * 4) // 2
    pos_y = size_text_ships + border
    for i in range(1, 5):
        pygame.draw.rect(surface, BLACK, (width + border, pos_y, block_size * i, block_size), 2)
        title = f'x{dict_number_ships[i]}'
        text = add_text(title, 35, BLACK, True, path_font)
        text_adding_axes_y = ((pos_y + block_size) - (pos_y + text.get_height())) // 2
        surface.blit(text,
                     ((width + border + block_size * i // 2) - text.get_width() // 2, pos_y + text_adding_axes_y))
        pos_y += block_size + border


# Добавление текста в игру
def add_text(text, size_font, color, anti_aliasing=False, path='None'):
    font = pygame.font.Font(path, size_font)
    text = font.render(text, anti_aliasing, color)
    return text


# Основные переменные
additional_area_width = 250
height = width = 500
FPS = 60
number_blocks = 10
block_size = height // number_blocks
distance_between_blocks = 2
list_blocks = []
# Список кораблей
list_ships = []
# Путь до шрифта
path_font = 'Fonts/main_font.otf'

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE_AZURE = (42, 82, 190)

# Инициализация игры
pygame.init()
pygame.font.init()
surface = pygame.display.set_mode((width + additional_area_width, height), 0, 32)
clock = pygame.time.Clock()
pygame.display.set_caption('Sea Battle')
surface.fill(WHITE)
draw_map(first_draw=True)
runner = True

# Запуск игры
while runner:
    clock.tick(FPS)

    # Рисование карты
    draw_map()
    # Рисование основных текстов
    text_ships = add_text('Корабли', 40, BLUE_AZURE, True, path_font)
    # Рисование текста "Корабли" в правой панели
    draw_limit_ship(text_ships.get_height())
    surface.blit(text_ships, (width + (additional_area_width - text_ships.get_width()) // 2, 10))
    # Обновляем текст по кол-ву кораблей
    draw_limit_ship(text_ships.get_height())
    # Проверка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runner = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                check_input_mouse(event.pos)

    pygame.display.flip()
    surface.fill(WHITE)
pygame.quit()
