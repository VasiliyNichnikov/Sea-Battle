import pygame


# Класс точки
class Point:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y


# класс блока
class Block:
    def __init__(self, x, y, size_block, color_select, color_empty):
        self.pos_x = x * size_block
        self.pos_y = y * size_block
        self.size_block = size_block
        self.number_block = (x, y)

        self.pos_left_up = Point(self.pos_x, self.pos_y)
        self.pos_right_up = Point(self.pos_x + size_block, self.pos_y)
        self.pos_left_down = Point(self.pos_x, self.pos_y + size_block)
        self.pos_right_down = Point(self.pos_x + size_block, self.pos_y + size_block)

        self.color_select = color_select
        self.color_empty = color_empty
        self.color_selected = color_empty

    def draw_block(self):
        pygame.draw.rect(surface, self.color_selected, (self.pos_x, self.pos_y, self.size_block, self.size_block))


# цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


# основные значения переменных
height, width = 500, 500
FPS = 60
number_blocks = 10
distance_between_blocks = 2
block_size = height // 10
list_blocks = []


# проверка нажатия
def check_input_mouse(pos_mouse):
    pos_mouse_x, pos_mouse_y = pos_mouse

    for block in list_blocks:
        pos_left_up_y = block.pos_left_up.get_y()
        pos_right_down_y = block.pos_right_down.get_y()

        pos_left_down_x = block.pos_left_down.get_x()
        pos_right_down_x = block.pos_right_down.get_x()
        if pos_left_down_x < pos_mouse_x < pos_right_down_x and pos_left_up_y < pos_mouse_y < pos_right_down_y:
            block.color_selected = block.color_select
            block.draw_block()


# рисование карты
def draw_map(first_draw=False):
    pos = 0
    for line in range(number_blocks):
        pygame.draw.line(surface, BLACK, (0, pos), (height, pos), distance_between_blocks)
        pygame.draw.line(surface, BLACK, (pos, 0), (pos, height), distance_between_blocks)
        pos += block_size

    if first_draw:
        for y in range(number_blocks):
            for x in range(number_blocks):
                new_block = Block(x=x, y=y, size_block=block_size, color_select=BLACK, color_empty=WHITE)
                list_blocks.append(new_block)


# инициализация игры
pygame.init()
surface = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
pygame.display.set_caption('Sea Battle')
runner = True

surface.fill(WHITE)
draw_map(first_draw=True)
pygame.display.flip()

# запуск игры
while runner:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runner = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                check_input_mouse(event.pos)
                draw_map()

    # surface.fill(WHITE)
    pygame.display.flip()

pygame.quit()
