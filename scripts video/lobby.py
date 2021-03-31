import pygame
from requests import Session
import sys
from colorsAndMainParameters import screen_height, screen_width, path_background_menu, FPS, size_field_top, \
    block_lobby, distance_between_block_lobby, path_font
from colorsAndMainParameters import WHITE, COLOR_TOP_BLOCK, GREEN, RED, YANDEX_COLOR
from lobbyBlock import BlockLobby
from imagesAndAnimations import load_image


class Menu:
    def __init__(self):
        self.FPS = FPS

        pygame.init()
        self.surface = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Sea Battle')
        self.surface.fill(WHITE)

        self.list_lobbies = []

        session = Session()

        get_lobbies = session.get('http://127.0.0.1:5002/getting_lobbies')
        if get_lobbies.status_code == 200:
            self.list_lobbies = get_lobbies.json()['list_lobbies']

        # Максимальное кол-во блоков лобби
        self.max_blocks = len(self.list_lobbies)
        # Выбранный блок лобби
        self.select_number_block = 0

        # Выбранный блок (класс)
        self.select_block_class = None

        # Задний фон меню
        self.background_image = load_image(path_background_menu, size_x=screen_width,
                                           size_y=screen_height, select_size=False)
        self.blocks_lobbies = [BlockLobby(self.surface, lobby['name'], lobby['lock']) for lobby in self.list_lobbies]

    def start_menu(self):
        while True:
            # Background -----------------------------------------------------------------------------------------------
            self.surface.fill(WHITE)
            self.surface.blit(self.background_image, (0, 0))

            y = size_field_top + distance_between_block_lobby - (
                    block_lobby + distance_between_block_lobby) * self.select_number_block
            for lobby_index in range(len(self.blocks_lobbies)):
                select_block = False
                if lobby_index == self.select_number_block:
                    self.select_block_class = self.blocks_lobbies[lobby_index]
                    select_block = True
                self.blocks_lobbies[lobby_index].draw_block(y, select_block)
                y += block_lobby + distance_between_block_lobby

            pygame.draw.rect(self.surface, COLOR_TOP_BLOCK, (0, 0, screen_width, size_field_top))
            # Events ---------------------------------------------------------------------------------------------------
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        pass
                        # print(self.password_text)
                    elif event.key == pygame.K_BACKSPACE:
                        print( self.select_block_class.password_text)
                        self.select_block_class.password_text = self.select_block_class.password_text[:-1]
                    elif len(self.select_block_class.password_text) + 1 <= 4:
                        self.select_block_class.password_text += event.unicode

                    if event.key == pygame.K_UP and self.select_number_block - 1 >= 0:
                        self.select_number_block -= 1
                    if event.key == pygame.K_DOWN and self.select_number_block + 1 < self.max_blocks:
                        self.select_number_block += 1

            self.clock.tick(FPS)
            pygame.display.update()


if __name__ == '__main__':
    menu = Menu()
    menu.start_menu()
