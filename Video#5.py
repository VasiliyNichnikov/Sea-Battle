import pygame
import json
from enum import Enum


class ConditionBlock(Enum):
    Empty = 0
    Selected = 1
    Lock = 2


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


# Класс точки, который создает и отрисовывает точку, а также проверяет ее нажати
class Button:
    # Инициалиация параметров кнопки
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

    # Отрисовка кнопки
    def draw_button(self):
        if self.input_btn:
            pygame.draw.rect(self.surface, self.color_btn, (self.pos_x, self.pos_y, self.width, self.height))
        else:
            pygame.draw.rect(self.surface, self.color_btn, (self.pos_x, self.pos_y, self.width, self.height), 2)
        text_btn = self.__draw_text()
        surface.blit(text_btn, (
            self.pos_x + (self.width - text_btn.get_width()) // 2,
            self.pos_y + (self.height - text_btn.get_height()) // 2))

    # Проверка нажатия на кнопку
    def check_input_button(self, mouse, click=False):
        if self.rect.topleft[0] < mouse[0] < self.rect.bottomright[0] \
                and self.rect.topleft[1] < mouse[1] < self.rect.bottomright[1] and click:
            self.input_btn = True
        else:
            self.input_btn = False
        return self.input_btn

    # Рисует текст на кнопки
    def __draw_text(self):
        font = pygame.font.Font(self.path_font, self.size_font)
        text = font.render(self.text, True, self.color_text)
        return text


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
        self.condition_block = ConditionBlock.Empty

    def __change_condition_color(self, new_condition, new_color):
        self.condition_block = new_condition
        self.color_selected = new_color

    def change_to_lock(self, lock=False):
        if lock:
            self.condition_block = ConditionBlock.Lock
        self.color_selected = self.color_lock

    def change_to_empty(self):
        self.__change_condition_color(ConditionBlock.Empty, self.color_default)

    def test_color(self):
        self.__change_condition_color(ConditionBlock.Selected, (255, 255, 0))

    def change_to_selected(self):
        if self.condition_block == ConditionBlock.Empty:
            self.__change_condition_color(ConditionBlock.Selected, self.color_select)
        else:
            self.__change_condition_color(ConditionBlock.Empty, self.color_default)

    def draw_block(self):
        pygame.draw.rect(surface, self.color_selected, (self.pos_x, self.pos_y, self.size_block, self.size_block))


# Класс корабля
class Ship:
    def __init__(self, list_blocks_ship):
        self.len_ship = len(list_blocks_ship)
        self.list_blocks_ship = list_blocks_ship


# Работа с блоками
def change_block_to_selected(block):
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


# Проверяем на какой блок нажала мышь
def check_input_mouse(pos_mouse):
    global end_input_mouse_block
    pos_mouse_x, pos_mouse_y = pos_mouse

    for block in list_blocks:
        pos_left_up_y = block.pos_left_up.y
        pos_right_down_y = block.pos_right_down.y

        pos_left_down_x = block.pos_left_down.x
        pos_right_down_x = block.pos_right_down.x

        if pos_left_down_x < pos_mouse_x < pos_right_down_x and pos_left_up_y < pos_mouse_y < pos_right_down_y and \
                block.condition_block != ConditionBlock.Lock:
            end_input_mouse_block = block
            change_block_to_selected(block)
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
                new_ship = Ship(search_nearest_blocks(block, 1, []))
                if new_ship.len_ship > 4:
                    change_block_to_selected(end_input_mouse_block)
                list_ships.append(new_ship)

    if first_draw:
        for y in range(number_blocks):
            for x in range(number_blocks):
                new_block = Block(x=x, y=y, block_size=block_size, color_select=BLACK, color_default=WHITE,
                                  color_lock=RED)
                list_blocks.append(new_block)


# Рисование лимита кораблей
def draw_limit_ship(size_text_ships):
    # Словарь с кораблями
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
        title = f'x{dict_number_ships[i]}'
        # Меняем цвет в зависимости от кол-ва кораблей
        color = BLACK
        if dict_number_ships[i] < 0:
            color = RED
        elif dict_number_ships[i] == 0:
            color = GREEN
        pygame.draw.rect(surface, color, (width + border, pos_y, block_size * i, block_size), 2)
        text = add_text(title, 35, color, True, path_font)
        text_adding_axes_y = ((pos_y + block_size) - (pos_y + text.get_height())) // 2
        surface.blit(text,
                     ((width + border + block_size * i // 2) - text.get_width() // 2, pos_y + text_adding_axes_y))
        pos_y += block_size + border


# Добавление текста в игру
def add_text(text, size_font, color, anti_aliasing=False, path='None'):
    font = pygame.font.Font(path, size_font)
    text = font.render(text, anti_aliasing, color)
    return text


# Сохранение карты в файл
def save_map():
    with open(path_save_map + 'map.json', 'w') as json_write:
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


# Основные переменные
additional_area_width = 250
height = width = 500
FPS = 60
number_blocks = 10
block_size = height // number_blocks
distance_between_blocks = 2
list_blocks = []
# Путь до папки с сохранением
path_save_map = 'static/'
# Список кораблей
list_ships = []
# Путь до шрифта
path_font = 'Fonts/main_font.otf'
# Последний нажатый блок
end_input_mouse_block = None

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE_AZURE = (42, 82, 190)
GREEN = (0, 128, 0)

# Инициализация игры
pygame.init()
pygame.font.init()
surface = pygame.display.set_mode((width + additional_area_width, height), 0, 32)
clock = pygame.time.Clock()
pygame.display.set_caption('Sea Battle')
surface.fill(WHITE)
draw_map(first_draw=True)
runner = True

# Инициализация кнопки
button_save = Button(surface, width + (additional_area_width - block_size * 4) // 2,
                     height - block_size - 10,
                     block_size, block_size * 4, BLACK, 'СОХРАНИТЬ', BLUE_AZURE, path_font, 30)

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
    # Отрисовка кнопки
    button_save.draw_button()

    # Проверка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runner = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                check_input_mouse(event.pos)
                # Обновляем текст по кол-ву кораблей
                draw_limit_ship(text_ships.get_height())
                if button_save.check_input_button(event.pos, True):
                    save_map()
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                button_save.check_input_button(event.pos)

    pygame.display.flip()
    surface.fill(WHITE)
pygame.quit()
