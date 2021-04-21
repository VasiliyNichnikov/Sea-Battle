import os
from pygame import Surface, Vector2
from typing import Union
from pygame.surface import SurfaceType
from scripts.images.loadImage import load_image


class Image:
    def __init__(self):
        self.__path = ""
        self.__image: Union[Surface, SurfaceType] = None

    @property
    def path(self) -> str:
        return self.__path

    @path.setter
    def path(self, value) -> None:
        if os.path.exists(value):
            self.__path = value

    @property
    def image(self) -> Union[Surface, SurfaceType]:
        return self.__image

    def loading_image(self, size: Vector2) -> bool:
        if self.__path != "" and size.x != 0 and size.y != 0:
            self.__image = load_image(self.__path, int(size.x), int(size.y), proportionately=False)
            return True
        return False
