from AllConditions import ConditionBlock, ConditionAxisShip, ConditionPlayerMap
from ImagesAndAnimations import AnimationWater, load_image
import pygame


# Класс служит вектором 2
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Block:
    """  Класс блока, используется для проверки, что в данный момент происходит с конкретным блоком """

    def __init__(self, surface, x, y, border_x, border_y, block_size) -> None:
        # Поле для отрисовки блока
        self.surface = surface
        # Позиция блока по оси X
        self.pos_x = x * block_size + border_x
        # Позиция блока по оси Y
        self.pos_y = y * block_size + border_y
        # Размер блока
        self.block_size = block_size
        # Номер блока
        self.number_block = (x, y)
        # Длина корабля в котором находится данный блок
        self.len_ship_which_block_located = 0
        # Класс корабля в котором находится блок
        self.ship_class = None

        # Блок является началом корабля
        self.block_start_ship = False

        # Блок является концом корабля
        self.block_end_ship = False

        # Ось блока
        self.axis_block = None

        # Крест первый
        self.sprite_cross_1 = load_image('../static/cross1.png', size_x=block_size, size_y=block_size)

        # Крест второй
        self.sprite_cross_2 = load_image('../static/cross2.png', size_x=block_size, size_y=block_size)

        # Круг промаха
        self.miss_circle = load_image('../static/miss_circle.png', size_x=block_size, size_y=block_size)

        # Блок одиночного корабля
        self.sprite_block_ship_1 = load_image('../static/ships/ship_1.png', size_x=block_size, size_y=block_size)
        # Верхняя часть корабля
        self.part_up_ships = load_image('../static/ships/part_up_ships.png', size_x=block_size, size_y=block_size)
        # Средняя часть корабля
        self.part_center_ships = load_image('../static/ships/part_center_ships.png', size_x=block_size,
                                            size_y=block_size)
        # Нижняя часть корабля
        self.part_down_ships = load_image('../static/ships/part_down_ships.png',
                                          size_x=block_size, size_y=block_size)

        # Позиция точек блока
        self.pos_left_up = Point(self.pos_x, self.pos_y)
        self.pos_right_up = Point(self.pos_x + block_size, self.pos_y)
        self.pos_left_down = Point(self.pos_x, self.pos_y + block_size)
        self.pos_right_down = Point(self.pos_x + block_size, self.pos_y + block_size)

        self.rect = pygame.Rect(self.pos_x, self.pos_y, self.block_size, self.block_size)

        # Создание класса анимации воды
        self.water_animation = AnimationWater(self.rect)

        # Группа спрайтов анимации воды
        self.group_sprites_water = pygame.sprite.Group(self.water_animation)

        # Состояние блока
        self.condition_block = ConditionBlock.Empty

    # Смена состояния блока
    def __change_condition_color(self, new_condition) -> None:
        self.condition_block = new_condition

    # Смена состояния блока на блокированное
    def change_to_lock(self, lock=False) -> None:
        if lock:
            self.condition_block = ConditionBlock.Lock

    # Смена состояния блока на пустое
    def change_to_empty(self) -> None:
        self.__change_condition_color(ConditionBlock.Empty)

    # Смена состояния блока на поврежденный
    def change_to_hit(self) -> None:
        self.__change_condition_color(ConditionBlock.Hit)

    # Смена состояния блока на промах
    def change_to_miss(self) -> None:
        self.__change_condition_color(ConditionBlock.Miss)

    # Смена состояния блока на выбранный
    def change_to_selected(self) -> None:
        self.__change_condition_color(ConditionBlock.Selected)

    # Проверка нажатия на блок
    def check_input_block(self, mouse) -> bool:
        if self.rect.topleft[0] < mouse[0] < self.rect.bottomright[0] and self.rect.topleft[1] < mouse[1] < \
                self.rect.bottomright[1]:
            return True
        return False

    # Отрисовка воды
    def draw_water(self) -> None:
        self.group_sprites_water.update()
        self.group_sprites_water.draw(self.surface)

    # Отрисовка спрайтов кораблей
    def draw_images_ships(self, condition_map):
        # Угол поворота блока
        angle = 90
        if self.axis_block == ConditionAxisShip.Vertical:
            angle = 0

        # Отрисовка кораблей
        # Отрисовка единичных кораблей
        if self.len_ship_which_block_located == 1:
            self.__draw_sprite_block(self.sprite_block_ship_1, position=self.rect, angle=angle)
        # Отрисовка кораблей больше 1
        elif self.len_ship_which_block_located > 1:
            if self.block_start_ship:
                self.__draw_sprite_block(self.part_up_ships, position=self.rect, angle=angle)
            elif self.block_end_ship:
                self.__draw_sprite_block(self.part_down_ships, position=self.rect, angle=angle)
            else:
                self.__draw_sprite_block(self.part_center_ships, position=self.rect, angle=angle)

        if self.condition_block == ConditionBlock.Hit or self.condition_block == ConditionBlock.Lock:
            if condition_map == ConditionPlayerMap.Player:
                self.__draw_sprite_block(self.sprite_cross_2, position=self.rect)
            else:
                self.__draw_sprite_block(self.sprite_cross_1, position=self.rect)
        elif self.condition_block == ConditionBlock.Miss:
            self.__draw_sprite_block(self.miss_circle, position=self.rect)

    # Отрисовка спрайта на блоке
    def __draw_sprite_block(self, sprite, position=(0, 0), angle=0) -> None:
        if angle != 0:
            sprite = pygame.transform.rotate(sprite, angle)
        self.surface.blit(sprite, position)

        # self.surface.blit(, self.rect)

        # if self.condition_block == ConditionBlock.Empty:
        #
        # else:
        # if self.condition_block != ConditionBlock.Empty:
        #     if self.len_ship_which_block_located == 1:
        #         self.surface.blit(self.sprite_ship_size_1, self.rect)
        #     else:
        #         pygame.draw.rect(self.surface, self.color_selected, self.rect)
        # self.surface.blit(self.water_sprite_1.get_image(), self.number_block)

    # Получение информации о блоке, для того, чтобы разукрасить
    # def get_info_draw_block(self):
    #     pass
    # return {'color_selected': self.color_selected, 'position': self.rect, 'number_block': self.number_block}

    # Проверка состояния блока
    def check_condition_block(self):
        function_block = {}
        # По блоку попали
        if self.condition_block == ConditionBlock.Selected:
            function_block = {'function': 'hit', 'next_motion': False}
            self.change_to_hit()
        # Промах
        elif self.condition_block == ConditionBlock.Empty:
            function_block = {'function': 'miss', 'next_motion': True}
            self.change_to_miss()
        return function_block
