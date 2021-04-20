import pygame
from pygame import Vector2
from requests import Session
import sys
# Пустой объект
from scripts.draw_objects.empty import Empty
# Блок лобби
from scripts.lobby.lobbyBlock import LobbyBlock
# Позиция объектов
from scripts.position.positioning_operation import PositioningOperation, PositionAndSize, SelectPositioning
# Изображения
from scripts.images.image import Image
# Дополнительные параметры
from scripts.colors import WHITE, COLOR_TOP_BLOCK
from scripts.main.mainParameters import FPS, BACKGROUND_MENU_LOBBY
from scripts.lobby.lobbyParameters import HEIGHT_BLOCK, WIDTH_BLOCK, \
    DISTANCE_BETWEEN_BLOCKS, ANIMATION_SPEED, HEIGHT_SCREEN, WIDTH_SCREEN


class Lobby(PositioningOperation):
    def __init__(self, parent: PositionAndSize, selected_positioning: SelectPositioning, height: int, width: int):
        super().__init__(parent, selected_positioning, height, width)
        pygame.init()
        self.__creating_screen()
        condition, values = self.__connecting_server()

        self.background = Image(surface=self.surface, path=BACKGROUND_MENU_LOBBY, parent=self,
                                selected_positioning=SelectPositioning.center,
                                height=self.height, width=self.width)
        self.__movement_block = False

        if condition:
            # Максимальное кол-во блоков лобби
            self.__max_blocks = len(values['list_lobbies'])

            self.parent_blocks_lobbies = Empty(surface=self.surface)
            self.parent_blocks_lobbies.transform.size = Vector2(WIDTH_BLOCK,
                                                                (HEIGHT_BLOCK + DISTANCE_BETWEEN_BLOCKS)
                                                                * self.__max_blocks)
            self.parent_blocks_lobbies.transform.position = Vector2(5, HEIGHT_BLOCK)
            self.parent_blocks_lobbies.outline = 1

            self.__initializing_blocks(values)
            self.__length_height_blocks = (HEIGHT_BLOCK + DISTANCE_BETWEEN_BLOCKS) * (self.__max_blocks + 1)
            if self.__length_height_blocks > HEIGHT_SCREEN:
                self.__movement_block = True

    def __creating_screen(self):
        self.FPS = FPS
        self.surface = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Sea Battle')
        self.surface.fill(WHITE)

    def __connecting_server(self) -> (bool, str):
        session = Session()
        get_lobbies = session.get('http://127.0.0.1:5002/getting_lobbies')

        if get_lobbies.status_code == 200:
            return True, get_lobbies.json()
        return False, None

    def __initializing_blocks(self, values):
        self.__blocks = [
            LobbyBlock(surface=self.surface, name=values['list_lobbies'][lobby_index]['name'], index=lobby_index,
                       parent=self.parent_blocks_lobbies, width=self.parent_blocks_lobbies.transform.size.x,
                       height=HEIGHT_BLOCK,
                       shift_y=(HEIGHT_BLOCK + DISTANCE_BETWEEN_BLOCKS) * lobby_index,
                       lock=values['list_lobbies'][lobby_index]['lock'], selected_positioning=SelectPositioning.up)
            for lobby_index in range(self.__max_blocks)]

    def start_lobby(self):
        while True:
            # Background -----------------------------------------------------------------------------------------------
            self.background.draw()
            self.parent_blocks_lobbies.draw()

            for block_lobby in self.__blocks:
                block_lobby.draw()

            # pygame.draw.rect(self.surface, COLOR_TOP_BLOCK,
            #                  (0, 0, WIDTH_SCREEN, HEIGHT_BLOCK - DISTANCE_BETWEEN_BLOCKS))

            # Events ---------------------------------------------------------------------------------------------------
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    pass
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pass
                    if self.__movement_block:
                        if event.button == 4:
                            self.parent_blocks_lobbies.transform.position = Vector2(self.parent_blocks_lobbies.transform.position.x,
                                                                                    self.parent_blocks_lobbies.transform.position.y + ANIMATION_SPEED)
                        elif event.button == 5:
                            self.parent_blocks_lobbies.transform.position = Vector2(self.parent_blocks_lobbies.transform.position.x,
                                self.parent_blocks_lobbies.transform.position.y - ANIMATION_SPEED)

                    # if event.button == 1:
                    #     for block in self.__blocks:
                    #         block.checking_clicks(event.pos, True)
                if event.type == pygame.MOUSEBUTTONUP:
                    pass

            self.clock.tick(FPS)
            pygame.display.update()
