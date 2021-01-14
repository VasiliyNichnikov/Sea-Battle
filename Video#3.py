import pygame
from enum import Enum


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class ConditionBlock(Enum):
    Empty = 0
    Selected = 1
    Lock = 2


# Класс Block, который работает с каждым блоком
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

        self.list_main_blocks = []  # new
        self.condition_block = ConditionBlock.Empty  # new

    # Смена блока на заблокированный
    def change_to_lock(self):
        self.condition_block = ConditionBlock.Lock
        self.color_selected = self.color_lock
        self.draw_block()

    # Смена блока на пустой
    def change_to_empty(self):
        self.condition_block = ConditionBlock.Empty
        self.color_selected = self.color_default
        self.draw_block()

    # Смена блока на выбранный
    def change_to_selected(self):
        if self.condition_block == ConditionBlock.Empty:
            self.condition_block = ConditionBlock.Selected
            self.color_selected = self.color_select

        else:
            self.condition_block = ConditionBlock.Empty
            self.color_selected = self.color_default
        self.draw_block()

    # Рисование блока
    def draw_block(self):
        pygame.draw.rect(surface, self.color_selected, (self.pos_x, self.pos_y, self.size_block, self.size_block))


# Проверяем на какой блок нажала мышь
def check_input_mouse(pos_mouse):
    pos_mouse_x, pos_mouse_y = pos_mouse

    for block in list_blocks:
        pos_left_up_y = block.pos_left_up.y
        pos_right_down_y = block.pos_right_down.y

        pos_left_down_x = block.pos_left_down.x
        pos_right_down_x = block.pos_right_down.x

        if pos_left_down_x < pos_mouse_x < pos_right_down_x and pos_left_up_y < pos_mouse_y < pos_right_down_y \
                and block.condition_block != ConditionBlock.Lock:  # new
            block.change_to_selected()  # new

            for block_nearby in get_blocks_nearby(block):
                if block.condition_block == ConditionBlock.Selected:
                    block_nearby.list_main_blocks.append(block)
                    block_nearby.change_to_lock()
                elif block.condition_block == ConditionBlock.Empty:
                    block_nearby.list_main_blocks.remove(block)
                    if len(block_nearby.list_main_blocks) == 0:
                        block_nearby.change_to_empty()
            break  # new


# Получение блоков поблизости
def get_blocks_nearby(select_block):
    x, y = select_block.number_block
    list_positions_blocks = [(x - 1, y - 1), (x - 1, y + 1), (x + 1, y - 1), (x + 1, y + 1)]
    list_ready_blocks = []
    for block in list_blocks:
        if block.number_block in list_positions_blocks:
            list_ready_blocks.append(block)
    return list_ready_blocks


# Рисование карты
def draw_map(first_draw=False):
    pos = 0

    for line in range(number_blocks):
        pygame.draw.line(surface, BLACK, (0, pos), (height, pos), distance_between_blocks)
        pygame.draw.line(surface, BLACK, (pos, 0), (pos, height), distance_between_blocks)
        pos += block_size

    if first_draw:
        for y in range(number_blocks):
            for x in range(number_blocks):
                new_block = Block(x=x, y=y, block_size=block_size,
                                  color_select=BLACK,
                                  color_default=WHITE,
                                  color_lock=RED)
                list_blocks.append(new_block)


# Основные переменные
height = width = 500
FPS = 60
number_blocks = 10
block_size = height // number_blocks
distance_between_blocks = 2
list_blocks = []

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 5, 5)  # new

# Инициализация игры
pygame.init()
surface = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
pygame.display.set_caption('Sea Battle')
surface.fill(WHITE)
draw_map(first_draw=True)
runner = True

# Запуск игры
while runner:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runner = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                check_input_mouse(event.pos)
                draw_map()

    pygame.display.flip()

pygame.quit()
