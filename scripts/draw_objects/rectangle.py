from pygame import Surface, Vector2
from scripts.colors import BLACK
from pygame import draw as draw_pg


class Rectangle:
    def __init__(self):
        super().__init__()
        self.color = BLACK
        self.outline = 0
