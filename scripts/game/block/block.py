# from allConditions import ConditionBlock, ConditionAxisShip, ConditionPlayerMap
# from imagesAndAnimations import AnimationWater, load_image
import pygame
from pygame import Vector2, Surface
from scripts.game.block.parametersBlock import ParametersBlock


class Block:
    def __init__(self, surface: Surface, number_block: Vector2, border: Vector2, block_size) -> None:
        self.__parameters_block = ParametersBlock(surface, number_block, border, block_size)
        self.__position_block = self.__parameters_block.position_block
        self.__condition_block = self.__parameters_block.condition_block

    def check_input_block(self, mouse) -> bool:
        rect = self.__position_block.rect
        if rect.topleft[0] < mouse[0] < rect.bottomright[0] and rect.topleft[1] < mouse[1] < rect.bottomright[1]:
            return True
        return False

    # Отрисовка воды
    # def draw_water(self) -> None:
    #     self.group_sprites_water.update()
    #     self.group_sprites_water.draw(self.surface)

    # Отрисовка спрайтов кораблей
    # def draw_images_ships(self, condition_map):
    #     # Угол поворота блока
    #     angle = 90
    #     if self.axis_block == ConditionAxisShip.Vertical:
    #         angle = 0
    #
    #     # Отрисовка кораблей
    #     # Отрисовка единичных кораблей
    #     if self.len_ship_which_block_located == 1:
    #         self.__draw_sprite_block(self.sprite_block_ship_1, position=self.rect, angle=angle)
    #     # Отрисовка кораблей больше 1
    #     elif self.len_ship_which_block_located > 1:
    #         if self.block_start_ship:
    #             self.__draw_sprite_block(self.part_up_ships, position=self.rect, angle=angle)
    #         elif self.block_end_ship:
    #             self.__draw_sprite_block(self.part_down_ships, position=self.rect, angle=angle)
    #         else:
    #             self.__draw_sprite_block(self.part_center_ships, position=self.rect, angle=angle)
    #
    #     if self.condition_block == ConditionBlock.Hit or self.condition_block == ConditionBlock.Lock:
    #         if condition_map == ConditionPlayerMap.Player:
    #             self.__draw_sprite_block(self.sprite_cross_2, position=self.rect)
    #         else:
    #             self.__draw_sprite_block(self.sprite_cross_1, position=self.rect)
    #     elif self.condition_block == ConditionBlock.Miss:
    #         self.__draw_sprite_block(self.miss_circle, position=self.rect)
    # Отрисовка спрайта на блоке
    # def __draw_sprite_block(self, sprite, position=(0, 0), angle=0) -> None:
    #     if angle != 0:
    #         sprite = pygame.transform.rotate(sprite, angle)
    #     self.surface.blit(sprite, position)
    # Проверка состояния блока
    # def check_condition_block(self):
    #     function_block = {}
    #     # По блоку попали
    #     if self.condition_block == ConditionBlock.Selected:
    #         function_block = {'function': 'hit', 'next_motion': False}
    #         self.change_to_hit()
    #     # Промах
    #     elif self.condition_block == ConditionBlock.Empty:
    #         function_block = {'function': 'miss', 'next_motion': True}
    #         self.change_to_miss()
    #     return function_block
