import pygame
import random
from images.loadImage import load_image
from colorsAndMainParameters import block_size


# Анимация воды
class AnimationWater(pygame.sprite.Sprite):
    def __init__(self, rect):
        super(AnimationWater, self).__init__()

        # Пути до изображений воды
        self.water_1_path = '../static/waters/water1.png'
        self.water_2_path = '../static/waters/water2.png'

        # Создание спрайтов воды
        water_sprite_1 = load_image(self.water_1_path, width=block_size, height=block_size)
        water_sprite_2 = load_image(self.water_2_path, width=block_size, height=block_size)
        self.images = [water_sprite_1, water_sprite_2]

        self.slowing_down = 100
        self.frame = random.randint(0, self.slowing_down * len(self.images) - 1)
        self.image = self.images[self.frame // self.slowing_down]
        self.rect = rect

    def update(self):
        self.frame += 1
        if self.frame >= len(self.images) * self.slowing_down:
            self.frame = 0
        self.image = self.images[self.frame // self.slowing_down]
