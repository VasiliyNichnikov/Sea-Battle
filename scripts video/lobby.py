import pygame
from requests import Session
import sys
from lobbyBlock import LobbyBlock
from colorsAndMainParameters import screen_height, screen_width, path_background_menu, FPS, size_field_top, \
    block_lobby, distance_between_block_lobby, path_font, path_block_lobby_not_selected, path_text_selection, \
    path_block_lobby_pressed
from colorsAndMainParameters import WHITE, COLOR_TOP_BLOCK, COLOR_GRAY_BLOCK, RED, YANDEX_COLOR
from textAndButton import Text
from imagesAndAnimations import load_image


class Lobby:
    def __init__(self):
        self.FPS = FPS

        pygame.init()
        self.surface = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Sea Battle')
        self.surface.fill(WHITE)

        self.list_objects_lobbies = []

        session = Session()

        get_lobbies = session.get('http://127.0.0.1:5002/getting_lobbies')
        if get_lobbies.status_code == 200:
            self.list_objects_lobbies = [LobbyBlock(self.surface, get_lobbies.json()['list_lobbies'][lobby_index]['name'], lobby_index, lock=get_lobbies.json()['list_lobbies'][lobby_index]['lock'])
                                         for lobby_index in range(len(get_lobbies.json()['list_lobbies']))]

        # Максимальное кол-во блоков лобби
        self.max_blocks = len(self.list_objects_lobbies)
        # Выбранный блок лобби (номер)
        self.select_number_block = 0

        # Задний фон меню
        self.background_image = load_image(path_background_menu, size_x=screen_width,
                                           size_y=screen_height, select_size=False)

    def start_menu(self):
        while True:
            # Background -----------------------------------------------------------------------------------------------
            self.surface.fill(WHITE)
            self.surface.blit(self.background_image, (0, 0))

            # Отрисовка блоков
            y = size_field_top + distance_between_block_lobby - (
                    block_lobby + distance_between_block_lobby) * self.select_number_block
            for lobby in self.list_objects_lobbies:
                line_y = 0
                block_select = False
                if self.select_number_block == lobby.get_index():
                    block_select = True
                    line_y = 10
                lobby.draw_block(y, block_select)
                y += block_lobby + distance_between_block_lobby + line_y

            pygame.draw.rect(self.surface, COLOR_TOP_BLOCK, (0, 0, screen_width, size_field_top))
            # Events ---------------------------------------------------------------------------------------------------
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if self.list_objects_lobbies[self.select_number_block].lock:
                        block = self.list_objects_lobbies[self.select_number_block]
                        if event.key == pygame.K_RETURN:
                            print(block.text_password)
                        elif event.key == pygame.K_BACKSPACE:
                            block.text_password = block.text_password[:-1]
                        else:
                            block.text_password += event.unicode

                    if event.key == pygame.K_UP and self.select_number_block - 1 >= 0:
                        self.select_number_block -= 1
                    if event.key == pygame.K_DOWN and self.select_number_block + 1 < self.max_blocks:
                        self.select_number_block += 1

            self.clock.tick(FPS)
            pygame.display.update()


if __name__ == '__main__':
    menu = Lobby()
    menu.start_menu()
