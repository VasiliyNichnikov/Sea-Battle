from pygame import Surface, Vector2
from scripts.lobby.lobbyParameters import HEIGHT_LINE, WIDTH_BLOCK, BACKGROUND_BLOCK_LINE
from scripts.images.image import Image
from scripts.main_objects.transform import Transform


class BackgroundLine:
    def __init__(self, surface: Surface):
        self.transform = Transform()
        self.transform.size = Vector2(WIDTH_BLOCK, HEIGHT_LINE)

        self.image = Image()
        self.image.path = BACKGROUND_BLOCK_LINE

        self.__surface = surface
        self.loading_image()

    def loading_image(self):
        self.image.loading_image(self.transform.size)

    def draw(self) -> None:
        # self.transform.change_position_children()
        x, y = self.transform.position

        # if local:
        #     x, y = self.transform.get_global_position()

        self.__surface.blit(self.image.image, (x, y))
