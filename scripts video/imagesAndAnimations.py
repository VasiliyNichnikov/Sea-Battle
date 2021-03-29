import pygame
import random
from colorsAndMainParameters import block_size


def load_image(path_sprite, select_size=True, size_x=0, size_y=0):
    image = pygame.image.load(path_sprite)
    if size_x != 0 and size_y != 0:
        if select_size is False:
            w, h = size_x, size_y
        else:
            image_size_x, image_size_y = image.get_width(), image.get_height()
            ratio = min(float(size_x) / image_size_x, float(size_y) / image_size_y)
            w = int(image_size_x * ratio)
            h = int(image_size_y * ratio)
        image = pygame.transform.scale(image, (w, h))
    return image


# Анимация воды
class AnimationWater(pygame.sprite.Sprite):
    def __init__(self, rect):
        super(AnimationWater, self).__init__()

        # Пути до изображений воды
        self.water_1_path = '../static/waters/water1.png'
        self.water_2_path = '../static/waters/water2.png'

        # Создание спрайтов воды
        water_sprite_1 = load_image(self.water_1_path, size_x=block_size, size_y=block_size)
        water_sprite_2 = load_image(self.water_2_path, size_x=block_size, size_y=block_size)
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
