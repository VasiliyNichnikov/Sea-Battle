import pygame
import random
import sys


def load_image(image_path):
    return pygame.image.load(image_path)


class AnimationWater(pygame.sprite.Sprite):
    def __init__(self, rect):
        super(AnimationWater, self).__init__()

        self.water_1_path = '../static/waters/water1.png'
        self.water_2_path = '../static/waters/water2.png'

        water_sprite_1 = load_image(self.water_1_path)
        water_sprite_2 = load_image(self.water_2_path)
        self.images = [water_sprite_1, water_sprite_2]
        self.slowing_down = 40

        self.frame = random.randint(0, self.slowing_down * len(self.images) - 1)
        self.image = self.images[self.frame // self.slowing_down]
        self.rect = rect

    def update(self):
        self.frame += 1
        if self.frame >= len(self.images) * self.slowing_down:
            self.frame = 0
        self.image = self.images[self.frame // self.slowing_down]


w, h = 200, 200
runner = True
FPS = 60
SEA_WATER = (0, 102, 170)

pygame.init()
surface = pygame.display.set_mode((w, h))
surface.fill(SEA_WATER)
clock = pygame.time.Clock()
pygame.display.set_caption('Example #1')

water_animation = AnimationWater((w // 2 - 32, h // 2 - 32))
group_sprites_water = pygame.sprite.Group(water_animation)

while runner:
    clock.tick(FPS)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            runner = False

    group_sprites_water.update()
    group_sprites_water.draw(surface)

    pygame.display.flip()
pygame.quit()
sys.exit()


