from pygame import Surface
from scripts.images.load_image import load_image
from scripts.position.positioning_operation import PositioningOperation, PositionAndSize, SelectPositioning


class Image(PositioningOperation):
    def __init__(self, surface: Surface, path: str, parent: PositionAndSize, selected_positioning: SelectPositioning,
                 height: int, width: int,
                 shift_x: int = 0, shift_y: int = 0):
        super().__init__(parent, selected_positioning, height, width, shift_x, shift_y)
        self.__parent = parent
        self.__surface = surface
        self.__path_image = path
        self.__image = load_image(path, width, height, proportionately=False)

    def draw(self):
        super(Image, self).draw()
        self.__surface.blit(self.__image, (self.x, self.y))
